from django import template

from photos.models import Photo

register = template.Library()

@register.filter(name='list_item')
def list_item(lst, i):
    try:
        return lst[i]
    except:
        return None

#https://stackoverflow.com/questions/53287022/django-template-access-to-list-item-by-forloop-counter

@register.filter(name='is_empty')
def is_empty(album):
    return not Photo.objects.filter(album=album).exists()



from django.core.files.images import ImageFile
from django.core.files.storage import get_storage_class

from django.conf import settings

@register.filter
def static_image(path):
    """
    source : https://stackoverflow.com/questions/7490684/using-static-images-with-sorl-thumbnail

    {% thumbnail "/img/default_avatar.png"|static_image "50x50" as img %}
        <img src="{{ MEDIA_URL }}{{img}}"/>
    {% endthumbnail %}
    """
    storage_class = get_storage_class(settings.STATICFILES_STORAGE)
    storage = storage_class()
    image = ImageFile(storage.open(path))
    image.storage = storage
    return image
