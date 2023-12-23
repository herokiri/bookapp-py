# Ваш файл forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Author, Publisher, Book, Genre


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'middle_name']


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']


class BookForm(forms.ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = Book
        # Включаем все поля с модели в форму
        fields = '__all__'
        widgets = {
            'authors': forms.CheckboxSelectMultiple,  # Используем виджет для выбора нескольких авторов
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']