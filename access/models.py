from django.db import models

from accounts.models import CustomUser
from photos.models import Album



# -------- Album Access ---------
class AlbumAccess(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='accesses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_accesses')
    has_access = models.BooleanField(default=False)

# ------- Access Requests ---------
class AlbumAccessRequest(models.Model):
    user_receiving = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_req_receiver')
    user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_req_sender')
    message_from_sender = models.TextField(blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
