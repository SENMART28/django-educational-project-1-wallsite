from django import forms
from .models import Wall
from django.core.exceptions import ValidationError


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Wall
        fields = ['title', 'text', 'private']
        widgets = {'text': forms.Textarea(attrs={'cols': 50, 'rows': 5})}
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Длина больше 100 символов')
        return title
    
    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) > 500:
            raise ValidationError('Длина больше 500 символов')
        return text
        