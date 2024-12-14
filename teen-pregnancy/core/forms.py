# core/forms.py

from django import forms
from .models import Resource, ForumPost, Comment, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User




# Form for submitting a new resource
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'category', 'content']

# Form for submitting a new forum post
class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category']

# core/forms.py
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']    

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

# Form for user registration
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Form for user login
class LoginForm(AuthenticationForm):
    pass