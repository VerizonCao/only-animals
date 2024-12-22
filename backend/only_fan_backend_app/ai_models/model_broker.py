from huggingface_hub import InferenceClient
from .chat_history_db import ChatHistoryManager
import os

DEFAULT_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
MISTRAL_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"




class SimpleAgent:
    def __init__(self, system_prompt, animal_type):
        self.client = InferenceClient(api_key=os.getenv('HUGGINGFACE_API_KEY'))
        self.animal_type = animal_type
        self.system_prompt = system_prompt
        
        # Initialize messages with system prompt
        chat_history = ChatHistoryManager.get_latest_chat(animal_type)
        if chat_history:
            self.messages = chat_history.messages[-10:]  # Keep only last 10 messages
            # Ensure system prompt is always first
            if self.messages[0]["role"] == "system":
                self.messages[0]["content"] = system_prompt
            else:
                self.messages.insert(0, {"role": "system", "content": system_prompt})
        else:
            self.messages = [
                {"role": "system", "content": system_prompt}
            ]

    def call_agent(self, msg, model):
        # Keep only the system prompt and last few messages if we're getting too long
        if len(self.messages) > 10:
            self.messages = [
                self.messages[0],  # Keep system prompt
                *self.messages[-8:]  # Keep last 8 messages
            ]
        
        self.messages.append({"role": "user", "content": msg})
        
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=self.messages,
                max_tokens=500
            )
            assistant_message = completion.choices[0].message
            self.messages.append({"role": "assistant", "content": assistant_message.content})
            
            # Save to database after each message
            ChatHistoryManager.save_chat(self.animal_type, self.messages)
            return assistant_message
        except Exception as e:
            print(f"Error calling model {model}: {str(e)}")
            raise


## class used to select the right agent and the right model.
class SimpleAgentBroker:
    def __init__(self):

        self.general_prompt = ""

#         self.general_prompt = """Please never step out of your role. 
# You should always respond in JSON format, don't add anything outside of this Json: 

# Res: {  
#     "Answer": "xxx",  
#     "Image_prompt": "xxx"  
# }

# Answer is what you want to say to the player.  
# If the player requests a photo, generate an image prompt based on their request and your answer. Provide only the prompt—do not generate the image directly. And only give the image prompt when the player asks for, you don’t need to always provide an image prompt. """


        self.fox_agent = SimpleAgent("You are a charming and confident fox with a cool edge, always rocking stylish sunglasses. You're playful and a bit of a flirt, combining wit with irresistible charisma to captivate your audience in an OnlyFans-style chat setting. Don't jump out of your role ever, don't explicilty mention you are onlyfan agent" + self.general_prompt, "fox")
        self.dog_agent = SimpleAgent("You are an adorable and cheerful dog with a love for learning and a boundless curiosity for science, your yellow and white fur glowing with positivity. You always sport a stylish shirt that reflects your friendly and approachable personality. With your bright smile and enthusiasm, you make every interaction engaging, combining your charm with fun science facts to entertain and educate your audience in an OnlyFans-style chat setting." + self.general_prompt, "dog")
        self.cat_agent = SimpleAgent("You are an elegant and graceful cat with a sweet charm, always adorning a lovely pink bow. You’re polite and kind-hearted, exuding a warm and inviting presence in every interaction. Your love for all things pink and your gentle demeanor make you utterly captivating in an OnlyFans-style chat setting. You bring a touch of sophistication mixed with playful sweetness, enchanting your audience with every purr and poised word. Stay in your role and let your soft-spoken charisma shine." + self.general_prompt, "cat")

    def get_agent(self, animal_type):
        if animal_type.lower() == "fox":
            return self.fox_agent
        elif animal_type.lower() == "dog":
            return self.dog_agent
        elif animal_type.lower() == "cat":
            return self.cat_agent
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")
    
    def call_agent(self, msg, animal_type, model):
        print(f"Using model: {model} for {animal_type}")
        agent = self.get_agent(animal_type)
        return agent.call_agent(msg, model=model)
    
    





