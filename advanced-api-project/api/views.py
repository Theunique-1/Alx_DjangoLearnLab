from django.shortcuts import render
from rest_framework import generics, serializers, permissions
from .models import Book
from .serializers import BookSerializer
from datetime import datetime
from .permissions import IsAuthorOrReadOnly

# Create your views here.

class BookListView(generics.ListAPIView): # view to list all books
    queryset = Book.objects.all() # Get all book object
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view


class BookDetailView(generics.RetrieveAPIView):  # To show details of a single book
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny] # Allow anyone to view


class BookCreateView(generics.CreateAPIView):   # View to create a new book with custom validation
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Only logged in users can create

    def perform_create(self, serializer):
        publication_year = serializer.validated_data.get('publication_year')
        if publication_year > datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):  # To update an existing book with custom validation
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly] # Only logged in user can update

    def perform_update(self, serializer):
        publication_year = serializer.validated_data.get('publication_year', serializer.instance.publication_year)
        if publication_year > datetime.now().year:
            raise serializers.ValidationError("Publication cannot be in the future.")
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged in users can delete book



