# catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('book/<int:book_id>/', views.book_detail_view, name='book-detail'),
    path('genre/<int:genre_id>/', views.BookListByGenreView.as_view(), name='book-list-by-genre'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('author/<int:author_id>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    path('libuser/books/', views.LoanedBooksByUserListView.as_view(), name='loaned-books-by-user'),
    path('books/loaned/', views.LoanedBookListView.as_view(), name='loaned-books'),
    path('bookinstance/<uuid:bookinstance_id>/return/', views.bookinstance_return_view, name='bookinstance-return'),
    path('bookinstance/<uuid:bookinstance_id>/renew/', views.bookinstance_renew_view, name='bookinstance-renew'),
    # re_path(r'^genre/(?P<genre_id>\d+)/$', views.BookListByGenreView.as_view(), name='book-list-by-genre'),
]
