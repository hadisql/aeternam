from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from django.views.generic import CreateView, ListView, DeleteView, DetailView

from django.db.models import Count

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Album
from .forms import AlbumForm
from photos.models import Photo
from access.models import AlbumAccess

from django.contrib import messages #used in AlbumCreateView
from django.contrib.messages.views import SuccessMessageMixin # used in AlbumDeleteView


# ----------------------------
# ------ CREATE ALBUM --------
# ----------------------------


class AlbumCreateView(LoginRequiredMixin, CreateView):
    # -- template name is 'album_form.html'
    model = Album
    form_class = AlbumForm
    # success_url = reverse_lazy('albums:albums_view')
    # "redirect" didn't work : The reverse_lazy function is used to lazily reverse the URL, ensuring that it's only evaluated when the view is executed.

    def form_valid(self, form):
        album = form.save(commit=False)
        album.creator = self.request.user
        album.save()

        # Save associated photos to the album
        images = self.request.FILES.getlist('images')

        first_image = images.pop(0)
        photo = Photo(album=album, image=first_image, is_default=True, uploaded_by=self.request.user)
        photo.save() #calls the customized save method (photo resize)

        for image in images:
            photo = Photo(album=album, image=image, uploaded_by=self.request.user)
            photo.save()

        if form.is_valid():
            messages.success(self.request, f'Album successfully created, with {len(images)+1} photos')
            return redirect('albums:album_detail', album.id)

        return super().form_valid(form)

# ----------------------------
# ------ LIST ALBUMS ---------
# ----------------------------
class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'albums/albums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # retrieving albums specific to the creator of the albums
        my_albums = Album.objects.filter(creator=self.request.user)
        shared_albums = Album.objects.filter(accesses__user__exact=self.request.user) #'accesses' is the related name in the AlbumAccess model for the album FK

        # Annotate each album with the count of photos associated with it
        my_albums = my_albums.annotate(photo_count=Count('photos_album'))
        shared_albums = shared_albums.annotate(photo_count=Count('photos_album'))

        # Create a dictionary to hold album objects and their default photos
        albums_with_default_photos = {}
        number_of_access = []

        for album in my_albums:
            # we save the number of users having access to the album -> if 0, no access was given
            number_of_access.append(len(AlbumAccess.objects.filter(album=album)))

            default_photo = album.photos_album.filter(is_default=True).first()
            if default_photo:
                albums_with_default_photos[album] = default_photo
            else:
                albums_with_default_photos[album] = False

        shared_albums_with_default_photos = {}
        for album in shared_albums:
            default_photo = album.photos_album.filter(is_default=True).first()
            if default_photo:
                shared_albums_with_default_photos[album] = default_photo
            else:
                shared_albums_with_default_photos[album] = False


        context['number_of_access'] = number_of_access
        context['albums_with_default_photos'] = albums_with_default_photos
        context['shared_albums_with_default_photos'] = shared_albums_with_default_photos

        return context


# ----------------------------
# ------ UPDATE ALBUM --------
# ----------------------------

# -----> defined in "album_access" function view, in accounts app

# class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     # -- template name is 'album_form.html'
#     model = Album
#     form_class = AlbumForm

#     def test_func(self):
#         album_id = self.kwargs['pk']
#         album = Album.objects.get(id=album_id)
#         return self.request.user == album.creator  # Check if the logged-in user owns the album

#     def handle_no_permission(self):
#         return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")


#     def get_success_url(self) -> str:
#         return reverse('albums:album_detail', kwargs={'pk': self.kwargs['pk']})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['type_of_view'] = 'update'
#         album_id = self.kwargs['pk']
#         context['photos'] = Photo.objects.filter(album=album_id)
#         return context


# ----------------------------
# --------- DETAIL  ----------
# ----------------------------
class AlbumDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Album
    template_name = "albums/album_detail.html"

    def test_func(self):
        album_id = self.kwargs['pk']
        album = Album.objects.get(id=album_id)
        has_access = AlbumAccess.objects.filter(album=album, user=self.request.user)
        return self.request.user == album.creator or has_access  # Check if the logged-in user owns the album or has access to it

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_id = self.kwargs['pk']
        context['photos'] = Photo.objects.filter(album=album_id)

        album_accesses = AlbumAccess.objects.filter(album=album_id) #all users concerned
        users_with_access = [album_access.user for album_access in album_accesses]
        context['users_with_access'] = users_with_access
        context['avatar_show_number'] = 3

        success_message = self.request.GET.get('success_message')
        if success_message:
            context['success_message'] = success_message

        return context


# -----------------------------
# --------- DELETE  -----------
# -----------------------------
class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Album
    fields = '__all__'
    success_url = reverse_lazy('albums:albums_view')
    context_object_name = 'album'
    success_message = "Album was deleted successfully"

    def test_func(self):
        album_id = self.kwargs['pk']
        album = Album.objects.get(id=album_id)
        return self.request.user == album.creator  # Check if the logged-in user owns the album

    def handle_no_permission(self):
        return HttpResponseForbidden("<h2>You don't have permission to view this page.</h2>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_id = self.kwargs['pk']
        album = Album.objects.get(id=album_id)
        default_photo = Photo.objects.get(album=album, is_default=True)

        album_photos = Photo.objects.filter(album=album)
        displayed_photos = min(3, len(album_photos))
        rest = len(album_photos) - displayed_photos
        context['default_photo'] = default_photo
        context['album_photos'] = album_photos[:displayed_photos]
        context['rest'] = rest
        return context
