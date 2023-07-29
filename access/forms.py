from django import forms

from .models import RelationRequest

class AlbumAccessRequestForm(forms.Form):
    pass

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
