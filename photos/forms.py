from django import forms
from multiupload.fields import MultiImageField, MultiUploadMetaInput

from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']


class PhotoForm(forms.Form):
    photos = MultiImageField(min_num=1, max_num=10, max_file_size=1024*1024*5)
