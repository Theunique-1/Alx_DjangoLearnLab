from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import user

# Create your tests here:

class TestBookViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Jane Austen")
        self.book = Book.objects.create(title="Pride and Prejudice", publication_year=1813, author=self.author)
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.author_user = Author.objects.create(name="Author User")
        self.author_user.user = self.user
        self.author_user.save()
        self.book2 = Book.objects.create(title="Emma", publication_year=1815, author=self.author_user)

    def test_book_list_view(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Pride and Prejudice")