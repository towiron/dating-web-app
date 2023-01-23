from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Создание формы UserUpdateForm для обновления имени пользователя и электронной почты
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

# Создание формы ProfileUpdateForm для добавление/обноваление данных
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'first_name', 'last_name', 'banner', 'age', 'sex', 'seeking', 'about', 'city', 'online_status']