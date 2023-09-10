from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .forms import CustomUserChangeForm, RegisterForm #CustomUserCreationForm
from .models import CustomUser, RelationRequest, Relation, Notification

from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    add_form = RegisterForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_picture', 'country', 'hide_connections', 'premium_member', 'photo_limit')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(RelationRequest)
admin.site.register(Relation)
admin.site.register(Notification)
