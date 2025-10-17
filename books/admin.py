from django.contrib import admin
from .models import Author, Genre, Book, Loan, UserProfile


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
    list_display = ['title', 'author', 'genre', 'access_level', 'max_loan_days', 'is_available']
    list_filter = ['is_available', 'genre', 'access_level']
    search_fields = ['title', 'author__full_name']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'loan_date', 'expiry_date', 'status', 'is_access_active_display']
    list_filter = ['status', 'loan_date']
    search_fields = ['book__title', 'user__username']

    def is_access_active_display(self, obj):
        return obj.is_access_active()

    is_access_active_display.boolean = True
    is_access_active_display.short_description = 'Доступ активен'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone']
    list_filter = ['user_type']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']