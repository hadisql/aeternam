from django import forms

from .models import Album, AlbumAccess
from accounts.models import CustomUser


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class':'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows':4}),
        }


class AlbumAccessGrantForm(forms.Form):
    users_to_grant_access = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),  # We will populate this dynamically in the view
        widget=forms.CheckboxSelectMultiple,
    )
    def __init__(self, *args, queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if queryset is not None:
            self.fields['users_to_grant_access'].queryset = queryset


class AlbumAccessRevokeForm(forms.Form):
    users_to_revoke_access = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),  # We will populate this dynamically in the view
        widget=forms.CheckboxSelectMultiple,
    )
    def __init__(self, *args, queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if queryset is not None:
            self.fields['users_to_revoke_access'].queryset = queryset
