from django.urls import path

from photos.views import AlbumListView, AlbumCreateView, AlbumUpdateView, AlbumDetailView, AlbumDeleteView, AddPhotosToAlbumView
from photos.views import PhotoDetailView, PhotosDeleteView

app_name = "photos"

urlpatterns = [
    path('create/', AlbumCreateView.as_view(), name='album_create'),
    path('', AlbumListView.as_view(), name='albums_view'),
    path('<int:pk>/detail', AlbumDetailView.as_view(), name='album_detail'),
    path('<int:pk>/edit', AlbumUpdateView.as_view(), name='album_edit'),
    path('<int:album_id>/add-photos/', AddPhotosToAlbumView.as_view(), name='add_photos_to_album'),
    path('<int:pk>/delete', AlbumDeleteView.as_view(), name='album_delete'),
    # path('<int:album_id>/add-photos/', add_photos_to_album, name='add_photos_to_album'),
    path('photo/<int:pk>/detail', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/<int:pk>/delete', PhotosDeleteView.as_view(), name='photo_delete'),
]
