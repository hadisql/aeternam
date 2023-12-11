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
        'relation': 'accounts:account_view',
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
    elif content_object and content_type == 'relation':
        return content_object.user_receiving.pk
    elif content_object and content_type == 'relationrequest':
        return content_object.user_sending.pk
    elif content_object and content_type == 'album':
        return content_object.pk
    else :
        return None

# Define the custom filter to map the flags for each language
@register.filter(name='get_language_flag')
def get_language_flag(language):
    lang_mappings = {
        'fr': '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" id="flag-icons-fr" viewBox="0 0 640 480"><path fill="#fff" d="M0 0h640v480H0z"/><path fill="#000091" d="M0 0h213.3v480H0z"/><path fill="#e1000f" d="M426.7 0H640v480H426.7z"/></svg>',
        'en': '<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" id="flag-icons-gb" viewBox="0 0 640 480"><path fill="#012169" d="M0 0h640v480H0z"/><path fill="#FFF" d="m75 0 244 181L562 0h78v62L400 241l240 178v61h-80L320 301 81 480H0v-60l239-178L0 64V0h75z"/><path fill="#C8102E" d="m424 281 216 159v40L369 281h55zm-184 20 6 35L54 480H0l240-179zM640 0v3L391 191l2-44L590 0h50zM0 0l239 176h-60L0 42V0z"/><path fill="#FFF" d="M241 0v480h160V0H241zM0 160v160h640V160H0z"/><path fill="#C8102E" d="M0 193v96h640v-96H0zM273 0v480h96V0h-96z"/></svg>',
    }
    return lang_mappings.get(language, '')  # Default to empty string if not found
