from .models import Comment
from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['caption', 'file']  # Include 'photo' field if needed
        labels = {'photo': ''}
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 4},),
            'file': forms.FileInput(attrs={'accept':'.png, .jpeg, .jpg, .mp4, .mkv, .webm, .avi, .mov, .gif'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 30,
                'rows': 4,
                'placeholder': 'Add your comment here',
            }),
            'parent': forms.HiddenInput()
        }
#regular form
"""class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'cols': 30,
        'rows': 4,
        'placeholder': 'Add your comment here'
    }))"""
