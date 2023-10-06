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
