from unicodedata import name
from django import forms
from django.forms import ModelForm, Select, TimeInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Account

class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]

class UserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['name', 'phone']

class UserSettingsForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['timezone', 'wake_up_time', 'bedtime']
        labels = {
            'timezone': 'Timezone',
            'wake_up_time': 'Wake Up Time',
            'bedtime': 'Bedtime'
        }
        timezones = [('America/Chicago', 'America/Chicago'), ('America/New_York', 'America/New York'),
                    ('America/Denver', 'America/Denver'), ('America/Los_Angeles', 'America/Los Angeles')]
        widgets = {
            'timezone': Select(choices=timezones),
            'wake_up_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'bedtime': TimeInput(attrs={'type': 'time'}, format="%H:%M")
        }

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.fields['wake_up_time'].input_formats = ('%-H:$M',)