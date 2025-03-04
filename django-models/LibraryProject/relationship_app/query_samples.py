from relationship_app.models import Author, Book, Library, Librarian

author_name = "John Doe"
author = Author.objects.get(name = author_name)
books_by_author = Book.objects.filter(author = author)


library_name = "School Library"
library = Library.objects.get(name = library_name)
books_in_library = library.books.all()


Librarian_library_name = "School Library"
Librarian_library = library.objects.get(name = Librarian_library_name)
librarian = Librarian_library_name