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
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
