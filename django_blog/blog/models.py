from django.db import models
from django.contrib.auth.models import User # Import the User model for author relationship
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)  # CharField for post title, max length 200
    content = models.TextField()  # TextField for post content
    published_date = models.DateTimeField(auto_now_add=True)  # DateTimeField for publication date, automatically set on creation
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model, CASCADE delete behavior

    def __str__(self):
        """
        String representation of the Post object.
        """
        return self.title  # Returns the title of the post when the object is represented as a string

    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])