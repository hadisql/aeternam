from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
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


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password','new_password1','new_password2')

    input_class = 'w-full input input-bordered text-sm'
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':input_class, 'placeholder':_('Old password')}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':input_class, 'placeholder':_('New password')}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':input_class, 'placeholder':_('Confirm new password')}))

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import unicodedata

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'class':'w-full input input-bordered text-sm',
                                       'placeholder':'Email'}))
    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        self.users_cache = CustomUser.objects.filter(
            email__iexact=email,
            is_active=True,
        )
        if not len(self.users_cache):
            raise forms.ValidationError(_("The provided email address does not match any user account."))
        return email

    def get_users(self, email):
        """
        Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = CustomUser.get_email_field_name()
        active_users = CustomUser._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = CustomUser.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )

class CustomSetPasswordForm(SetPasswordForm):
    input_class = 'w-full input input-bordered text-sm'
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': input_class, 'placeholder':_('Enter new password')}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': input_class, 'placeholder':_('Confirm new password')}),
    )

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
