from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
 # serializer for the book model.
 class Meta:
  model = Book
  fields = '__all__'
 
 def validate_publication_year(self, value):
  # Custom validation to ensure publication is not in the future.
  current_year = datetime.now().year
  if value > current_year:
   raise serializers.ValidationError("Publication year is not in the future.")
  return value
 
class AuthorSerializer(serializers.ModelSerializer):
 # Serializer for the author model, including nested BookSerializer.
 books = BookSerializer(many = True, read_only = True)

 class Meta:
  model = Author
  fields = ['id', 'name', 'books']