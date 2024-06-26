from django import forms

from .models import Album, AlbumAccess
from accounts.models import CustomUser

from django.utils.translation import gettext_lazy as _

class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class':'input input-sm input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full',
                                                'placeholder': _('Add a description for this album'),
                                                'rows':3,
                                                'oninput':'showSaveButton()',
                                                'x-data':'{ resize () { $el.style.height = "0px"; $el.style.height = $el.scrollHeight + "px" } }',
                                                'x-init':'resize()',
                                                '@input':'resize()',
                                                'type':'text',}),
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class':'input input-sm input-bordered w-full', 'oninput':'showSaveButton()'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full',
                                                'placeholder': _('Add a description for this album'),
                                                'rows':3,
                                                'oninput':'showSaveButton()',
                                                'x-data':'{ resize () { $el.style.height = "0px"; $el.style.height = $el.scrollHeight + "px" } }',
                                                'x-init':'resize()',
                                                '@input':'resize()',
                                                'type':'text',}),
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
