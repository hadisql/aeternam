from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView, ListView, DeleteView, UpdateView, DetailView
from django.views.generic.edit import FormView

from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages #used in add_photos_to_album
from django.http import HttpResponseForbidden

from .models import Album, Photo
from .forms import AlbumForm, PhotoForm


# ----------------------------
# ------ CREATE ALBUM --------
# ----------------------------


class AlbumCreateView(LoginRequiredMixin, CreateView):
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
class AlbumListView(LoginRequiredMixin, ListView):
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
class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # -- template name is 'album_form.html'
    model = Album
    form_class = AlbumForm

    def test_func(self):
        album_id = self.kwargs['pk']
        album = Album.objects.get(id=album_id)
        return self.request.user == album.creator  # Check if the logged-in user owns the album

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")


    def get_success_url(self) -> str:
        return reverse('photos:album_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_of_view'] = 'update'
        album_id = self.kwargs['pk']
        context['photos'] = Photo.objects.filter(album=album_id)
        return context


# def add_photos_to_album(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     existing_photos = Photo.objects.filter(album=album)

#     if request.method == 'POST':
#         data = request.POST
#         images = request.FILES.getlist('images')

#         if not existing_photos.exists():
#             first_image = images.pop(0)
#             photo = Photo.objects.create(album=album, image=first_image, is_default=True)

#         for image in images:
#             photo = Photo.objects.create(album=album, image=image)


#         #The messages framework allows you to store messages that persist across requests and can be displayed to the user
#         messages.success(request, 'New photos were uploaded successfully')
#         return redirect('photos:album_detail', pk=album_id)

#     context = {'album': album}
#     return render(request, 'photos/add_photos_to_album.html', context)

class AddPhotosToAlbumView(LoginRequiredMixin, FormView):
    template_name = 'photos/add_photos_to_album.html'
    form_class = PhotoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_id = self.kwargs['album_id']
        context['album'] = get_object_or_404(Album, pk=album_id)
        return context

    def form_valid(self, form):
        album_id = self.kwargs['album_id']
        album = get_object_or_404(Album, pk=album_id)
        existing_photos = Photo.objects.filter(album=album)

        images = self.request.FILES.getlist('images')

        if not existing_photos.exists():
            first_image = images.pop(0)
            photo = Photo.objects.create(album=album, image=first_image, is_default=True)
        for image in images:
            photo = Photo.objects.create(album=album, image=image)

        messages.success(self.request, 'Photos were uploaded successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('photos:album_detail', kwargs={'pk': self.kwargs['album_id']})


# ----------------------------
# ------ DETAIL ALBUM --------
# ----------------------------
class AlbumDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Album
    template_name = "photos/album_detail.html"

    def test_func(self):
        album_id = self.kwargs['pk']
        album = Album.objects.get(id=album_id)
        return self.request.user == album.creator  # Check if the logged-in user owns the album

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_id = self.kwargs['pk']
        context['photos'] = Photo.objects.filter(album=album_id)

        success_message = self.request.GET.get('success_message')
        if success_message:
            context['success_message'] = success_message

        return context

# ----------------------------
# ------ DELETE ALBUM --------
# ----------------------------
class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    fields = '__all__'
    success_url = reverse_lazy('photos:albums_view')
    context_object_name = 'album'

    def test_func(self):
        album_id = self.kwargs['pk']
        album = Album.objects.get(id=album_id)
        return self.request.user == album.creator  # Check if the logged-in user owns the album

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")
