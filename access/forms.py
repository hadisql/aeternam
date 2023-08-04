from django import forms

from .models import AlbumAccess
from accounts.models import CustomUser


# class AlbumAccessForm(forms.ModelForm):
#     class Meta:
#         model = AlbumAccess
#         fields = ['user']

#     def __init__(self, *args, **kwargs):
#         # Get the relations_dict from the kwargs (passed from the view's get_context_data)
#         relations_ids = kwargs.pop('relations_ids', {})
#         super().__init__(*args, **kwargs)
#         # Filter the user choices based on the keys of the relations_dict
#         self.fields['user'].queryset = self.fields['user'].queryset.filter(id__in=relations_ids)


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
