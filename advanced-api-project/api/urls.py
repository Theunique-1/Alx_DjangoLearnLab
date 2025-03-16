from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns [
     path('books/', BookListView.as_view(), name ='book-list'), # url pattern for listing books
     path('books/<int:pk/>', BookDetailView.as_view(), name='book-detail'), # url pattern for viewing a book by id
     path('books/create/', BookCreateView.as_view(), name='book-create'), # url pattern for creating a book
     path('books/<int:pk>/update/',BookUpdateView.as_view(), name='book-update'), # url pattern for updating a book by id
     path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'), # url pattern for deleting a book by id
]