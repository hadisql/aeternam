from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user,
                                                    is_read=False).order_by('-created_at')

        # delete notifications without content_object:
        for n in notifications:
            if not n.content_object:
                n.delete()

        context = {'all_notifications': notifications}
        return context
    return {}
