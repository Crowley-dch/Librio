# Librio - Система управления электронной библиотекой

Django-приложение для управления электронной библиотекой учебного заведения.

## Функциональность

- 📚 Каталог книг с поиском
- 👥 Управление пользователями
- 📖 Система выдачи и возврата книг
- 🎯 Админ-панель для управления контентом

## Технологии

- Python 3.12
- Django 5.2
- SQLite
- Bootstrap 5

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ВАШ_USERNAME/librio-library.git
cd librio-library
```
2. создайте виртуальное окружение
```bash
python -m venv venv
venv\Scripts\activate
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Примените миграции
```bash
python manage.py migrate
```
5. Запустите сервер
```bash
python manage.py runserver
```
## Доступ

- Веб-сайт: http://127.0.0.1:8000
- Админ-панель: http://127.0.0.1:8000/admin
