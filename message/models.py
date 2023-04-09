from django.db import models

from user.models import User

from django.utils import timezone


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_received")
    dateSend = models.DateTimeField(default=timezone.now)
    content = models.TextField()
