from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):

    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('accounts:account_view', pk=request.user.pk) #forces to redirect to main page when user is authenticated

    return render(request, "core/index.html")


# def unread_notifications(request):
#     if request.method == 'GET' and request.user.is_authenticated:
#         notifications = Notification.objects.filter(user=request.user, is_read=False)
#         context = {'notifications': notifications}
#     return render(request, 'notifications/unread.html', context)
