
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, DetailView
from django.views.generic.edit import FormView

from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages #used in add_photos_to_album
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Photo
from .forms import PhotoForm, CommentForm, PhotoUpdateForm, PhotoDescriptionForm

from albums.models import Album, AlbumAccess

from comments_likes.models import Comment

import os
from PIL import Image, ImageOps
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
        total_photos = Photo.objects.filter(uploaded_by=self.request.user)

        images = self.request.FILES.getlist('images')

        if len(total_photos) < self.request.user.photo_limit:
            if not existing_photos.exists():
                first_image = images.pop(0)
                photo = Photo(album=album, image=first_image, is_default=True, uploaded_by=self.request.user)
                photo.save() #save the instance, applying resize from model save method

            for image in images:
                total_photos = Photo.objects.filter(uploaded_by=self.request.user) # refresh the number for each iteration
                photo = Photo(album=album, image=image, uploaded_by=self.request.user)
                photo.save() #save the instance, applying resize from model save method
                total_photos = Photo.objects.filter(uploaded_by=self.request.user) # refresh the number for each iteration
                if len(total_photos) == int(.8 * self.request.user.photo_limit):
                    messages.warning(self.request, f"You've reached 80% of your maximum photo upload limit")

            if len(images)<=1:
                # if you add 1 photo to an empty album -> the list length is 0 because of the default_photo pop(0) treatment
                messages.success(self.request, '1 photo was uploaded successfully')
            else:
                messages.success(self.request, f'{len(images)} photos were uploaded successfully')
        else:
            messages.error(self.request, f"You have reached your maximum amount of photos to upload: {self.request.user.photo_limit} photos")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('albums:album_detail', kwargs={'pk': self.kwargs['album_id']})


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "photos/photo_edit.html"
    form_class = PhotoUpdateForm
    form_description_form = PhotoDescriptionForm

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

        photo_description = photo.description
        form_description = PhotoDescriptionForm(initial={'description': photo_description})

        context['photo'] = photo
        context['photo_update_form'] = PhotoUpdateForm()
        context['form_description_form'] = form_description

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        description_form = self.form_description_form(data=self.request.POST)

        photo_id = self.kwargs['pk']
        photo = Photo.objects.get(pk=photo_id)

        if description_form.is_valid():
            if description_form.has_changed():
                new_description = description_form.cleaned_data['description']
                photo.description = new_description
                photo.save()

        if form.is_valid():
            rotation_angle = form.cleaned_data['rotation_angle']
            new_photo = form.cleaned_data['upload_photo']
            mirror_flip = form.cleaned_data['mirror_flip']

            if new_photo:
                if photo.uploaded_by == self.request.user:
                    old_photo = Photo.objects.get(pk=photo_id)
                    old_photo.image.delete(save=False)

                    old_photo.image = new_photo
                    old_photo.save()

            elif rotation_angle or mirror_flip:
                if photo.uploaded_by == self.request.user:
                    if rotation_angle:
                        image = Image.open(photo.image.path)
                        rotated_image = image.rotate(-rotation_angle, expand=True)
                        rotated_image_io = BytesIO()
                        rotated_image.save(rotated_image_io, format='JPEG')
                        photo.image.save(
                            os.path.basename(photo.image.name),
                            ImageFile(rotated_image_io),
                            save=False
                        )
                        photo.save()
                        #return HttpResponseRedirect(request.path_info)
                    if mirror_flip:
                        image = Image.open(photo.image.path)
                        flipped_image = ImageOps.mirror(image)
                        flipped_image_io = BytesIO()
                        flipped_image.save(flipped_image_io, format='JPEG')
                        photo.image.save(
                            os.path.basename(photo.image.name),
                            ImageFile(flipped_image_io),
                            save=False
                        )
                        photo.save()

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
        comments_from_user = comments.filter(author=self.request.user)
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
        context['comments_from_user'] = comments_from_user
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

        # Comment deletion
        comments = Comment.objects.filter(commented_photo=photo)
        comments_from_user = comments.filter(author=self.request.user)
        for comment in comments_from_user:
            delete_comment_key = f"delete_comment_{comment.id}"
            if delete_comment_key in request.POST:
                comment.delete()
                return HttpResponseRedirect(request.path_info)

        return redirect('photos:photo_detail', pk=photo_id)
        # return HttpResponseRedirect(request.path_info)

# -----------------------------
# --------- DELETE  -----------
# -----------------------------

import sorl.thumbnail

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
        sorl.thumbnail.delete(self.object)
        return HttpResponseRedirect(success_url)
