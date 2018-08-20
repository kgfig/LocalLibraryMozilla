# catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('book/<int:book_id>/', views.BookDetailView.as_view(), name='book-detail'),
    path('genre/<int:genre_id>/', views.BookListByGenreView.as_view(), name='book-list-by-genre'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('author/<int:author_id>/', views.AuthorDetailView.as_view(), name='author-detail'),
    # re_path(r'^genre/(?P<genre_id>\d+)/$', views.BookListByGenreView.as_view(), name='book-list-by-genre'),
]
