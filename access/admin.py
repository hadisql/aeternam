from django.contrib import admin

from .models import AlbumAccess, AlbumAccessRequest
# Register your models here.

admin.site.register(AlbumAccess)
admin.site.register(AlbumAccessRequest)
