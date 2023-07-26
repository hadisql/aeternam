from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView, ListView, DeleteView, UpdateView, DetailView
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render


from .models import Album, Photo
from .forms import AlbumForm, PhotoForm


# ----------------------------
# ------ CREATE ALBUM --------
# ----------------------------


class AlbumCreateView(CreateView):
    # -- template name is 'album_form.html'
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy('photos:albums_view')
    # "redirect" didn't work : The reverse_lazy function is used to lazily reverse the URL, ensuring that it's only evaluated when the view is executed.

    def form_valid(self, form):
        album = form.save(commit=False)
        album.creator = self.request.user
        album.save()

        # Save associated photos to the album
        for image in self.request.FILES.getlist('images'):
            Photo.objects.create(album=album, image=image)

        # Set the first photo as the default photo
        default_photos = Photo.objects.filter(album=album)
        if default_photos.exists():
            default_photo = default_photos.first()
            default_photo.is_default = True
            default_photo.save()

        return super().form_valid(form)

# ----------------------------
# ------ LIST ALBUMS ---------
# ----------------------------
class AlbumListView(ListView):
    model = Album
    template_name = 'photos/albums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # retrieving albums specific to the creator of the albums
        my_albums = Album.objects.filter(creator=self.request.user)

        # Annotate each album with the count of photos associated with it
        my_albums = my_albums.annotate(photo_count=Count('photos'))

        # Create a dictionary to hold album objects and their default photos
        albums_with_default_photos = {}

        for album in my_albums:
            default_photo = album.photos.filter(is_default=True).first()
            if default_photo:
                albums_with_default_photos[album] = default_photo
            else:
                albums_with_default_photos[album] = False

        context['albums_with_default_photos'] = albums_with_default_photos
        return context

# ----------------------------
# ------ UPDATE ALBUM --------
# ----------------------------
class AlbumUpdateView(UpdateView):
    # -- template name is 'album_form.html'
    model = Album
    form_class = AlbumForm

    def get_success_url(self) -> str:
        return reverse('photos:album_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_of_view'] = 'update'
        album_id = self.kwargs['pk']
        context['photos'] = Photo.objects.filter(album=album_id)
        return context

class AddPhotosToAlbumView(View):
    def get(self, request, album_id):
        album = get_object_or_404(Album, pk=album_id)
        photo_form = PhotoForm()
        existing_photos = Photo.objects.filter(album=album)
        return render(request, 'photos/add_photos_to_album.html', {'album': album, 'photo_form': photo_form, 'existing_photos': existing_photos})

    def post(self, request, album_id):
        album = get_object_or_404(Album, pk=album_id)
        photo_form = PhotoForm(request.POST, request.FILES)

        if photo_form.is_valid():
            new_photos = request.FILES.getlist('photos')
            for image in new_photos:
                Photo.objects.create(album=album, image=image)

            return redirect('photos:album_detail', pk=album_id)

        return render(request, 'photos/add_photos_to_album.html', {'album': album, 'photo_form': photo_form})

# ----------------------------
# ------ DETAIL ALBUM --------
# ----------------------------
class AlbumDetailView(DetailView):
    model = Album
    template_name = "photos/album_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_id = self.kwargs['pk']
        context['photos'] = Photo.objects.filter(album=album_id)
        return context

# ----------------------------
# ------ DELETE ALBUM --------
# ----------------------------
class AlbumDeleteView(DeleteView):
    model = Album
    fields = '__all__'
    success_url = reverse_lazy('photos:albums_view')
    context_object_name = 'album'
