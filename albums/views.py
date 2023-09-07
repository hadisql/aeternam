from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render

from django.views.generic import CreateView, ListView, DeleteView, DetailView

from django.db.models import Count, Q

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Album
from .forms import AlbumForm
from photos.models import Photo
from .models import AlbumAccess

from django.contrib import messages #used in AlbumCreateView
from django.contrib.messages.views import SuccessMessageMixin # used in AlbumDeleteView

from .forms import AlbumAccessGrantForm, AlbumAccessRevokeForm
from accounts.models import CustomUser, Relation


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

        if len(images):
            first_image = images.pop(0)
            photo = Photo(album=album, image=first_image, is_default=True, uploaded_by=self.request.user)
            photo.save() #calls the customized save method (photo resize)

            for image in images:
                photo = Photo(album=album, image=image, uploaded_by=self.request.user)
                photo.save()

        if form.is_valid():
            if len(images)==1:
                messages.success(self.request, f'Album successfully created, with 1 photo')
            elif len(images)==0:
                messages.success(self.request, f'Empty album successfully created')
            else:
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
        default_photo = Photo.objects.filter(album=album, is_default=True).first()

        album_photos = Photo.objects.filter(album=album)
        displayed_photos = min(3, len(album_photos))
        rest = len(album_photos) - displayed_photos
        context['default_photo'] = default_photo
        context['album_photos'] = album_photos[:displayed_photos]
        context['rest'] = rest
        return context


# -----------------------------
# --------- ACCESS  -----------
# -----------------------------


@login_required
def album_access(request, pk):
    album = Album.objects.get(pk=pk)
    if request.user != album.creator:
        return HttpResponseForbidden("You don't have permission to access this page.")

    existing_access = AlbumAccess.objects.filter(album=pk)
    users_with_access = [access.user for access in existing_access]
    users_id_with_access = [access.user.id for access in existing_access]


    relations_to_album_creator = Relation.objects.filter(Q(user_sending__exact=album.creator) | Q(user_receiving__exact=album.creator))
    # relations list contains all other users sharing a relation object with the creator of the album
    relations = [relation.user_sending if relation.user_receiving == album.creator else relation.user_receiving for relation in relations_to_album_creator]

    relations_dict = {}
    for relation in relations_to_album_creator:
        if relation.user_receiving == album.creator:
            relations_dict[relation.user_sending] = relation.relation_type
        elif relation.user_sending == album.creator:
            relations_dict[relation.user_receiving] = relation.relation_type

    # GET
    album_form = AlbumForm(instance=album) #title and description update
    add_access_form = AlbumAccessGrantForm(queryset=CustomUser.objects.exclude(pk__in=users_id_with_access))
    revoke_access_form = AlbumAccessRevokeForm(queryset=CustomUser.objects.filter(pk__in=users_id_with_access))

    if 'album_form' in request.POST:
        album_form = AlbumForm(request.POST, instance=album)
        if album_form.is_valid():
            album_form.save()
            return HttpResponseRedirect(request.path_info)

    if 'add_access_form' in request.POST:
        add_access_form = AlbumAccessGrantForm(request.POST, queryset=CustomUser.objects.exclude(pk__in=users_id_with_access))
        if add_access_form.is_valid():
            selected_users = add_access_form.cleaned_data['users_to_grant_access']
            for user in selected_users:
                AlbumAccess.objects.create(
                    album=album,
                    user=user,
                )
        return HttpResponseRedirect(request.path_info)

    elif 'revoke_access_form' in request.POST:
        revoke_access_form = AlbumAccessRevokeForm(request.POST, queryset=CustomUser.objects.filter(pk__in=users_id_with_access))
        if revoke_access_form.is_valid():
            selected_users = revoke_access_form.cleaned_data['users_to_revoke_access']
            for user in selected_users:
                access_to_delete = AlbumAccess.objects.get(
                    album=album,
                    user=user,
                )
                access_to_delete.delete()
        return HttpResponseRedirect(request.path_info)

    context = {
        'album': album,
        'album_form':album_form,
        'existing_access': existing_access,
        'relations': relations,
        'relations_to_album_creator': relations_to_album_creator,
        'relations_dict': relations_dict,
        'users_with_access': users_with_access,
        'add_access_form': add_access_form,
        'revoke_access_form': revoke_access_form,
    }

    return render(request, 'access/album_access.html', context)
