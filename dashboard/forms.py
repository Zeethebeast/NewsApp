from django import forms
from absotv.models import Post

class PostForn(forms.ModelForm):
    Class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'category', 'plublished']