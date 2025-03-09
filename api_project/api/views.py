from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def get_permission(self):
    '''''Instantiate and returns the list of permissions that this views requires. '''''
    if self.action in ['list','retrieve']: # Getting a list of books or a single book
        permission_classes = [permissions.AllowAny] # Anyone can access this end point
    elif self.action == 'create': # creating a new book
        permission_classes = [permissions.IsAuthenticated] # requiring a valid authentication token
    else:
        permission_classes = [permissions.IsAdminUser] #requiring an admin user with a valid token
    return [permission() for permission in permission_classes]

