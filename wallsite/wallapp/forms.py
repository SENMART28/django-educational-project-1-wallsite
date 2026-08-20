from django import forms
from .models import Wall
from django.core.exceptions import ValidationError


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Wall
        fields = ['title', 'text', 'private']
        widgets = {'text': forms.Textarea(attrs={'cols': 50, 'rows': 5})}
        