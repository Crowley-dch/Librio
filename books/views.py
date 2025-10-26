from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Loan
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .models import UserProfile

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

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