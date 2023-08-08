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


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','date_of_birth','bio')
        input_class = 'w-full input input-bordered text-sm'
        textarea_class = 'w-full textarea textarea-bordered p-3 text-sm'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': input_class, 'placeholder':'First Name', 'id':'first_name'}),
            'last_name': forms.TextInput(attrs={'class': input_class, 'placeholder':'Last Name', 'id':'last_name'}),
            'email': forms.EmailInput(attrs={'class':input_class,'placeholder':'Email Adress', 'id':'email'}),
            'date_of_birth': forms.DateInput(attrs={'class': input_class, 'id':'date_of_birth','type':'date'}),
            'bio': forms.Textarea(attrs={'class':textarea_class, 'placeholder':'Bio','rows':8, 'id':'bio'})
        }
        # date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': input_class, 'id':'date_of_birth','type':'date'}))

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
