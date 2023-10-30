from django.template import Library

from photos.models import Photo
from albums.models import AlbumAccess, Album

from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import stringfilter



register = Library()

@register.filter(name="default_photo")
def default_photo(album_object):
    # print(isinstance(album_object.content_object, AlbumAccess))
    related_album = album_object.content_object.album
    default_photo = Photo.objects.get(album=related_album, is_default=True)
    return default_photo.image.url


@register.filter
@stringfilter
def up_to(value, delimiter=None):
    '''Used specifically for time information along with timesince filter
    to shorten the timesince information (3 weeks, 2 hours -> 3 weeks)'''
    return value.split(delimiter)[0]
up_to.is_safe = True


####### Processing Notifications  ######

@register.filter(name="get_notif_name")
def get_notif_name(notif_content_type):
    if notif_content_type == ContentType.objects.get_for_model(Album):
        return 'photo access'
    return str(notif_content_type).split('|')[1][1:]

# Define the custom filter to map content types to URLs.
@register.filter(name='get_url_mapping')
def get_url_mapping(content_type):
    url_mappings = {
        'albumaccess': 'albums:album_detail',
        'relationrequest': 'accounts:account_view',
        'comment': 'photos:photo_detail',
        'album': 'albums:album_detail',
        # ... more mapping if needed
    }
    return url_mappings.get(content_type, '')  # Default to empty string if not found

@register.filter(name='get_notif_param')
def get_notif_param(notification):
    content_type = notification.content_type.model
    content_object = notification.content_object
    if content_object and content_type == 'comment':
        return content_object.commented_photo.pk
    elif content_object and content_type == 'albumaccess':
        return content_object.album.pk
    elif content_object and content_type == 'relationrequest':
        return content_object.user_sending.pk
    elif content_object and content_type == 'album':
        return content_object.pk
    else :
        return None
