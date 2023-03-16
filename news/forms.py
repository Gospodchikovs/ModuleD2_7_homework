from django.forms import ModelForm
from .models import Post
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django import forms
from allauth.account.forms import SignupForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'category', 'heading', 'body']


class ProfileEditForm(ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    username = forms.CharField(label="Логин")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
