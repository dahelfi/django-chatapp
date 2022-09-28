from email.policy import default
from django.db import models
from django.db.models.fields import DateField
from datetime import date
from django.conf import settings

# Create your models here.

class Chat(models.Model):
    participant1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant1_chat_set', default=None, blank=True, null=True)
    participant2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant2_chat_set', default=None, blank=True, null=True)
   

class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = DateField(default=date.today)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')
