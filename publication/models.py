from django.db import models
from django.utils import timezone

from user.models import User
from user.utils import upload_to


# Create your models here.
def upload_pubImage(instance, filename):
    return upload_to("publication")(instance, filename)


class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publications")
    datePub = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_pubImage)

    def __str__(self):
        return "pub{} {}".format(self.id, self.author.email)

    @property
    def likesCount(self):
        return self.likes.count()

    @property
    def commentsCount(self):
        return self.comments.count()


class PublicationLike(models.Model):
    pub = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")


class PublicationComment(models.Model):
    pub = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    dateComment = models.DateTimeField(default=timezone.now)
