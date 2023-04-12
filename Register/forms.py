from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from captcha.fields import CaptchaField

from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.exclude(name__exact='moderator'), required=True)
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username', 'email', 'group', 'captcha', 'password1', 'password2']



        