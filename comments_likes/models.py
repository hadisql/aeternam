from django.db import models

from accounts.models import CustomUser
from photos.models import Photo

# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="author_comment")
    commented_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="photo_comment")
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) #can be set to False via admin page

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.author}'
