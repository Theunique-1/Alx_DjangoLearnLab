from django.db import models
from django.contrib.auth.models import User # Import the User model for author relationship

# Create your models here.
class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200, help_text="Title of the blog post.")  # CharField for post title, max length 200
    content = models.TextField(help_text="Content of the blog post.")  # TextField for post content
    published_date = models.DateTimeField(auto_now_add=True, help_text="Date and time the post was published.")  # DateTimeField for publication date, automatically set on creation
    author = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Author of the blog post.")  # ForeignKey to User model, CASCADE delete behavior

    def _str_(self):
        """
        String representation of the Post object.
        """
        return self.title  # Returns the title of the post when the object is represented as a string