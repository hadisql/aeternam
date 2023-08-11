from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.views.generic.edit import FormView

from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages #used in add_photos_to_album
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Photo
from .forms import PhotoForm, CommentForm

from albums.models import Album
from access.models import AlbumAccess

from comments_likes.models import Comment


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
            photo = Photo.objects.create(album=album, image=first_image, is_default=True, uploaded_by=self.request.user)
        for image in images:
            photo = Photo.objects.create(album=album, image=image, uploaded_by=self.request.user)

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
        has_access = AlbumAccess.objects.filter(album__photos_album = photo, user=self.request.user)
        return self.request.user == photo.album.creator or has_access  # Check if the logged-in user owns the photo

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = context['photo']

        comments = Comment.objects.filter(commented_photo=photo)
        comment_form = CommentForm()

        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        photo_id = self.kwargs['pk']
        photo = Photo.objects.get(id=photo_id)

        if "body" in request.POST:
            comment_form = CommentForm(request.POST, instance=photo)

            if comment_form.is_valid():
                comment_body = comment_form.cleaned_data['body']
                Comment.objects.create(
                    author=request.user,
                    commented_photo=photo,
                    body=comment_body
                    )
                return HttpResponseRedirect(request.path_info)

        return redirect('photos:photo_detail', pk=photo_id)
        # return HttpResponseRedirect(request.path_info)

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
        has_uploaded = photo.uploaded_by == self.request.user
        return self.request.user == photo.album.creator or has_uploaded  # Check if the logged-in user owns the album

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
