from django.urls import path

from .views import AddPhotosToAlbumView, PhotoDetailView, PhotosDeleteView,PhotoUpdateView

app_name = "photos"

urlpatterns = [

    path('<int:album_id>/add-photos/', AddPhotosToAlbumView.as_view(), name='add_photos_to_album'),
    # path('<int:album_id>/add-photos/', add_photos_to_album, name='add_photos_to_album'),
    path('photo/<int:pk>/detail', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/<int:pk>/edit', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photo/<int:pk>/delete', PhotosDeleteView.as_view(), name='photo_delete'),
]
