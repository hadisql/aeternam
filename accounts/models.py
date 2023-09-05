from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail import ImageField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
          Create and save a user with the given username, email, and password.
          """
        if not email:
            raise ValueError('The given email must be set')
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
    profile_picture = ImageField(_('profile picture'), upload_to='profile_pictures/', blank=True, default='profile_pictures/default.jpg')
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True, null=True)
    bio = models.TextField(_('bio/description'), blank=True, null=True)
    premium_member = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_fields(self):
        # looping through the attributes in order to display them in profile.html
        show = ('first_name','last_name','email', 'date_of_birth', 'country', 'bio')
        return [(field.verbose_name, field.value_to_string(self)) for field in CustomUser._meta.fields if field.name in show]

    def __str__(self):
        return self.email



class Relation(models.Model):
    user_receiving = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_receiver')
    user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_sender')

    RELATION_CHOICES =(
        ("UNDEFINED", "UNDEFINED"),
        ("SIBLING", "SIBLING"),
        ("PARENT/CHILDREN", "PARENT/CHILDREN"),
        ("COUSIN", "COUSIN"),
        ("AUNT-UNCLE/NEPHEW-NIECE", "AUNT-UNCLE/NEPHEW-NIECE"),
        ("GRANDPARENT/GRANDCHILDREN", "GRANDPARENT/GRANDCHILDREN"),
        ("BROTHER/SISTER IN LAW", "BROTHER/SISTER IN LAW"),
        ("FRIEND", "FRIEND"),
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

    relation_type = models.CharField(max_length=50, choices=RELATION_CHOICES, default="UNDEFINED")

    class Meta:
        # Unique_together constraint to ensure unique pairs of users
        unique_together = ['user_receiving', 'user_sending']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create a notification when user sends a request
        title = "Connection request"
        message=f"{self.user_sending.first_name or self.user_sending} sent you a connection request."
        create_notification(self.user_receiving, ContentType.objects.get_for_model(self), self.pk, message, title)


    def delete(self, *args, **kwargs):
        # deleting notification when user cancel request
        mark_notification_as_read(self.user_receiving, ContentType.objects.get_for_model(self), self.pk)

        super().delete(*args, **kwargs) #the deletion should happen AFTER marking the notification (in order to retrieve the correct object_id)




class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='concerned_user_notif')
    identifier = models.CharField(max_length=255, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    message = models.TextField()
    title = models.CharField(max_length=255) # used in template automatically
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['created_at']

# When creating a notification
def create_notification(user, content_type, object_id, message, title):
    identifier = f"{content_type.model}{object_id}-{user.pk}"
    Notification.objects.create(
        user=user,
        identifier=identifier,
        content_type=content_type,
        object_id=object_id,
        message=message,
        title = title
    )

# When marking a notification as read
def mark_notification_as_read(user, content_type, object_id):
    identifier = f"{content_type.model}{object_id}-{user.pk}"
    print(f"identifier of notification before marking as read :{identifier}")
    notifications = Notification.objects.filter(user=user, identifier=identifier)
    print(f"querying the notification: {notifications}")
    notifications.update(is_read=True)
