from django import forms
from .models import Wall, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Wall
        fields = ['title', 'text', 'photo', 'private']
        widgets = {'text': forms.Textarea(attrs={'cols': 50, 'rows': 5})}
        

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'private']
        