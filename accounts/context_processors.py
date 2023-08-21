from .models import Notification

from access.models import AlbumAccess
from .models import RelationRequest
from comments_likes.models import Comment

def notifications(request):

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user,
                                                    is_read=False)

        categorized_notifications = {
            'relation_request': [],
            'album_access': [],
            'comment': [],
        }

        for notification in notifications:
            if isinstance(notification.content_object, AlbumAccess):
                categorized_notifications['album_access'].append(notification)
            elif isinstance(notification.content_object, RelationRequest):
                categorized_notifications['relation_request'].append(notification)
            elif isinstance(notification.content_object, Comment):
                categorized_notifications['comment'].append(notification)

        notifs_count = len(notifications)

        context = {'categorized_notifications': categorized_notifications,
                   'notifs_count': notifs_count}
        return context

    return {}
