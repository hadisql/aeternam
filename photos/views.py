from typing import Any, Dict
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.views.generic.edit import FormView

from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages #used in add_photos_to_album
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Photo
from .forms import PhotoForm, CommentForm, PhotoUpdateForm, PhotoRotationForm

from albums.models import Album
from access.models import AlbumAccess

from comments_likes.models import Comment

import os
from PIL import Image
from io import BytesIO
from django.core.files.images import ImageFile


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
        album_photos = Photo.objects.filter(album=album_id)
        displayed_photos = min(3, len(album_photos))
        rest = len(album_photos) - displayed_photos

        context['album'] = get_object_or_404(Album, pk=album_id)
        context['album_photos'] = album_photos[:displayed_photos]
        context['rest'] = rest
        return context

    def form_valid(self, form):
        album_id = self.kwargs['album_id']
        album = get_object_or_404(Album, pk=album_id)
        existing_photos = Photo.objects.filter(album=album)

        images = self.request.FILES.getlist('images')

        if not existing_photos.exists():
            first_image = images.pop(0)
            photo = Photo(album=album, image=first_image, is_default=True, uploaded_by=self.request.user)
            photo.save() #save the instance, applying resize from model save method
        for image in images:
            photo = Photo(album=album, image=image, uploaded_by=self.request.user)
            photo.save() #save the instance, applying resize from model save method

        messages.success(self.request, 'Photos were uploaded successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('albums:album_detail', kwargs={'pk': self.kwargs['album_id']})


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "photos/photo_edit.html"
    form_class = PhotoUpdateForm
    rotation_form_class = PhotoRotationForm

    def test_func(self):
        photo_id = self.kwargs['pk']
        photo = Photo.objects.get(id=photo_id)
        return self.request.user == (photo.album.creator or photo.uploaded_by) #only creator of album or photo uploader can edit it

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to edit this photo</h2>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo_id = self.kwargs['pk']
        photo = Photo.objects.get(id=photo_id)

        context['photo'] = photo
        context['photo_update_form'] = PhotoUpdateForm()
        context['rotation_form'] = self.rotation_form_class()

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        rotation_form = self.rotation_form_class(self.request.POST)

        if 'rotate' in request.POST:
            if rotation_form.is_valid():
                angle = rotation_form.cleaned_data['rotation_angle']
                photo = Photo.objects.get(pk=self.kwargs['pk'])

                image = Image.open(photo.image.path)
                rotated_image = image.rotate(angle, expand=True)
                rotated_image_io = BytesIO()
                rotated_image.save(rotated_image_io, format='JPEG')
                photo.image.save(
                    os.path.basename(photo.image.name),
                    ImageFile(rotated_image_io),
                    save=False
                )
                photo.save()
                return HttpResponseRedirect(request.path_info)

        elif form.is_valid():
            photo_id = self.kwargs['pk']
            new_photo = form.cleaned_data['upload_photo']
            if new_photo:
                old_photo = Photo.objects.get(pk=photo_id)
                old_photo.image.delete(save=False)

                old_photo.image = new_photo
                old_photo.save()

        return self.form_valid(form)

    def get_success_url(self):
        return reverse_lazy('photos:photo_edit', kwargs={'pk': self.kwargs['pk']})


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

        # we list the Album photo pk in order to know "where" the displayed photo is in the list
        album_id = Album.objects.get(photos_album=photo)
        album_photo_pk_list = [photo.pk for photo in Photo.objects.filter(album=album_id)]

        previous = next = None
        if len(album_photo_pk_list)==1: #if album contains 1 photo only
            previous = next = None
        elif album_photo_pk_list.index(photo.id) == 0:
            next = album_photo_pk_list[album_photo_pk_list.index(photo.id)+1]
        elif album_photo_pk_list.index(photo.id)+1 == len(album_photo_pk_list):
            previous = album_photo_pk_list[album_photo_pk_list.index(photo.id)-1]
        else:
            next = album_photo_pk_list[album_photo_pk_list.index(photo.id)+1]
            previous = album_photo_pk_list[album_photo_pk_list.index(photo.id)-1]

        context['previous'] = previous
        context['next'] = next
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
