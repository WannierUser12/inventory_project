from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DocumentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(DocumentForm, self).save(commit=False)
        if self.user:
            instance.description = self.user.username
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Document
        fields = ('description', 'document',)
        widgets = {
            'description': forms.TextInput(attrs={'readonly': 'readonly'}),
            'document': forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'id': 'customFile'}),
            }
