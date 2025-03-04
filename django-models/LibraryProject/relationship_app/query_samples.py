from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    """Retrieves books by a given author name."""
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def get_books_in_library(library_name):
    """Retrieves books in a given library."""
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []

def get_librarians_in_library(library_name):
    """Retrieves librarians in a given library."""
    try:
        library = Library.objects.get(name=library_name)
        return Librarian.objects.filter(library=library)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []