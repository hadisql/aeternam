from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, RelationRequest, Relation

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


class CustomProfilePicWidget(forms.widgets.ClearableFileInput):
    template_name = "accounts/custom_widget.html"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','date_of_birth','profile_picture', 'hide_connections')
        input_class = 'w-full input input-bordered text-sm'
        textarea_class = 'w-full textarea textarea-bordered p-3 text-sm'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': input_class, 'placeholder':_('First Name'), 'id':'first_name'}),
            'last_name': forms.TextInput(attrs={'class': input_class, 'placeholder':_('Last Name'), 'id':'last_name'}),
            'email': forms.EmailInput(attrs={'class':input_class,'placeholder':_('Email Adress'), 'id':'email'}),
            'date_of_birth': forms.DateInput(attrs={'class': input_class, 'id':'date_of_birth','type':'date'}),
            'profile_picture': CustomProfilePicWidget(),
            'hide_connections': forms.CheckboxInput(attrs={'class':'toggle toggle-error'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.hide_connections:
            self.fields['hide_connections'].initial = True
        else:
            self.fields['hide_connections'].initial = False


class RelationRequestForm(forms.Form):
    pass

class RelationAcceptForm(forms.Form):
    relation_type = forms.ChoiceField(choices=RelationRequest.RELATION_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial value for the relation_type field
        self.fields['relation_type'].initial = _('UNDEFINED')

class RelationRequestUndoForm(forms.Form):
    pass

class RelationDeleteForm(forms.Form):
    pass

class RelationChangeForm(forms.Form):
    change_relation = forms.ChoiceField(choices=Relation.RELATION_CHOICES, required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Set the initial value for the relation_type field
    #     self.fields['change_relation'].initial = 'UNDEFINED'
