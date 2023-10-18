from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import JsonResponse
from accounts.models import Notification, CustomUser
from photos.models import Photo, PhotoAccess
from albums.models import Album, AlbumAccess

from django.contrib import messages

def index(request):

    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('accounts:account_view', pk=request.user.pk) #forces to redirect to main page when user is authenticated

    return render(request, "core/index.html")


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

        print(f"you would like to grant {CustomUser.objects.get(id=relation_id)} access to photos: {selected_photos} from the album {album_id}")

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
            messages.success(request, f"You gave {user.get_full_name() or user.email} access to {len(access_to_add)} and revoked their access to {len(access_to_remove)}")
        elif len(access_to_add) and not len(access_to_remove):
            messages.success(request, f"You gave {user.get_full_name() or user.email} access to {len(access_to_add)} photos")
        else:
            messages.success(request, f"You revoked {user.get_full_name() or user.email} their access to {len(access_to_remove)} photos")

        if not PhotoAccess.objects.filter(user=user, photo__album=album_id):
            # no more photos with access for this album -> delete the album access
            albumaccess_to_delete = AlbumAccess.objects.filter(album=album_id, user=user)
            albumaccess_to_delete.delete()
            print(f'deleting album access for photo {photo_id} ')
            messages.success(request, f'{user.get_full_name() or user.email} won\'t have access to your album anymore')
        elif PhotoAccess.objects.filter(user=user, photo__album=album_id) and not AlbumAccess.objects.filter(album=album_id, user=user):
            # giving access to photos -> creates the album access if it didn't exist
            AlbumAccess.objects.create(album=album, user=user)
            print(f'creating album access for photo {photo_id} ')
            messages.success(request, f'{user.get_full_name() or user.email} can now access your album ({PhotoAccess.objects.filter(user=user, photo__album=album_id).count()} photos)')

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
