from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import datetime

from .forms import RenewBookModelForm
from catalog.models import Author, Book, BookInstance, Genre

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

@login_required
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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing book instances on loan to current user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__iexact=BookInstance.ON_LOAN).order_by('due_back')

def bookinstance_return_view(request, bookinstance_id):
    bookinstance_item = get_object_or_404(BookInstance, id=bookinstance_id)
    bookinstance_item.borrower = None
    bookinstance_item.status = BookInstance.AVAILABLE
    bookinstance_item.due_back = None
    bookinstance_item.save()

    response = HttpResponse("Marked as returned!")
    return response

class LoanedBookListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/loaned_book_list.html'
    context_object_name = 'loaned_book_list'
    permission_required = ('catalog.can_mark_returned')

    def get_queryset(self):
        self.bookinstance_list = BookInstance.objects.filter(status__iexact=BookInstance.ON_LOAN)
        return self.bookinstance_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loaned_book_list'] = self.bookinstance_list
        return context

@permission_required('catalog.can_renew')
def bookinstance_renew_view(request, bookinstance_id):
    bookinstance_item = get_object_or_404(BookInstance, id=bookinstance_id)

    # If this is a POST request, process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request
        renew_book_form = RenewBookModelForm(request.POST)
        valid = renew_book_form.is_valid()

        # Validate
        if renew_book_form.is_valid():
            # Process/save validated data
            bookinstance_item.due_back = renew_book_form.cleaned_data['due_back']
            bookinstance_item.save()

            # Redirect
            return HttpResponseRedirect(reverse('loaned-books'))
        
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        initial_data = {
                'due_back': proposed_renewal_date,
        }
        renew_book_form = RenewBookModelForm(initial=initial_data)

    context = {
            'form': renew_book_form,
            'bookinstance_item': bookinstance_item,
    }

    return render(request, 'catalog/bookinstance_renew.html', context)


class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_edit_authors'

class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_edit_authors'
    template_name_suffix = '_update_form'

class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')
    template_name_suffix = '_delete_confirmation'
    permission_required = 'catalog.can_edit_authors'

class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.can_edit_books'
    fields = '__all__'
    template_name_suffix = '_create_form'

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.can_edit_books'
    fields = '__all__'
    exclude = ['id']
    template_name_suffix = '_update_form'
    pk_url_kwarg = 'book_id'

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('book-list')
    template_name_suffix = '_confirm_delete'
    permission_required = 'catalog.can_edit_books'
    pk_url_kwarg = 'book_id'
