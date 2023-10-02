from django import template

register = template.Library()

# Define the custom filter to map content types to URLs.
@register.filter(name='get_url_mapping')
def get_url_mapping(content_type):
    url_mappings = {
        'albumaccess': 'albums:album_detail',
        'relationrequest': 'accounts:account_view',
        'comment': 'photos:photo_detail',
        # ... more mapping if needed
    }
    return url_mappings.get(content_type, '')  # Default to empty string if not found

@register.filter(name='get_notif_param')
def get_notif_param(notification):
    content_type = notification.content_type.model
    content_object = notification.content_object
    if content_type == 'comment':
        return content_object.commented_photo.pk
    elif content_type == 'albumaccess':
        return content_object.album.pk
    elif content_type == 'relationrequest':
        return content_object.user_sending.pk
