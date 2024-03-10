from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail import ImageField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from utils.edit_image import resize_image
from django.core.files.images import ImageFile
import os
from io import BytesIO

import logging
logger = logging.getLogger(__name__)

class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
          Create and save a user with the given username, email, and password.
          """
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model with email as username field
    """
    username = None

    email = models.EmailField(_('email address'), blank=True, unique=True)
    profile_picture = ImageField(_('profile picture'), upload_to='profile_pictures/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True, null=True)
    premium_member = models.BooleanField(default=False)
    hide_connections = models.BooleanField(default=False)
    photo_limit = models.PositiveSmallIntegerField(default=100)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_fields(self):
        # looping through the attributes in order to display them in profile.html
        show = ('first_name','last_name','email', 'date_of_birth', 'country')
        return [(field.verbose_name, field.value_to_string(self)) for field in CustomUser._meta.fields if field.name in show]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        size_limit = 512*512 # 0.5MB

        # Check if the image size exceeds size limit
        if self.profile_picture and self.profile_picture.size > size_limit:
            logger.info(f"Resizing profile_picture {self.profile_picture.name}...")

            # Get the resized image data
            resized_image_data = resize_image(self.profile_picture, size_limit)
            logger.info(f"Resizing image {self.profile_picture.name}...")

            # Generate a new filename for the resized image
            filename, ext = os.path.splitext(os.path.basename(self.profile_picture.name))
            new_filename = f"{filename}_resized{ext}"

            # Create a new ImageFile object and save it to the image field
            self.profile_picture.save(
                new_filename,
                ImageFile(BytesIO(resized_image_data)),
                save=False
            )
            print("Profile Picture resized successfully.")
            super().save(*args, **kwargs)



class Relation(models.Model):
    user_receiving = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_receiver')
    user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_sender')

    RELATION_CHOICES =(
        ("UNDEFINED", _("UNDEFINED")),
        ("SIBLING", _("SIBLING")),
        ("PARENT/CHILDREN", _("PARENT/CHILDREN")),
        ("COUSIN", _("COUSIN")),
        ("AUNT-UNCLE/NEPHEW-NIECE", _("AUNT-UNCLE/NEPHEW-NIECE")),
        ("GRANDPARENT/GRANDCHILDREN", _("GRANDPARENT/GRANDCHILDREN")),
        ("BROTHER/SISTER IN LAW", _("BROTHER/SISTER IN LAW")),
        ("FRIEND", _("FRIEND")),
        )

    relation_type = models.CharField(max_length=50, choices=RELATION_CHOICES, default="UNDEFINED")

    class Meta:
        # Unique_together constraint to ensure unique pairs of users
        unique_together = ['user_receiving', 'user_sending']

    def save(self, *args, **kwargs):
        # Check if the interchangeable relation already exists
        if Relation.objects.filter(user_receiving=self.user_sending, user_sending=self.user_receiving).exists():
            # If it exists, don't save the new relation
            return
        super(Relation, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_sending} -> {self.user_receiving}"


class RelationRequest(models.Model):
    user_receiving = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_req_receiver')
    user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_req_sender')

    RELATION_CHOICES = Relation.RELATION_CHOICES

    relation_type = models.CharField(max_length=50, choices=RELATION_CHOICES, default=_("UNDEFINED"))

    class Meta:
        # Unique_together constraint to ensure unique pairs of users
        unique_together = ['user_receiving', 'user_sending']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create a notification when user sends a request
        title = _("Connection request")
        message=_("{} sent you a connection request.").format(self.user_sending.first_name or self.user_sending)
        create_notification(self.user_receiving, self.user_sending, ContentType.objects.get_for_model(self), self.pk, message, title)


    def delete(self, *args, **kwargs):
        # deleting notification when user cancel request
        mark_notification_as_read(self.user_receiving, ContentType.objects.get_for_model(self), self.pk)

        super().delete(*args, **kwargs) #the deletion should happen AFTER marking the notification (in order to retrieve the correct object_id)

    def __str__(self):
        return f"{self.user_sending} -> {self.user_receiving}"



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='target_user_notif')
    identifier = models.CharField(max_length=255, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    message = models.TextField()
    title = models.CharField(max_length=255) # used in template automatically
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    user_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user_notif', null=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['created_at']

# When creating a notification
def create_notification(user, user_from, content_type, object_id, message, title):
    identifier = f"{content_type.model}{object_id}-{user.pk}"
    Notification.objects.create(
        user=user,
        identifier=identifier,
        content_type=content_type,
        object_id=object_id,
        message=message,
        title = title,
        user_from=user_from
    )

# When marking a notification as read
def mark_notification_as_read(user, content_type, object_id):
    identifier = f"{content_type.model}{object_id}-{user.pk}"
    print(f"identifier of notification before marking as read :{identifier}")
    notifications = Notification.objects.filter(user=user, identifier=identifier)
    print(f"querying the notification: {notifications}")
    notifications.update(is_read=True)

# def delete_notification(user, content_type, object_id):
#     notification = Notification.objects.filter(user=user, content_type=content_type, object_id=object_id)
#     print(f"querying the notification: {notification}")
#     if notification:
#         notification.delete()
