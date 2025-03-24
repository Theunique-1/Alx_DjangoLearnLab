from django.urls import path
from .views import UserCreate, UserLogin, GetToken, UserProfile

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user_register'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('token/', GetToken.as_view(), name='get_token'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
]