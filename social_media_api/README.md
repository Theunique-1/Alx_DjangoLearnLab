

Details on setting up and using the accounts service of the Social Media API.

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


 Posts and Comments Service

API endpoints for managing posts and comments within the Social Media API.

## Setup (Assuming Accounts Service is Already Setup)

1.  **Create posts App:**

    bash
    python manage.py startapp posts
    

2.  **Add posts to INSTALLED_APPS in social_media_api/settings.py:**

    python
    INSTALLED_APPS = [
        # ...
        'posts',
    ]
    

3.  **Define Models (posts/models.py):**

    python
    from django.db import models
    from django.contrib.auth import get_user_model

    User = get_user_model()

    class Post(models.Model):
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        title = models.CharField(max_length=200)
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.title

    class Comment(models.Model):
        post = models.ForeignKey(Post, on_delete=models.CASCADE)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.content
    

4.  **Create Serializers (posts/serializers.py):**

    python
    from rest_framework import serializers
    from .models import Post, Comment
    from django.contrib.auth import get_user_model

    User = get_user_model()

    class PostSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source='author.username')

        class Meta:
            model = Post
            fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at')

    class CommentSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source='author.username')

        class Meta:
            model = Comment
            fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at')
    

5.  **Create Views (posts/views.py):**

    python
    from rest_framework import viewsets, permissions, filters
    from .models import Post, Comment
    from .serializers import PostSerializer, CommentSerializer
    from .permissions import IsAuthorOrReadOnly
    from rest_framework.pagination import PageNumberPagination

    class PostPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    class CommentPagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 100

    class PostViewSet(viewsets.ModelViewSet):
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
        pagination_class = PostPagination
        filter_backends = [filters.SearchFilter]
        search_fields = ['title', 'content']

        def perform_create(self, serializer):
            serializer.save(author=self.request.user)

    class CommentViewSet(viewsets.ModelViewSet):
        queryset = Comment.objects.all()
        serializer_class = CommentSerializer
        permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
        pagination_class = CommentPagination

        def perform_create(self, serializer):
            serializer.save(author=self.request.user)
    

6.  **Create Permissions (posts/permissions.py):**

    python
    from rest_framework import permissions

    class IsAuthorOrReadOnly(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.author == request.user
    

7.  **Create URLs (posts/urls.py):**

    python
    from rest_framework.routers import DefaultRouter
    from .views import PostViewSet, CommentViewSet

    router = DefaultRouter()
    router.register(r'posts', PostViewSet, basename='post')
    router.register(r'comments', CommentViewSet, basename='comment')

    urlpatterns = router.urls
    

8.  **Include Posts URLs in Project (social_media_api/urls.py):**

    python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('accounts.urls')),
        path('posts/', include('posts.urls')),
    ]
    

9.  *Run Migrations:*

    bash
    python manage.py makemigrations posts
    python manage.py migrate
    

## Posts Endpoints

### List Posts

* *Endpoint:* GET /posts/posts/
* *Method:* GET
* *Headers:* (None Required)
* *Query Parameters:*
    * page: Page number (e.g., ?page=2)
    * page_size: Number of items per page (e.g., ?page_size=10)
    * search: Search posts by title or content (e.g., ?search=example)
* *Response:*

    json
    {
        "count": 100,
        "next": "[http://127.0.0.1:8000/posts/posts/?page=2](https://www.google.com/search?q=http://127.0.0.1:8000/posts/posts/%3Fpage%3D2)",
        "previous": null,
        "results": [
            {
                "id": 1,
                "author": "user1",
                "title": "Example Post",
                "content": "This is an example post.",
                "created_at": "2023-10-27T10:00:00Z",
                "updated_at": "2023-10-27T10:00:00Z"
            },
            // ... more posts
        ]
    }
    

### Create Post

* *Endpoint:* POST /posts/posts/
* *Method:* POST
* *Headers:*
    * Content-Type: application/json
    * Authorization: Token <your_token>
* *Body:*

    json
    {
        "title": "New Post",
        "content": "This is a new post."
    }
    

* *Response:*

    json
    {
        "id": 101,
        "author": "user1",
        "title": "New Post",
        "content": "This is a new post.",
        "created_at": "2023-10-27T10:30:00Z",
        "updated_at": "2023-10-27T10:30:00Z"
    }
    

### Update Post

* *Endpoint:* PUT /posts/posts/{post_id}/
* *Method:* PUT
* *Headers:*
    * Content-Type: application/json
    * Authorization: Token <your_token>
* *Body:*

    json
    {
        "title": "Updated Post",
        "content": "This post has been updated."
    }
    

* *Response:* (Updated post object)

### Delete Post

* *Endpoint:* DELETE /posts/posts/{post_id}/
* *Method:* DELETE
* *Headers:*
    * Authorization: Token <your_token>
* *Response:* 204 No Content

## Comments Endpoints

### List Comments

* *Endpoint:* GET /posts/comments/
* *Method:* GET
* *Headers:* (None Required)
* *Query Parameters:* (Pagination: page, page_size)
* *Response:* (Paginated list of comments)

### Create Comment

* *Endpoint:* POST /posts/comments/
* *Method:* POST
* *Headers:*
    * Content-Type: application/json
    * `Authorization: Token <your


# Social Media API - Follows and Feed Service

Details of the API endpoints for managing user follows and accessing the user feed within the Social Media API.

## Setup (Assuming Posts and Accounts Services are Already Setup)

1.  **Modify accounts/models.py:**

    * Add the followers field to the CustomUser model:

        python
        from django.contrib.auth.models import AbstractUser
        from django.db import models
        from django.contrib.auth.models import Group, Permission
        from django.utils.translation import gettext_lazy as _

        class CustomUser(AbstractUser):
            bio = models.TextField(blank=True)
            profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
            followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')
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
        

2.  *Run Migrations:*

    bash
    python manage.py makemigrations accounts
    python manage.py migrate
    

3.  **Create Follow/Unfollow Views (accounts/views.py):**

    python
    from rest_framework import status
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from rest_framework.permissions import IsAuthenticated
    from django.shortcuts import get_object_or_404
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # ... (other views)

    class FollowUser(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request, user_id):
            user_to_follow = get_object_or_404(User, id=user_id)
            if request.user == user_to_follow:
                return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.followers.add(user_to_follow)
            return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)

    class UnfollowUser(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request, user_id):
            user_to_unfollow = get_object_or_404(User, id=user_id)
            request.user.followers.remove(user_to_unfollow)
            return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
    

4.  **Create Feed View (posts/views.py):**

    python
    from rest_framework import viewsets, permissions, filters, generics
    from .models import Post, Comment
    from .serializers import PostSerializer, CommentSerializer
    from rest_framework.pagination import PageNumberPagination
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # ... (other views)

    class UserFeedView(generics.ListAPIView):
        serializer_class = PostSerializer
        permission_classes = [permissions.IsAuthenticated]

        def get_queryset(self):
            user = self.request.user
            following_users = user.followers.all()
            return Post.objects.filter(author__in=following_users).order_by('-created_at')
    

5.  **Create URLs (accounts/urls.py and posts/urls.py):**

    * accounts/urls.py:

        python
        from django.urls import path
        from .views import UserCreate, UserLogin, GetToken, UserProfile, FollowUser, UnfollowUser

        urlpatterns = [
            # ... (other paths)
            path('follow/<int:user_id>/', FollowUser.as_view(), name='follow_user'),
            path('unfollow/<int:user_id>/', UnfollowUser.as_view(), name='unfollow_user'),
        ]
        

    * posts/urls.py:

        python
        from rest_framework.routers import DefaultRouter
        from .views import PostViewSet, CommentViewSet, UserFeedView
        from django.urls import path

        router = DefaultRouter()
        router.register(r'posts', PostViewSet, basename='post')
        router.register(r'comments', CommentViewSet, basename='comment')

        urlpatterns = [
            path('feed/', UserFeedView.as_view(), name='user_feed'),
        ]

        urlpatterns += router.urls
        

6.  **Update social_media_api/urls.py:**

    python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/accounts/', include('accounts.urls')),
        path('api/posts/', include('posts.urls')),
    ]
    

## Follows Endpoints

### Follow User

* *Endpoint:* POST /api/accounts/follow/{user_id}/
* *Method:* POST
* *Headers:*
    * Authorization: Token <your_token>
* *Path Parameters:*
    * user_id: The ID of the user to follow.
* *Response:*

    json
    {
        "detail": "You are now following {username}."
    }
    

### Unfollow User

* *Endpoint:* POST /api/accounts/unfollow/{user_id}/
* *Method:* POST
* *Headers:*
    * Authorization: Token <your_token>
* *Path Parameters:*
    * user_id: The ID of the user to unfollow.
* *Response:*

    json
    {
        "detail": "You have unfollowed {username}."
    }
    

## Feed Endpoint

### Get User Feed

* *Endpoint:* GET /api/posts/feed/
* *Method:* GET
* *Headers:*
    * Authorization: Token <your_token>
* *Response:*

    json
    [
        {
            "id": 1,
            "author": "followed_user1",
            "title": "Post from followed user",
            "content": "Content of the post.",
            "created_at": "2023-10-27T10:00:00Z",
            "updated_at": "2023-10-27T10:00:00Z"
        },
        // ... more posts from followed users, ordered by creation date
    ]
    

## Model Changes

The CustomUser model in accounts/models.py has been updated to include a followers field:

* **followers:**
    * A ManyToMany field to self representing the users that the current user follows.
    * symmetrical=False to allow unidirectional follows.
    * related_name='following' to avoid reverse relation clashes.