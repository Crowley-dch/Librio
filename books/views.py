from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Loan
from django.utils import timezone
from datetime import timedelta

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
            # Создаем запись о выдаче
            Loan.objects.create(
                book=book,
                borrower_name=borrower_name,
                return_date=timezone.now().date() + timedelta(days=14)
            )
            # Меняем статус книги
            book.is_available = False
            book.save()
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