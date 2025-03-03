book = Book.objects.get(title = "1984", author = "George Orwell", publication_year = 1949)
print(book.title,book.author,book.publication_year)