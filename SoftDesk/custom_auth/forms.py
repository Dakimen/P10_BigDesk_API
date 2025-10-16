"""
Forms module of the auth app.
Contains:
CustomAuthenticationForm(AuthenticationForm)
Used for User Authentication, contains:
    A character field for username
    A password field
SignUpForm(UserCreationForm) - form used to create a new account, containing:
    username - character field
    password1 - password field
    password2 - password confirmation
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class CustomAuthenticationForm(AuthenticationForm):
    """
    CustomAuthenticationForm(AuthenticationForm)
    Used for authentication, contains:
    A character field for username
    A password field
    """
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur"
        })
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mot de passe'
        })
    )


class SignUpForm(UserCreationForm):
    """
    Form used to create a new account, containing:
    username - character field
    password1 - password field
    password2 - password confirmation
    """
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur",
        })
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mot de passe'
        })
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmer mot de passe'
        })
    )
    can_be_contacted = forms.BooleanField(
        label='Permission de vous contacter',
    )
    can_data_be_shared = forms.BooleanField(
        label='Permission de partager vos données'
    )

    class Meta(UserCreationForm.Meta):
        """
        SignUpForm specifications,
        determining model to use and fields to display
        """
        model = get_user_model()
        fields = ('username', 'password1', 'password2',
                  'can_be_contacted', 'can_data_be_shared')
