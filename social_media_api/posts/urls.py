from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserFeedView, LikePostView, UnlikePostView
from django.urls import path

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('feed/', UserFeedView.as_view(), name='user_feed'),
    path('like/', LikePostView.as_view(), name='like_post'),
    path('unlike/', UnlikePostView.as_view(), name='unlike_post'),
]

urlpatterns += router.urls