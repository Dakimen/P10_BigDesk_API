"""
Views for auth app.
Contains:
    class CustomLoginView(LoginView) :
        Custom login view that overrides the default LoginView.
        def get_success_url(self):
            Returns the URL to redirect the user to on successful login.
            Overrides the default method.

    def sign-up(request):
        Handles user registration and login.
    def logout_user(request):
        Logs user out of their account and redirects them to landing.
"""

from django.shortcuts import render, redirect
from custom_auth.forms import SignUpForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    """
    Custom login view that overrides the default LoginView.

    Attributes:
        template_name (str): The template to use for the login page.
        redirect_authenticated_user (bool): Redirects authenticated users.
        authentication_form (CustomAuthenticationForm):
            The custom authentication form to be used.
    """
    template_name = 'custom_auth/landing.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        """
        Returns the URL to redirect the user to upon successful login.
        Overrides the default `get_success_url` method in the LoginView.

        Returns:
            str: The URL to redirect the user after a successful login.
        """
        return redirect('landing')


def sign_up(request):
    """
    Handles user registration and login.

    If the request method is POST, this view processes the registration form,
    creates a new user, logs the user in, and redirects them to the 'flux'.
    If the request method is GET,
    it renders the sign-up form for the user to fill out.

    Args:
        request (HttpRequest): The HTTP request object containing request data.

    Returns:
        HttpResponse: A redirect response to the 'flux' page
        if registration is successful,
        or a rendered sign-up page if GET request is made.
    """
    if request.method == 'POST':
        register = SignUpForm(request.POST)
        if register.is_valid():
            user = register.save()
            login(request, user)
            return redirect('flux')
        else:
            register.add_error(None, 'Mots de passe ne sont pas identiques')
            return render(request,
                          'custom_auth/sign_up.html',
                          {'form': register})
    else:
        register = SignUpForm()
        return render(request,
                      'custom_auth/sign_up.html',
                      {'form': register})


def logout_user(request):
    """
    Logs out the current user and redirects them to the landing page.
    Args:
        request (HttpRequest): The HTTP request object containing request data.

    Returns:
        HttpResponse:
        A redirect response to the 'landing' page after logging out.
    """
    logout(request)
    return redirect('landing')
