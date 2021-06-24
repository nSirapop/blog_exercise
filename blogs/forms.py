# forms.py
from django import forms

from .models import Blog, Post

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title']
        labels = {'title': ''}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
        labels = {'title': 'Subject:', 'text': 'Content:'}