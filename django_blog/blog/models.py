from django.db import models
from django.contrib.auth.models import User # Import the User model for author relationship
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here. 

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def _str_(self):
        return self.name
    

class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)  # CharField for post title, max length 200
    content = models.TextField()  # TextField for post content
    published_date = models.DateTimeField(auto_now_add=True)  # DateTimeField for publication date, automatically set on creation
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model, CASCADE delete behavior
    tags = models.ManyToManyField(Tag, related_name='posts', through='PostTag')

    def __str__(self):
        return self.title  # Returns the title of the post when the object is represented as a string

    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    