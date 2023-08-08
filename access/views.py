from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import AlbumAccess, Album
from accounts.models import CustomUser, Relation

from .forms import AlbumAccessGrantForm, AlbumAccessRevokeForm
from albums.forms import AlbumForm






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




# from django.views import View
# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseRedirect
# from .forms import AlbumAccessFormTest, AlbumAccessRevokeForm

# class AlbumAccessView(View):
#     template_name = 'access/test_access.html'

#     def get(self, request, pk):
#         album = get_object_or_404(Album, pk=pk)
#         existing_access = AlbumAccess.objects.filter(album=pk)
#         users_with_access = [access.user for access in existing_access]
#         users_id_with_access = [access.user.id for access in existing_access]

#         relations_to_album_creator = Relation.objects.filter(Q(user_sending__exact=album.creator) | Q(user_receiving__exact=album.creator))
#         # relations list contains all other users sharing a relation object with the creator of the album
#         relations = [relation.user_sending if relation.user_receiving == album.creator else relation.user_receiving for relation in relations_to_album_creator]

#         relations_dict = {}
#         for relation in relations_to_album_creator:
#             if relation.user_receiving == album.creator:
#                 relations_dict[relation.user_sending] = relation.relation_type
#             elif relation.user_sending == album.creator:
#                 relations_dict[relation.user_receiving] = relation.relation_type

#         add_access_form = AlbumAccessFormTest(queryset=CustomUser.objects.exclude(pk__in=users_id_with_access))
#         revoke_access_form = AlbumAccessRevokeForm(queryset=CustomUser.objects.filter(pk__in=users_id_with_access))

#         context = {
#             'album': album,
#             'existing_access': existing_access,
#             'relations': relations,
#             'relations_to_album_creator': relations_to_album_creator,
#             'relations_dict': relations_dict,
#             'users_with_access': users_with_access,
#             'add_access_form': add_access_form,
#             'revoke_access_form': revoke_access_form,
#         }

#         return render(request, self.template_name, context)

#     def post(self, request, pk):
#         album = get_object_or_404(Album, pk=pk)
#         existing_access = AlbumAccess.objects.filter(album=pk)
#         users_with_access = [access.user for access in existing_access]
#         users_id_with_access = [access.user.id for access in existing_access]

#         relations_to_album_creator = Relation.objects.filter(Q(user_sending__exact=album.creator) | Q(user_receiving__exact=album.creator))
#         # relations list contains all other users sharing a relation object with the creator of the album
#         relations = [relation.user_sending if relation.user_receiving == album.creator else relation.user_receiving for relation in relations_to_album_creator]

#         relations_dict = {}
#         for relation in relations_to_album_creator:
#             if relation.user_receiving == album.creator:
#                 relations_dict[relation.user_sending] = relation.relation_type
#             elif relation.user_sending == album.creator:
#                 relations_dict[relation.user_receiving] = relation.relation_type

#         add_access_form = AlbumAccessFormTest(queryset=CustomUser.objects.exclude(pk__in=users_id_with_access))
#         revoke_access_form = AlbumAccessRevokeForm(queryset=CustomUser.objects.filter(pk__in=users_id_with_access))

#         if 'add_access_form' in request.POST:
#             add_access_form = AlbumAccessFormTest(request.POST, queryset=CustomUser.objects.exclude(pk__in=users_id_with_access))
#             if add_access_form.is_valid():
#                 selected_users = add_access_form.cleaned_data['users_to_grant_access']
#                 for user in selected_users:
#                     AlbumAccess.objects.create(
#                         album=album,
#                         user=user,
#                     )
#                 # Redirect to the same page after processing the form
#                 return HttpResponseRedirect(request.path_info)

#         elif 'revoke_access_form' in request.POST:
#             revoke_access_form = AlbumAccessRevokeForm(request.POST, queryset=CustomUser.objects.filter(pk__in=users_id_with_access))
#             if revoke_access_form.is_valid():
#                 selected_users = revoke_access_form.cleaned_data['users_to_revoke_access']
#                 for user in selected_users:
#                     access_to_delete = AlbumAccess.objects.get(
#                         album=album,
#                         user=user,
#                     )
#                     access_to_delete.delete()
#                 # Redirect to the same page after processing the form
#                 return HttpResponseRedirect(request.path_info)

#         context = {
#             'album': album,
#             'existing_access': existing_access,
#             'relations': relations,
#             'relations_to_album_creator': relations_to_album_creator,
#             'relations_dict': relations_dict,
#             'users_with_access': users_with_access,
#             'add_access_form': add_access_form,
#             'revoke_access_form': revoke_access_form,
#         }

#         return render(request, self.template_name, context)
