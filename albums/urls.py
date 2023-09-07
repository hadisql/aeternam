from django.urls import path

from .views import AlbumListView, AlbumCreateView, AlbumDetailView, AlbumDeleteView, album_access

app_name = "albums"

urlpatterns = [
    path('create/', AlbumCreateView.as_view(), name='album_create'),
    path('', AlbumListView.as_view(), name='albums_view'),
    path('<int:pk>/detail', AlbumDetailView.as_view(), name='album_detail'),
    path('<int:pk>/delete', AlbumDeleteView.as_view(), name='album_delete'),
    path('<int:pk>/settings', album_access, name='album-access'),
]
