from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Author(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=500, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр")
    is_available = models.BooleanField(default=True, verbose_name="Доступна")

    ACCESS_LEVELS = [
        ('free', 'Свободный доступ'),
        ('student', 'Только для студентов'),
        ('premium', 'Премиум доступ'),
        ('restricted', 'Ограниченный доступ'),
    ]
    access_level = models.CharField(
        max_length=20,
        choices=ACCESS_LEVELS,
        default='free',
        verbose_name="Уровень доступа"
    )
    max_loan_days = models.IntegerField(
        default=7,
        verbose_name="Срок выдачи (дней)"
    )
    description = models.TextField(blank=True, verbose_name="Описание")

    def get_access_description(self):
        descriptions = {
            'free': 'Свободный доступ',
            'student': 'Для студентов',
            'premium': 'Премиум доступ',
            'restricted': 'Ограниченный доступ'
        }
        return descriptions.get(self.access_level, 'Неизвестный доступ')

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


class Loan(models.Model):
    LOAN_STATUS = [
        ('active', 'Активна'),
        ('expired', 'Истекла'),
        ('returned', 'Возвращена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    loan_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")
    expiry_date = models.DateTimeField(verbose_name="Дата истечения")  # КОГДА ДОСТУП ЗАКОНЧИТСЯ
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='active', verbose_name="Статус")

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"

    def __str__(self):
        return f"{self.book.title} - {self.borrower_name}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.expiry_date:  # только при создании
            self.expiry_date = timezone.now() + timedelta(days=self.book.max_loan_days)

        if self.expiry_date and timezone.now() > self.expiry_date:
            self.status = 'expired'
            if self.book.is_available == False:
                self.book.is_available = True
                self.book.save()

        super().save(*args, **kwargs)

    def days_remaining(self):
        if self.status != 'active' or not self.expiry_date:
            return 0
        remaining = self.expiry_date - timezone.now()
        return max(0, remaining.days)

    def is_overdue(self):
        return self.status == 'active' and self.expiry_date and timezone.now() > self.expiry_date

    def is_access_active(self):
        from django.utils import timezone
        return self.status == 'active' and timezone.now() <= self.expiry_date


class UserProfile(models.Model):
    USER_TYPES = [
        ('guest', 'Гость'),
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('premium', 'Премиум пользователь'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='guest',
        verbose_name="Тип пользователя"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"

    @property
    def access_level(self):
        access_map = {
            'guest': 'free',
            'student': 'student',
            'teacher': 'premium',
            'premium': 'premium'
        }
        return access_map.get(self.user_type, 'free')

    def can_borrow_book(self, book):
        access_rules = {
            'guest': ['free'],  # Гости - только свободные книги
            'student': ['free', 'student'],  # Студенты + студенческие
            'teacher': ['free', 'student', 'premium'],  # Преподаватели + премиум
            'premium': ['free', 'student', 'premium', 'restricted']  # Полный доступ
        }

        user_access = self.access_level
        book_access = book.access_level

        return book_access in access_rules.get(user_access, [])

    def get_access_description(self):
        access_descriptions = {
            'guest': 'Только книги со свободным доступом',
            'student': 'Книги со свободным и студенческим доступом',
            'teacher': 'Все книги кроме ограниченных',
            'premium': 'Полный доступ ко всем книгам'
        }
        return access_descriptions.get(self.user_type, 'Неизвестный уровень доступа')