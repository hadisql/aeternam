from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail import ImageField

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
    profile_picture = ImageField(_('profile picture'), upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/default.jpg')
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True, null=True)
    bio = models.TextField(_('bio/description'), blank=True, null=True)

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
