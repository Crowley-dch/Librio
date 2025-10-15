from django.contrib import admin
from .models import Author, Genre, Book, Loan

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    search_fields = ['full_name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'is_available']
    list_filter = ['is_available', 'genre']
    search_fields = ['title', 'author__full_name']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower_name', 'loan_date', 'return_date']
    list_filter = ['loan_date']
    search_fields = ['book__title', 'borrower_name']