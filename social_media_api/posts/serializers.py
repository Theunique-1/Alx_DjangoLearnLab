from rest_framework import serializers
from .models import Post, Comment, Like
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


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'timestamp')
        read_only_fields = ('user', 'timestamp')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Like.objects.create(**validated_data)