from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__' #email, profile_picture, age, country, bio
        widgets = {
            'bio': forms.Textarea(attrs={'class':'textarea textarea-bordered'})
        }
