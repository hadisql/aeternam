from django.db import models
from accounts.models import CustomUser
from django.conf import settings
import shutil
import os


# ----------------------
# ------ Albums --------
# ----------------------

def album_directory_path(instance, filename):
    return f"albums/{instance.id}/{filename}"

class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_albums')

    def delete(self, *args, **kwargs):
        # Delete the album folder along with its photos
        album_directory = os.path.join(settings.MEDIA_ROOT, album_directory_path(self, ''))
        if os.path.exists(album_directory):
            # shutil.remtree deletes the folder and its contents
            shutil.rmtree(album_directory)
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"Album {self.pk} created by {self.creator}"

class AlbumAccess(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='accesses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_accesses')
    is_contributor = models.BooleanField(default=False)



# -------------------------
# ------- Photos ----------
# -------------------------

def album_photo_directory_path(instance, filename):
    # folder location for the saved albums
    return f"albums/{instance.album.id}/{filename}"

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=album_photo_directory_path)
    is_default = models.BooleanField(default=False)

    class Meta:
        # Add a unique constraint to ensure only one default photo per album
        constraints = [
            models.UniqueConstraint(fields=['album'], condition=models.Q(is_default=True), name='unique_default_photo_per_album'),
        ]

    def delete(self, *args, **kwargs):
        # Delete the photo file from storage when the Photo object is deleted
        os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
      return f"Photo {self.pk} (in Album {self.album.pk})"
