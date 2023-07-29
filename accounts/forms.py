from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

from .models import CustomUser, RelationRequest


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

class RelationRequestForm(forms.Form):
    pass

class RelationAcceptForm(forms.Form):
    relation_type = forms.ChoiceField(choices=RelationRequest.RELATION_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial value for the relation_type field
        self.fields['relation_type'].initial = 'UNDEFINED'

class RelationRequestUndoForm(forms.Form):
    pass

class RelationDeleteForm(forms.Form):
    pass
