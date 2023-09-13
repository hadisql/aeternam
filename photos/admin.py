from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html

from .models import Photo


class PhotoAdmin(AdminImageMixin, admin.ModelAdmin):
    #https://stackoverflow.com/questions/1385094/django-admin-and-showing-thumbnail-images?rq=3
    def image_thumbnail(self, obj):
        if obj.image:
            t = get_thumbnail(obj.image, "50x50", crop='center', quality=99)
            return format_html('<img src="%s"/>' % t.url)
        else:
            return u'profile_image'

    image_thumbnail.short_description = 'photo thumbnail'

    list_display = ('id','album', 'image_thumbnail')




admin.site.register(Photo, PhotoAdmin)
