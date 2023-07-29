from django.contrib import admin

from .models import AlbumAccess, AlbumAccessRequest, RelationRequest, Relation
# Register your models here.

admin.site.register(AlbumAccess)
admin.site.register(AlbumAccessRequest)
admin.site.register(RelationRequest)
admin.site.register(Relation)
