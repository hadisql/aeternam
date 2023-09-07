from .models import Notification

from albums.models import AlbumAccess
from .models import RelationRequest
from comments_likes.models import Comment

def notifications(request):

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user,
                                                    is_read=False).order_by('-created_at')

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

        all_notifications = []
        for notifications_list in categorized_notifications.values():
            all_notifications.extend(notifications_list)

        all_notifications.sort(key=lambda x: x.created_at, reverse=True)

        context = { 'all_notifications': all_notifications,
                    'categorized_notifications': categorized_notifications,
                   'notifs_count': notifs_count}
        return context

    return {}
