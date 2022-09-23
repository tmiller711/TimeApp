from unicodedata import name
from django import forms
from django.forms import ModelForm, Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone', 'timezone']
        timezones = [('America/Chicago', 'America/Chicago'), ('America/New_York', 'America/New_York')]
        widgets = {
            'timezone': Select(choices=timezones)
        }