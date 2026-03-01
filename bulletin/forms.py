from django import forms
from .models import Bulletin, Response

class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ['title', 'content', 'category']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'category': 'Категория',
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        labels = {
            'text': 'Ваш отклик'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите ваш отклик...'})
        }