from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from only_fan_backend_app.models import ChatHistory

class ChatHistoryManager:
    @staticmethod
    def save_chat(animal_type, messages):
        # Keep only the last 20 chat histories for each animal type
        existing_chats = ChatHistory.objects.filter(animal_type=animal_type)
        if existing_chats.count() >= 20:
            # Delete the oldest entries beyond the 20 limit
            to_delete = existing_chats[19:]
            for chat in to_delete:
                chat.delete()
        
        # Create new chat history
        ChatHistory.objects.create(
            animal_type=animal_type,
            messages=messages
        )

    @staticmethod
    def get_latest_chat(animal_type):
        try:
            return ChatHistory.objects.filter(animal_type=animal_type).first()
        except ObjectDoesNotExist:
            return None 