from django.db import models
from sorl.thumbnail import ImageField

from albums.models import Album
from accounts.models import CustomUser
import os



# -------------------------
# ------- Photos ----------
# -------------------------

def album_photo_directory_path(instance, filename):
    # folder location for the saved albums
    return f"albums/{instance.album.id}/{filename}"

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos_album')
    image = ImageField(upload_to=album_photo_directory_path, null=True)
    is_default = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        # Add a unique constraint to ensure only one default photo per album
        constraints = [
            models.UniqueConstraint(fields=['album'], condition=models.Q(is_default=True), name='unique_default_photo_per_album'),
        ]

    def delete(self, *args, **kwargs):
        # Delete the photo file from storage when the Photo object is deleted
        os.remove(self.image.path)

        # Check if the photo being deleted is the default photo
        if self.is_default:
            album = self.album
            self.is_default = False # necessary to respect the unique constraint
            self.save()
            # Get the next photo in the album to set as the new default photo
            next_photo = Photo.objects.filter(album=album).exclude(pk=self.pk).first()
            if next_photo:
                next_photo.is_default = True
                next_photo.save()

        super().delete(*args, **kwargs)

    def __str__(self) -> str:
      return f"Photo {self.pk} (in Album {self.album.pk})"
