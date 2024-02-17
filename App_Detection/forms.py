from django import forms
from .models import TestMedia

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = TestMedia 
        fields = ['file']

