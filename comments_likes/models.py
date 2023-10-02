from django.db import models

from accounts.models import CustomUser, create_notification
from photos.models import Photo
from django.contrib.contenttypes.models import ContentType


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # create notification to concerned comment (photo uploader and album owner if different)
        title = 'New comment'
        message=f"{self.author.first_name or self.author} commented on your photo: {self.body}"
        photo_uploader = self.commented_photo.uploaded_by
        album_owner = self.commented_photo.album.creator

        if self.author != photo_uploader or self.author != album_owner:
            create_notification(photo_uploader, self.author, ContentType.objects.get_for_model(self), self.pk, message=message, title=title)
            if photo_uploader != album_owner:
                create_notification(album_owner, self.author, ContentType.objects.get_for_model(self), self.pk, message=message, title=title)
