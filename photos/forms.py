from django import forms
from multiupload.fields import MultiFileField, MultiImageField
from django.core.exceptions import ValidationError
from PIL import Image  # To validate images

from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']

class PhotoForm(forms.Form):
    pass
