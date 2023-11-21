from django import forms

from comments_likes.models import Comment
from .models import Photo

from django.utils.translation import gettext_lazy as _

class PhotoForm(forms.Form):
    pass

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'textarea textarea-sm textarea-bordered',
                                        'placeholder': _('Send a comment..'),'rows':2,
                                        'x-data':'{ resize () { $el.style.height = "0px"; $el.style.height = $el.scrollHeight + "px" } }',
                                        'x-init':'resize()',
                                        '@input':'resize()',
                                        'type':'text',
                                        })
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
        widget=forms.CheckboxInput(attrs={'class':'hidden peer',
                                          'id':'choose-as-default',
                                          'name':'choose-as-default',
                                          'type':'checkbox'}),
        required=False
    )

class PhotoDescriptionForm(forms.Form):
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class':'block px-2.5 pb-2.5 pt-4 bg-base-200 w-full text-sm rounded-lg border-1 border-base-300 appearance-none dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                                     'rows':2,
                                     'id':'photo_description',
                                     'placeholder':'',
                                     'x-data':'{ resize () { $el.style.height = "0px"; $el.style.height = $el.scrollHeight + "px" } }',
                                     'x-init':'resize()',
                                     '@input':'resize()',
                                     'type':'text',
                                     }),
        required=False
    )

# class PhotoRotationForm(forms.Form):
#     rotation_angle = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'rotation-angle'}), initial=0)
