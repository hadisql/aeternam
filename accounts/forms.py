from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

from .models import CustomUser, RelationRequest

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',)

    input_class = 'mt-1 w-full input input-bordered shadow-sm'

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': input_class, 'id':'FirstName'}), required=False)

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': input_class, 'id':'LastName'}), required=False)

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': input_class, 'id':'Email', 'name':'email',}),
        required=True)

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':input_class, 'id':'Password'}))

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':input_class, 'id':'PasswordConfirmation'}))


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
