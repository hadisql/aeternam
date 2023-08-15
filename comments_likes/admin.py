from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','body','created','updated','active')
    list_filter = ('author','active','created','updated','active')
    search_fields = ('body', 'author','active')
    actions = ['disapprove_comments']

    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
