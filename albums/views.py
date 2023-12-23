from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render, get_object_or_404

from django.views.generic import CreateView, ListView, DeleteView, DetailView

from django.db.models import Count, Sum, Case, When, IntegerField, Q

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Album
from .forms import AlbumForm, AlbumCreateForm
from photos.models import Photo, PhotoAccess
from .models import AlbumAccess

from django.contrib import messages #used in AlbumCreateView
from django.contrib.messages.views import SuccessMessageMixin # used in AlbumDeleteView

from .forms import AlbumAccessGrantForm, AlbumAccessRevokeForm
from accounts.models import CustomUser, Relation, Notification

from django.utils.translation import gettext_lazy as _

# ----------------------------
# ------ CREATE ALBUM --------
# ----------------------------


class AlbumCreateView(LoginRequiredMixin, CreateView):
    # -- template name is 'album_form.html'
    model = Album
    form_class = AlbumCreateForm
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
            PhotoAccess.objects.create(photo=photo, user=self.request.user)

            for image in images:
                total_photos = Photo.objects.filter(uploaded_by=self.request.user)
                if len(total_photos) < self.request.user.photo_limit:
                    print(f'len(total_photos): {len(total_photos)}, user photo limit: {self.request.user.photo_limit}')
                    photo = Photo(album=album, image=image, uploaded_by=self.request.user)
                    photo.save()
                    PhotoAccess.objects.create(photo=photo, user=self.request.user)
                else:
                    messages.error(self.request, f"You have reached your maximum amount of photos to upload: {self.request.user.photo_limit} photos")

        if form.is_valid():
            if len(images)==1:
                messages.success(self.request, f'Album successfully created, with 1 photo')
            elif len(images)==0 and not first_image:
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
        shared_albums = Album.objects.filter(album_accesses__user__exact=self.request.user) #'accesses' is the related name in the AlbumAccess model for the album FK

        # Annotate each album with the count of photos associated with it
        my_albums = my_albums.annotate(photo_count=Count('photos_album'))

        # the following line uses Sum, Case and When functions in order to retrieve the number of allowed photos in an album for the user, so he only sees the corresponding total photos per shared albums
        shared_albums = shared_albums.annotate(photo_count=Sum(Case(When(photos_album__accessed_photo__user=self.request.user,then=1),output_field=IntegerField())))

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
        context['photos'] = Photo.objects.filter(album=album_id).filter(accessed_photo__user=self.request.user) # the second filter makes sure the user can only see album details with photos he has access to

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
    success_message = _("Album was deleted successfully")

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
def album_access(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.user != album.creator:
        return HttpResponseForbidden("You don't have permission to access this page.")

    existing_access = AlbumAccess.objects.filter(album=album)
    users_with_access = [access.user for access in existing_access]

    relations_to_album_creator = Relation.objects.filter(Q(user_sending__exact=album.creator) | Q(user_receiving__exact=album.creator))
    # Relations list contains all other users sharing a relation object with the creator of the album
    relations = [relation.user_sending if relation.user_receiving == album.creator else relation.user_receiving for relation in relations_to_album_creator]

    default_photo = Photo.objects.filter(album=album, is_default=True).first()
    photos_in_album = Photo.objects.filter(album=album)
    photo_count = photos_in_album.count()

    # (keys,values) : (related users , number of allowed photos in album)
    relations_dict = {}
    for relation in relations:
        relations_dict[relation] = Photo.objects.filter(album=album).filter(accessed_photo__user__in=[relation])

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()

            # # Process album access updates
            # for relation in relations:
            #     checkbox_name = f'user_{relation.id}'
            #     if checkbox_name in request.POST:
            #         if not AlbumAccess.objects.filter(album=album, user=relation).exists():
            #             AlbumAccess.objects.create(album=album, user=relation)
            #             messages.success(request, f'{relation.get_full_name() or relation.email} has now access to your album')
            #     else:
            #         access_to_delete = AlbumAccess.objects.filter(album=album, user=relation)
            #         photo_accesses = PhotoAccess.objects.filter(photo__album=album, user=relation)
            #         if access_to_delete:
            #             related_notifications = Notification.objects.filter(user_from=request.user, content_type=ContentType.objects.get_for_model(AlbumAccess), object_id=access_to_delete.first().id)
            #             print(f'related notifications to delete : {related_notifications}')
            #             if related_notifications:
            #                 for notification in related_notifications:
            #                     notification.delete()
            #             access_to_delete.delete()
            #             for photo_access in photo_accesses:
            #                 photo_access.delete()
            #                 print(f'access {photo_access} revoked for user {relation}')
            #             messages.info(request, f'{relation.get_full_name() or relation.email} access has been revoked')
            #             print(f'album access for user {relation.get_full_name()} was deleted')


    else:
        form = AlbumForm(instance=album)

    context = {
        'album': album,
        'existing_access': existing_access,
        'relations': relations,
        'relations_to_album_creator': relations_to_album_creator,
        'users_with_access': users_with_access,
        'form': form,
        'default_photo': default_photo,
        'photo_count': photo_count,
        'relations_dict': relations_dict,
        'photos_in_album': photos_in_album,
        'modal_num_photos_to_show': 6,
    }

    if request.POST:
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'albums/album_access.html', context)
