from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')


def clean(self):
    if self.publication_year > time.now.year:
        raise ValidationError({"publication_year": "publication_year is not in the future."})
    super().clean() # ensure other valodation ars run
