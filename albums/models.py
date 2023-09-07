from django.db import models

from accounts.models import CustomUser
import os
import shutil
from django.conf import settings

import sorl.thumbnail
from photos.models import Photo
from accounts.models import Notification, create_notification
from django.contrib.contenttypes.models import ContentType

# ----------------------
# ------ Albums --------
# ----------------------

def album_directory_path(instance, filename):
    return f"albums/{instance.id}/{filename}"

class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_albums')

    def delete(self, *args, **kwargs):
        # delete all photos in album with sorl delete method, to make sure cache is deleted along
        photos_to_delete = Photo.objects.filter(album=self)
        for photo in photos_to_delete:
            sorl.thumbnail.delete(photo)
            print(f"deleted photo {photo.id} with sorl-thumbnail delete method")
        # Delete the album folder along with its photos
        album_directory = os.path.join(settings.MEDIA_ROOT, album_directory_path(self, ''))
        if os.path.exists(album_directory):
            # shutil.remtree deletes the folder and its contents
            shutil.rmtree(album_directory)
        super().delete(*args, **kwargs)


    def __str__(self) -> str:
        return f"Album {self.pk} '{self.title}' created by {self.creator.first_name or self.creator}"

# -------------------------------
# -------- Album Access ---------
# -------------------------------

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
        title='Album Access granted'
        message=f"{self.album.creator.first_name or self.album.creator} gave you access to the album {self.album.title}."
        create_notification(self.user, ContentType.objects.get_for_model(self),self.pk, message=message, title=title)
