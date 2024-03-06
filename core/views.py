from typing import Any
from django.shortcuts import render, redirect

from django.http import HttpRequest, HttpResponse, JsonResponse
from accounts.models import Notification, CustomUser, create_notification, mark_notification_as_read
from django.contrib.contenttypes.models import ContentType

from photos.models import Photo, PhotoAccess
from albums.models import Album, AlbumAccess

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from django.views.generic import FormView
from .forms import FeedbackForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import Feedback

def index(request):

    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('accounts:account_view', pk=request.user.pk) #forces to redirect to main page when user is authenticated

    return render(request, "core/index.html")

class AboutView(FormView):
    template_name = 'core/about.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('core:about')  # Redirect to the same page after successful form submission

    def form_valid(self, form):
        # Save feedback to Feedback model
        feedback_instance = Feedback(
            user = self.request.user,
            feedback = form.cleaned_data['feedback']
        )
        feedback_instance.save()

        messages.success(self.request, _("Your feedback has been successfully.\nThank you! =)"))

        # Send email
        # subject = 'New Feedback from {}'.format(self.request.user.email)
        # message = 'Name: {}\nFeedback: {}'.format(
        #     self.request.user.get_full_name(),
        #     form.cleaned_data['feedback'],
        # )
        # from_email = 'yourwebsite@example.com'  # Replace with your website's email
        # to_email = 'hadi.sqalli@laplateforme.io'  # Replace with your personal email
        # send_mail(subject, message, from_email, [to_email])

        return super().form_valid(form)


def clear_notif_from_navbar(request, notification_id):
    if request.user.is_authenticated:
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'message': 'Notification marked as read'})
        except Notification.DoesNotExist:
            return JsonResponse({'message': 'Notification not found'}, status=404)
    else:
        return JsonResponse({'message': 'Authentication required'}, status=401)

def photo_access_manager(request):
    if request.method == 'POST' and request.user.is_authenticated:
        import json
        data = json.loads(request.body)
        relation_id = data['relationId']
        selected_photos = data['selectedPhotos']
        album_id = data['albumId']

        user = CustomUser.objects.get(id=relation_id)
        album = Album.objects.get(id=album_id)

        print(f"you would like to grant {user} access to photos: {selected_photos} from the album {album_id}")

        # For selected_photos -> update PhotoAccess objects accordingly
        access_to_add, access_to_remove = update_photo_access(selected_photos, album_id, relation_id)

        for photo_id in access_to_add:
            photo = Photo.objects.get(id=photo_id)
            PhotoAccess.objects.create(photo=photo, user=user)
            print(f'creating photo access for photo {photo_id} ')

        for photo_id in access_to_remove:
            photo = Photo.objects.get(id=photo_id)
            p_to_remove = PhotoAccess.objects.filter(photo=photo, user=user)
            print(f'deleting photo access for photo {photo_id} ')
            p_to_remove.delete()

        if len(access_to_add) and len(access_to_remove):
            messages.success(request, _("You gave {username} access to {add} and revoked their access to {revoke}").format(username=(user.get_full_name() or user.email), add=len(access_to_add), revoke=len(access_to_remove)) )
            create_notification(user=user, user_from=request.user, content_type=ContentType.objects.get_for_model(Album), object_id=album.id, message=f"{request.user.get_full_name() or request.user.email} gave you access to {len(access_to_add)} photos", title="Photo access")
            # we change the default 'identifier' in order for it to contain the photos information
            notif_to_update = Notification.objects.last()
            notif_to_update.identifier += '-photos:' + '+'.join(str(access_to_add))
            notif_to_update.save()
            # we check if the photos revoked have a notification associated with them
            notif_to_delete = Notification.objects.filter(identifier=f"album{album_id}-{user.id}-photos:{'+'.join(str(access_to_remove))}")
            if notif_to_delete:
                notif_to_delete.delete()
        elif len(access_to_add) and not len(access_to_remove):
            messages.success(request, _("You gave {username} access to {number} photos").format(username=(user.get_full_name() or user.email), number=len(access_to_add)) )
            create_notification(user=user, user_from=request.user, content_type=ContentType.objects.get_for_model(Album), object_id=album.id, message=f"{request.user.get_full_name() or request.user.email} gave you access to {len(access_to_add)} photos", title="Photo access")
            notif_to_update = Notification.objects.last()
            notif_to_update.identifier += '-photos:' + '+'.join(str(access_to_add))
            notif_to_update.save()
        else:
            message = _("You revoked {username} their access to {number} photos").format(username=(user.get_full_name() or user.email), number=len(access_to_remove))
            messages.success(request, message)
            # we check if the photos revoked have a notification associated with them
            notif_to_delete = Notification.objects.filter(identifier=f"album{album_id}-{user.id}-photos:{'+'.join(str(access_to_remove))}")
            if notif_to_delete:
                notif_to_delete.delete()

        if not PhotoAccess.objects.filter(user=user, photo__album=album_id):
            # no more photos with access for this album -> delete the album access
            albumaccess_to_delete = AlbumAccess.objects.filter(album=album_id, user=user)
            albumaccess_to_delete.delete()
            print(f'deleting album access for photo {photo_id} ')
            messages.success(request, _('{} won\'t have access to your album anymore').format(user.get_full_name() or user.email))
            # if their was photoaccess notifications for this album, delete them
            notif_to_delete = Notification.objects.filter(identifier__contains=f"album{album_id}-{user.id}")
            if notif_to_delete:
                notif_to_delete.delete()
        elif PhotoAccess.objects.filter(user=user, photo__album=album_id) and not AlbumAccess.objects.filter(album=album_id, user=user):
            # giving access to photos -> creates the album access if it didn't exist
            AlbumAccess.objects.create(album=album, user=user)
            print(f'creating album access for photo {photo_id} ')
            messages.success(request, _('{username} can now access your album ({number} photos)').format(username=(user.get_full_name() or user.email), number=PhotoAccess.objects.filter(user=user, photo__album=album_id).count()))

        return JsonResponse({'message': 'Success'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)


# CREER UNE FONCTION QUI VA GERER CE QUE FAIT photo_access_manager:
# - on reçoit une liste de checkbox:
#   - on regarde l'état des accès initialement : intersection des listes -> on obtient deux listes
#   - liste 1 : accès à retirer / liste 2 : accès à donner

def update_photo_access(selected_photos, album_id, user_id):
    initial_photo_access = Photo.objects.filter(album=album_id).filter(accessed_photo__user__id=user_id) # queryset of initial accessible photos
    initial_photo_id_list = [str(photo.id) for photo in initial_photo_access]

    access_to_add = list(set(selected_photos) - set(initial_photo_id_list))
    access_to_remove = list(set(initial_photo_id_list) - set(selected_photos))

    return access_to_add, access_to_remove



#######################
#######  DEMO  ########
#######################

from django.contrib.auth import authenticate, login, logout
import os
from django.conf import settings

def listdir_nohidden(path):
    # equivalent to listdir but without hidden files
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def get_demo(request):
    # Generate fake data
    # Create a temporary fake user account
    fake_user = CustomUser.objects.create_user(email='demo@example.com', password='password123')
    print(f'created fake user : {fake_user.email} with password {fake_user.password}')

    # Path to the directory containing fake albums
    fake_albums_dir = os.path.join(settings.MEDIA_ROOT, 'fake_albums')

    # Iterate over subdirectories (albums)
    for album_name in listdir_nohidden(fake_albums_dir):
        album_path = os.path.join(fake_albums_dir, album_name)
        if os.path.isdir(album_path):
            album = Album.objects.create(creator=fake_user, title=album_name)
            # Iterate over files (photos) in the album directory
            for filename in listdir_nohidden(album_path):
                if os.path.isfile(os.path.join(album_path, filename)):
                    # Create photo object for each file
                    photo = Photo.objects.create(album=album, image=os.path.join('fake_albums', album_name, filename), uploaded_by=fake_user)

    # Authenticate the user
    user = authenticate(request, email='demo@example.com', password='password123')
    if user is not None:
        # Log the user in
        login(request, user)
        # Redirect to the appropriate page
        return redirect('accounts:account_view', pk=request.user.pk)
    else:
        # Handle authentication failure
        return redirect('core:index')

def logout_demo(request):
    # Log out the user
    logout(request)
    # Redirect to the welcome page or another appropriate page
    return redirect('core:index')
