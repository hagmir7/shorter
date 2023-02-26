from django import forms
from .models import Post, Link
from django.utils.translation import gettext_lazy as _




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'description', 'tags', 'body', 'is_page')



class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('original', 'slug', 'custome')