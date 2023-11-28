from django import forms

from django.utils.translation import gettext_lazy as _

class FeedbackForm(forms.Form):
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'class':'w-full textarea textarea-bordered text-sm',
                                     'placeholder':_('Give a feedback and/or ideas..'),
                                     'rows':'4'}),
        required=True,
        label=""
    )
