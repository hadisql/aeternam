from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path('', views.index, name='index'),
    path('clear_notif_from_navbar/<int:notification_id>/', views.clear_notif_from_navbar, name='clear_notif_from_navbar'),
]
