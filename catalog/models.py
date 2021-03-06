from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from datetime import date
import uuid

class Book(models.Model):
    """Model representing a Book (but not a specific copy of a book)"""

    # Fields
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a summary of this book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13-character ISBN number')
    genre = models.ManyToManyField('Genre', help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, null=False)

    # Metadata
    class Meta:
        ordering = ['title']
        permissions = (
            ('can_edit_books', 'Create, update or delete books'),        
        )

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Book"""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class Genre(models.Model):
    """Model representing a Genre"""

    # Fields
    name = models.CharField(max_length=64)

    # Meta
    class Meta:
        ordering = ['name']

    # Methods

    def __str__(self):
        return self.name


class Language(models.Model):
    """Model representing a language"""

    # Fields
    name = models.CharField(max_length=64)

    # Meta
    class Meta:
        ordering = ['name']

    # Methods
    def __str__(self):
        return self.name


class Author(models.Model):
    """Model representing an Author"""

    # Fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    # Meta
    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (
                ('can_edit_authors', 'Create, edit or delete authors'),
        )

    # Methods
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class BookInstance(models.Model):
    """Model representing an instance of a Book"""

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Book Instance')
    due_back = models.DateField('Return on', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    imprint = models.CharField(max_length=200)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    MAINTENANCE = 'm'
    ON_LOAN = 'o'
    AVAILABLE  = 'a'
    RESERVED = 'r'

    LOAN_STATUS = (
        (MAINTENANCE, 'Maintenance'),
        (ON_LOAN, 'On loan'),
        (AVAILABLE, 'Available'),
        (RESERVED, 'Reserved'),
    )

    status = models.CharField(
            max_length=64,
            choices=LOAN_STATUS,
            blank=True,
            default=MAINTENANCE,
            help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back', 'book']
        permissions = (
                ('can_mark_returned', 'Set book as returned'),
                ('can_renew', 'Renew book due date'),
        )

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

