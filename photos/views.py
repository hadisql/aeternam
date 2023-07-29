from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.views.generic.edit import FormView

from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages #used in add_photos_to_album
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Photo
from .forms import PhotoForm

from albums.models import Album



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
        return reverse_lazy('albums:album_detail', kwargs={'pk': self.kwargs['album_id']})




class PhotoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Photo
    template_name = "photos/photo_detail.html"

    def test_func(self):
        photo_id = self.kwargs['pk']
        photo = Photo.objects.get(id=photo_id)
        return self.request.user == photo.album.creator  # Check if the logged-in user owns the photo

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = context['photo']
        album = photo.album
        photos = Photo.objects.filter(album=album)
        context['photos'] = photos
        return context

# -----------------------------
# --------- DELETE  -----------
# -----------------------------

class PhotosDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    fields = '__all__'
    context_object_name = 'photo'


    def test_func(self):
        photo_id = self.kwargs['pk']
        photo = Photo.objects.get(id=photo_id)
        return self.request.user == photo.album.creator  # Check if the logged-in user owns the album

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")

    def get_success_url(self):
        album_id = self.object.album.pk
        return reverse('albums:album_detail', kwargs={'pk':album_id})

    def delete(self, request, *args, **kwargs):
        # Override the delete method to handle success URL redirection
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
