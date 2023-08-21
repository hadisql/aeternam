from django.db import models

from accounts.models import CustomUser
from photos.models import Album

from accounts.models import Notification, create_notification
from django.contrib.contenttypes.models import ContentType


# -------- Album Access ---------
class AlbumAccess(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='accesses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_accesses')

    class Meta:
        unique_together = ['album', 'user']

    def __str__(self) -> str:
        return f"Album {self.album.pk} (creator {self.album.creator.first_name or self.album.creator}): {self.user.first_name or self.user.email}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        #create notification to concerned user
        message=f"{self.user.first_name or self.user} gave you access to the album {self.album.title}."
        create_notification(self.user, ContentType.objects.get_for_model(self),self.pk, message=message)

# ------- Access Requests ---------
# class AlbumAccessRequest(models.Model):
#     user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_req_sender')
#     album = models.ForeignKey(Album, on_delete=models.CASCADE)
