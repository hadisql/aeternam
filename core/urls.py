from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path('', views.index, name='index'),
    path('clear_notif_from_navbar/<int:notification_id>/', views.clear_notif_from_navbar, name='clear_notif_from_navbar'),
    path('photo_access_manager/', views.photo_access_manager, name='photo_access_manager'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('get_a_demo/', views.DemoView.as_view(), name='get_a_demo')
    # path('get_a_demo/', views.demo_view, name='get_a_demo'),
]
