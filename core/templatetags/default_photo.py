from django.template import Library

from photos.models import Photo
from albums.models import AlbumAccess

from django.contrib.contenttypes.models import ContentType


register = Library()

@register.filter(name="default_photo")
def default_photo(album_object):
    # print(isinstance(album_object.content_object, AlbumAccess))
    related_album = album_object.content_object.album
    default_photo = Photo.objects.get(album=related_album, is_default=True)
    return default_photo.image.url
