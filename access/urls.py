from django.urls import path

# from .views import AlbumAccessView
from .views  import album_access

app_name = 'access'

urlpatterns = [
    # path('<int:pk>/settings', AlbumAccessView.as_view(), name='album_access'),
    path('<int:pk>/settings', album_access, name='album-access')
]
