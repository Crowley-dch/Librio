from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Loan, Genre
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .models import UserProfile
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('home')
@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, user_type='student')

    user_loans = Loan.objects.filter(user=request.user).order_by('-loan_date')

    return render(request, 'books/profile.html', {
        'user_loans': user_loans,
        'user_profile': user_profile
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(user=user, user_type='student')

            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()

    return render(request, 'books/register.html', {'form': form})

def book_list(request):
    books = Book.objects.all()
    genres = Genre.objects.all()

    # Поиск по названию, автору или жанру
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            models.Q(title__icontains=search_query) |
            models.Q(author__full_name__icontains=search_query) |
            models.Q(genre__name__icontains=search_query)
        )

    # Фильтрация по жанру
    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books = books.filter(genre__name=genre_filter)

    # Фильтрация по уровню доступа (НОВОЕ!)
    access_level_filter = request.GET.get('access_level', '')
    if access_level_filter:
        books = books.filter(access_level=access_level_filter)

    return render(request, 'books/book_list.html', {
        'books': books,
        'genres': genres,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'access_level_filter': access_level_filter,  # НОВОЕ!
    })
def home(request):
    return render(request, 'books/home.html')


def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        borrower_name = request.POST.get('borrower_name')

        if borrower_name and book.is_available:
            user_profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={'user_type': 'guest'}  # по умолчанию гость
            )

            if not user_profile.can_borrow_book(book):
                messages.error(request,
                               f'Доступ запрещен! Ваш уровень: {user_profile.get_access_description()}. '
                               f'Книга требует: {book.get_access_level_display()}.'
                               )
                return redirect('book_list')

            Loan.objects.create(
                book=book,
                user=request.user,
                borrower_name=borrower_name
            )

            book.is_available = False
            book.save()

            messages.success(request, f'Книга "{book.title}" успешно выдана!')
            return redirect('book_list')

    return render(request, 'books/borrow_book.html', {'book': book})


def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == 'POST':
        loan.return_date = timezone.now().date()
        loan.save()
        # Возвращаем книгу в доступные
        loan.book.is_available = True
        loan.book.save()
        return redirect('book_list')

    return render(request, 'books/return_book.html', {'loan': loan})