from django.db import models
from sorl.thumbnail import ImageField

from accounts.models import CustomUser

import os
from io import BytesIO
from django.core.files.images import ImageFile
from PIL import Image as PILImage

from utils.edit_image import resize_image

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
        size_limit = 1024*1024  # 1MB (1024*1024=1048576 bytes)

        # Check if the image size exceeds the size limit
        if self.image.size > size_limit:
            # Get the resized image data
            resized_image_data = resize_image(self.image, size_limit)
            logger.info(f"Resizing image {self.image.name}...")

            # Open the resized image using PIL
            resized_image = PILImage.open(BytesIO(resized_image_data))

            # Generate a new filename for the resized image
            filename, ext = os.path.splitext(os.path.basename(self.image.name))
            new_filename = f"{filename}_resized{ext}"

            # Save the resized image to a BytesIO buffer
            with BytesIO() as buffer:
                resized_image.save(buffer, format=resized_image.format)
                buffer.seek(0)

                # Save the resized image to the same location as the original image
                self.image.save(
                    new_filename,
                    ImageFile(buffer),
                    save=False
                )
            logger.info("Image resized successfully.")
        else:
            # Call the parent class's save method if no resizing is needed
            logger.info("Image saved successfully without resizing.")

        # Call the parent class's save method
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

      # Check if another Photo object references the same image file
        other_photos = Photo.objects.filter(image=self.image)
        if other_photos.count() == 1:
            # If no other object references the image, delete the file
            try:
                os.remove(self.image.path)
                logger.success(f'Image {self.image.path} removed')
            except FileNotFoundError:
                logger.warning('Image file not found during deletion')
        else:
            logger.info('Skipping image file deletion as other objects reference it')

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
