from django.db import models

# Import the ChatHistory model from chat_history_db
class ChatHistory(models.Model):
    animal_type = models.CharField(max_length=50)
    messages = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
