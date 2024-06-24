from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document',)
        widgets = {
            'document': forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'id': 'customFile'}),
        }