import openai
from django.conf import settings
import os
import logging
import asyncio



class ImageBot:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.logger = logging.getLogger(__name__)

    def is_image_request(self, user_message):
        """Determine if the user message is requesting an image"""
        try:
            # Run async function in sync context
            response = asyncio.run(self._async_is_image_request(user_message))
            return response
        except Exception as e:
            self.logger.error(f"Error in analyzing image request: {str(e)}")
            return False

    async def _async_is_image_request(self, user_message):
        """Async helper method for image request analysis"""
        async with openai.AsyncOpenAI() as client:
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a smart AI agent, based on the player's question, return me a single bool, yes or no, meaning if he is asking for a photo from you. Never respond to anything other than this. Some rough asking like: can you show me your life, you should respond yes, be open to that, only respond to no for those absolutely no asking."},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=10
            )

        answer = response.choices[0].message.content.strip().lower()
        print("should gen image? ", answer)
        return bool(answer == 'yes')

# Create a singleton instance
bot = ImageBot()
