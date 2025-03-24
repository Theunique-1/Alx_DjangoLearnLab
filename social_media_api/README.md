Social Media API - Accounts Service

This document provides details on setting up and using the accounts service of the Social Media API.

## Setup Process

1.  *Install Dependencies:*

    bash
    pip install django djangorestframework Pillow
    

2.  *Create Django Project and App:*

    bash
    django-admin startproject social_media_api
    cd social_media_api
    python manage.py startapp accounts
    

3.  **Configure settings.py:**

    * Add 'rest_framework' and 'rest_framework.authtoken' and 'accounts' to INSTALLED_APPS:

        python
        INSTALLED_APPS = [
            # ...
            'rest_framework',
            'rest_framework.authtoken',
            'accounts',
        ]
        

4.  **Define User Model (accounts/models.py):**

    python
    from django.contrib.auth.models import AbstractUser
    from django.db import models
    from django.contrib.auth.models import Group, Permission
    from django.utils.translation import gettext_lazy as _

    class CustomUser(AbstractUser):
        bio = models.TextField(blank=True)
        profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
        followers = models.ManyToManyField('self', symmetrical=False, blank=True)
        groups = models.ManyToManyField(
            Group,
            verbose_name=_('groups'),
            blank=True,
            help_text=_(
                'The groups this user belongs to. A user will get all permissions '
                'granted to each of their groups.'
            ),
            related_name="customuser_set",
            related_query_name="user",
        )
        user_permissions = models.ManyToManyField(
            Permission,
            verbose_name=_('user permissions'),
            blank=True,
            help_text=_('Specific permissions for this user.'),
            related_name="customuser_set",
            related_query_name="user",
        )

        def __str__(self):
            return self.username
    

5.  **Create Serializers (accounts/serializers.py):**

    python
    from rest_framework import serializers
    from django.contrib.auth import get_user_model, authenticate
    from rest_framework.authtoken.models import Token

    User = get_user_model()

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 'followers')
            extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user

    class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

        def validate(self, data):
            user = authenticate(**data)
            if user and user.is_active:
                return user
            raise serializers.ValidationError("Incorrect Credentials")

    class TokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = Token
            fields = ('key',)
    

6.  **Create Views (accounts/views.py):**

    python
    from rest_framework import status
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from .serializers import UserSerializer, LoginSerializer, TokenSerializer
    from rest_framework.authtoken.models import Token
    from django.contrib.auth import get_user_model
    from rest_framework.permissions import IsAuthenticated

    User = get_user_model()

    class UserCreate(APIView):
        def post(self, request):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class UserLogin(APIView):
        def post(self, request):
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class GetToken(APIView):
        def post(self, request):
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class UserProfile(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
    

7.  **Create URLs (accounts/urls.py):**

    python
    from django.urls import path
    from .views import UserCreate, UserLogin, GetToken, UserProfile

    urlpatterns = [
        path('register/', UserCreate.as_view(), name='user_register'),
        path('login/', UserLogin.as_view(), name='user_login'),
        path('token/', GetToken.as_view(), name='get_token'),
        path('profile/', UserProfile.as_view(), name='user_profile'),
    ]
    

8.  **Include Accounts URLs in Project (social_media_api/urls.py):**

    python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('accounts.urls')),
    ]
    

9.  *Run Migrations:*

    bash
    python manage.py makemigrations
    python manage.py migrate
    

10. *Run the Development Server:*

    bash
    python manage.py runserver
    

## User Registration and Authentication

### Registration

* *Endpoint:* POST /accounts/register/
* *Method:* POST
* *Headers:* Content-Type: application/json
* *Body:*

    json
    {
        "username": "yourusername",
        "email": "your@email.com",
        "password": "yourpassword"
    }
    

* *Response:* Returns a JSON object with a token key.

### Login

* *Endpoint:* POST /accounts/login/
* *Method:* POST
* *Headers:* Content-Type: application/json
* *Body:*

    json
    {
        "username": "yourusername",
        "password": "yourpassword"
    }
    

* *Response:* Returns a JSON object with a token key.

### User Profile

* *Endpoint:* GET /accounts/profile/
* *Method:* GET
* *Headers:* Authorization: Token <your_token>
* *Response:* Returns a JSON object containing the user's profile information.

## User Model Overview

The CustomUser model extends Django's AbstractUser to include the following fields:

* bio: A text field for user biography.
* profile_picture: An image field for the user's profile picture.
* followers: A ManyToMany field representing user followers.
* groups: A ManyToMany field to manage user groups.
* user_permissions: A ManyToMany field to assign specific user permissions.