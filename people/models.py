from django.db import models
from django.utils import timezone

from user.models import User


# Create your models here.
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendRequest')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    dateRequest = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s request to be friend with %s" % (
            self.sender.first_name, self.friend.first_name
        )


class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_friends")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="which_my_friends")
    dateAccept = models.DateTimeField(default=timezone.now)
