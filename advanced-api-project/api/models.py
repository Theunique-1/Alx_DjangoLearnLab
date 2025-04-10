from django.db import models

# Create your models here.
class Author(models.Model):      # Model representing an author
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Book(models.Model):       # Model representing a book
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name = 'books')

    def __str__(self):
        return self.title
    