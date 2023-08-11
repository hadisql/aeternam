from django import forms

from comments_likes.models import Comment

class PhotoForm(forms.Form):
    pass

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'textarea textarea-primary textarea-sm w-full max-w-lg', 'placeholder': 'Send a comment..','rows':2})
            }
