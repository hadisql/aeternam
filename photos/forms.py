from django import forms

from comments_likes.models import Comment
from .models import Photo

class PhotoForm(forms.Form):
    pass

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'textarea textarea-sm textarea-bordered', 'placeholder': 'Send a comment..','rows':2})
            }

class PhotoUpdateForm(forms.Form):
    upload_photo = forms.ImageField(
        label="",
        widget=forms.FileInput(attrs={'class':'file-input file-input-sm w-full'}),
        required=False)

    rotation_angle = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id':'rotation-angle'}),
        initial=0,
        required=False)

    mirror_flip = forms.BooleanField(
        widget=forms.HiddenInput(attrs={'id':'mirror-flip'}),
        initial=False,
        required=False)

    set_as_default_photo = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class':'toggle toggle-info', 'id':'choose-as-default'}),
        required=False
    )

class PhotoDescriptionForm(forms.Form):
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class':'textarea textarea-bordered', 'rows':2, 'id':'photo_description', 'placeholder':'Add a photo description..'}),
        required=False
    )

# class PhotoRotationForm(forms.Form):
#     rotation_angle = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'rotation-angle'}), initial=0)
