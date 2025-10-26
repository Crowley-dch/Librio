from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('loans/<int:loan_id>/return/', views.return_book, name='return_book'),
path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='books/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/logout/', views.custom_logout, name='logout'),
]
