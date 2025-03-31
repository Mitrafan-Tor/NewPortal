from django import forms
from .models import Post, Comment


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'post_type', 'categories', 'author']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')