from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone

class BookSerializer(serializers.ModelSerialzer): #Serializer for the book model
    
    class Meta:
        model = Book
        fields = "__all__"  # Serializes all fields of the Book model


    def validate_publication_year(self, value): # Custom validation for the publication_year field
        if value > timezone.now().year:
            raise serializers.ValidationError("Publication_year cannot be in the future.") # Ensures that the publication year is not in the future
        return value



class AuthorSerializer(serializers.ModelSerializer): # Serializer for the author model
    books = BookSerializer(many=True, read_only=True) #Nested serializer for related books

    class Meta:
        model = Author
        fields = ["id", "name" "books"] #include names and related books, and id fied

    def create(self, validated_data):
        return super().create(validated_data)