from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from base.models import Type, Genre

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class SignupFormStep1(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class SignupFormStep2(forms.Form):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(), 
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'id': 'id_genres'}),
        help_text="Select preferred genres (use Ctrl or Command for multiple selection)"
    )
    media_types = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'id': 'id_media_types'}),
        help_text="Select preferred media types (use Ctrl or Command for multiple selection)"
    )

