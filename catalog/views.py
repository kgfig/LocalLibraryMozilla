from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404

from .models import Author, Book, BookInstance, Genre

def index(request):
    """View function for home page of our catalog app"""

    # Generate counts of main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books
    num_instances_available = BookInstance.objects.filter(status__exact=BookInstance.AVAILABLE).count()

    # Authors
    num_authors = Author.objects.all().count()

    # Genres
    genres = Genre.objects.all()

    # Track number of visits to this view and store it in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'genre_list': genres,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

def book_list_by_genre(request, genre_id):
    """Returns the list of books under the selected genre"""
    genre = Genre.objects.get(id=genre_id)

    # Get list of books in the given genre
    book_list = Book.objects.filter(genre__id=genre_id)
    
    context = {
        'genre': genre,
        'book_list': book_list,
    }

    return render(request, 'catalog/book_list_by_genre.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookListByGenreView(generic.ListView):
    model = Book
    template_name = 'catalog/book_list_by_genre.html'
    # context_object_name
    # template_name
    # queryset = Book.objects.filter(genre__id=genre_id)

    # Pass the custom queryset as context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_in_genre_list'] = self.book_list
        return context
    
    # Use the id from the url to create a queryset for the subset of Books in the given genre
    def get_queryset(self):
        genre_id = self.kwargs['genre_id']
        self.book_list = Book.objects.filter(genre__id=genre_id)
        return self.book_list

def book_detail_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book': book,
    }
    return render(request, 'catalog/book_detail.html', context=context)

class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'catalog/book_detail.html'
    pk_url_kwarg = 'book_id'

class AuthorListView(generic.ListView):
    model = Author
    pk_url_kwarg = 'author_id'
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'

class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'catalog/author_detail.html'
    pk_url_kwarg = 'author_id'
