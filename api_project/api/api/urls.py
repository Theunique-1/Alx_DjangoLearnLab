from django.urls import path
from .import views, BookList

urlpatterns = [
    path ('books/', views.BookList, name="book_list"),
]