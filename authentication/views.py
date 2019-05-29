from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .backend import JWTAuthentication

# Create your views here.
from .serializers import (
    RegistrationSerializer, LoginSerializer, UserSerializer
)

from django.contrib.auth.hashers import check_password
from .models import User


auth = JWTAuthentication()

class RegistrationAPIView(CreateAPIView):
    """
    Register a new user.
    """
    # Allow any user (authenticated or not) to hit thiis endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        request.data['username'] = request.data['username'].lower()
        user = request.data

        serializer = self.serializer_class(
            data=user, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        success_message={
            "success": "Please check your email for a link to complete your registration!"
        }
        return Response(success_message, status=status.HTTP_201_CREATED)

class LoginAPIView(CreateAPIView):
    """
    Login a registered a user.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
