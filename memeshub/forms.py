from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['caption', 'image']  # Include 'photo' field if needed
        labels = {'photo': ''}
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 4},)
        }
