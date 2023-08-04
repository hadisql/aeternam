from django.db import models

from accounts.models import CustomUser
from photos.models import Album



# -------- Album Access ---------
class AlbumAccess(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='accesses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_accesses')

    class Meta:
        unique_together = ['album', 'user']

    def __str__(self) -> str:
        return f"Album {self.album.pk} (creator {self.album.creator.first_name or self.album.creator}): {self.user.first_name or self.user.email}"

# ------- Access Requests ---------
# class AlbumAccessRequest(models.Model):
#     user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_req_sender')
#     album = models.ForeignKey(Album, on_delete=models.CASCADE)
