from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .ai_models import SimpleAgentBroker, SimpleAgent
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ai_models.ifImageBot import bot
from asgiref.sync import sync_to_async
from rest_framework import status
from .ai_models.imageGen import ImageGenerator

# Create a single instance of SimpleTestAgent to be reused
agent = SimpleAgentBroker()

def index(request):
    return HttpResponse("Hello, world. You're at the main page.")



@csrf_exempt
def chat(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        message = data.get('message')
        animal = data.get('animal')
        model = data.get('model')
        
        response = agent.call_agent(message, animal, model)
        
        return JsonResponse({'content': response})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

## return the last 20 messages for the animal type
def get_history(request):
    try:
        animal_type = request.GET.get('animal_type')
        if not animal_type:
            return JsonResponse({'error': 'animal_type parameter is required'}, status=400)
        
        specific_agent = agent.get_agent(animal_type)
        
        # Filter out system messages and get last 5 messages
        chat_messages = [msg for msg in specific_agent.messages if msg['role'] != 'system'][-5:]
        
        return JsonResponse({
            'messages': chat_messages,
            'animal_type': animal_type
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['POST'])
def is_image_request(request):
    message = request.data.get('message')
    if not message:
        return Response({'error': 'Message is required'}, status=400)
    
    is_image = bot.is_image_request(message)
    return Response({'is_image': is_image})

@api_view(['POST'])
def generate_image(request):
    """
    API endpoint to generate images using DALL-E
    
    Expected POST data:
    {
        "prompt": "description of the image to generate",
        "size": "1024x1024" (optional),
        "model": "dall-e-3" (optional),
        "n": 1 (optional)
    }
    """
    try:
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        size = request.data.get('size', '1024x1024')
        model = request.data.get('model', 'dall-e-3')
        n = request.data.get('n', 1)
        
        generator = ImageGenerator()
        image_url = generator.generate_image(prompt=prompt, size=size, model=model, n=n)
        
        return Response({'image_url': image_url}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

