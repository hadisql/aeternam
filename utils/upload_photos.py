from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from photos.models import Photo, PhotoAccess


def upload_photos(self, album, files, existing_photos, total_photos):

    allowed_image_types = ['image/jpeg', 'image/png', 'image/gif']
    valid_images = []
    skipped_files = []

    # Client-side validation: Check file types before uploading
    for file in files:
        if file.content_type in allowed_image_types:
            valid_images.append(file)
        else:
            skipped_files.append(file)
            messages.warning(self.request, _("Skipped a non-photo file: {}").format(file.name))

    n_photos_uploaded = len(valid_images) # used in messages
    if len(total_photos) < self.request.user.photo_limit: # continue if user doesn't reach his photo limit
        if not existing_photos:
            # Handle the first image separately
            if valid_images:
                first_file = valid_images.pop(0)
                photo = Photo(album=album, image=first_file, is_default=True, uploaded_by=self.request.user)
                photo.save()
                PhotoAccess.objects.create(photo=photo, user=self.request.user)
                if self.request.user != album.creator:
                    PhotoAccess.objects.create(photo=photo, user=album.creator)

        for image in valid_images:
            total_photos = Photo.objects.filter(uploaded_by=self.request.user)
            photo = Photo(album=album, image=image, uploaded_by=self.request.user)
            photo.save()
            PhotoAccess.objects.create(photo=photo, user=self.request.user)
            if self.request.user != album.creator:
                PhotoAccess.objects.create(photo=photo, user=album.creator)
            total_photos = Photo.objects.filter(uploaded_by=self.request.user)
            if len(total_photos) == int(0.8 * self.request.user.photo_limit):
                messages.warning(self.request, _("You've reached 80% of your maximum photo upload limit"))

        if valid_images:
            if n_photos_uploaded <= 1:
                messages.success(self.request, _('1 photo was uploaded successfully'))
            elif n_photos_uploaded > 1 and not existing_photos:
                messages.success(self.request, _('Album successfully created, with {} photos').format(n_photos_uploaded))
            else:
                messages.success(self.request, _('{} photos were uploaded successfully').format(n_photos_uploaded))
        else:
            messages.warning(self.request, _('No valid photos were uploaded'))

    else:
        messages.error(self.request, _("You have reached your maximum amount of photos to upload: {} photos").format(self.request.user.photo_limit))
