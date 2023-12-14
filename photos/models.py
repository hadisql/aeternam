from django.db import models
from sorl.thumbnail import ImageField

from accounts.models import CustomUser

import os
from io import BytesIO

from utils.resize_image import resize_image

import logging
logger = logging.getLogger(__name__)

# -------------------------
# ------- Photos ----------
# -------------------------

def album_photo_directory_path(instance, filename):
    # folder location for the saved albums
    return f"albums/{instance.album.id}/{filename}"


class Photo(models.Model):
    album = models.ForeignKey(to='albums.Album', on_delete=models.CASCADE, related_name='photos_album')
    image = ImageField(upload_to=album_photo_directory_path, null=True)
    is_default = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=500 ,null=True)

    class Meta:
        # Add a unique constraint to ensure only one default photo per album
        constraints = [
            models.UniqueConstraint(fields=['album'], condition=models.Q(is_default=True), name='unique_default_photo_per_album'),
        ]

    def save(self, *args, **kwargs):
        # Call the parent class's save method
        super().save(*args, **kwargs)

        size_limit = 1024*1024 # 1MB (1024*1024=1048576 bytes)

        # Check if the image size exceeds size limit
        if self.image.size > size_limit:

            # Get the resized image data
            resized_image_data = resize_image(self.image.path, size_limit)
            logger.info(f"Resizing image {self.image.name}...")
            print(f"Resizing image {self.image.name}...")

            # Create a new ImageFile object and save it to the image field
            from django.core.files.images import ImageFile
            self.image.save(
                os.path.basename(self.image.name),
                ImageFile(BytesIO(resized_image_data)),
                save=False
            )
            logger.info("Image resized successfully.")
            print("Image resized successfully.")
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
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

        # Delete the photo file from storage when the Photo object is deleted
        try:
            os.remove(self.image.path)
        except:
            logger.warning('image file does not exist, associated photo object will be deleted anyway')


        super().delete(*args, **kwargs)

    def __str__(self) -> str:
      return f"Photo {self.pk} (in Album {self.album.pk}) uploaded by {self.uploaded_by}"

class PhotoAccess(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='accessed_photo')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photo_accessing_user')

    class Meta:
        unique_together = ['photo', 'user']

    def __str__(self) -> str:
        return f"Photo {self.photo.pk} accessible to {self.user.get_full_name() or self.user.email} (uploaded by {self.photo.uploaded_by.get_full_name() or self.photo.uploaded_by.email})"
