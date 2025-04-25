import unittest

import pytest
import os
import json
import datetime
import io
import sys
from contextlib import contextmanager
from unittest.mock import patch, MagicMock

# Імпортуємо необхідні функції та класи з вашої системи
from refactored_main import (
    Book, User, BookBorrowing,
    add_book, add_user, borrow_book, return_book, search_books,
    load_data, save_data, _add_test_data, books, users, borrows
)


@contextmanager
def captured_input(user_input):
    """Контекстний менеджер для симуляції введення користувача"""
    orig_stdin = sys.stdin
    sys.stdin = io.StringIO(user_input)
    yield
    sys.stdin = orig_stdin


@contextmanager
def captured_output():
    """Контекстний менеджер для захоплення виводу програми"""
    new_out = io.StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield new_out
    finally:
        sys.stdout = old_out


@pytest.fixture(autouse=True)
def setup_teardown():
    """Fixture для підготовки та очищення тестового середовища перед та після кожного тесту"""
    # Підготовка тестового середовища
    global books, users, borrows
    books.clear()
    users.clear()
    borrows.clear()

    # Додавання тестових даних для використання в тестах
    books.append(Book(1, "Тестова книга", "Тестовий автор", "Фантастика", 2020))
    books.append(Book(2, "Друга книга", "Інший автор", "Драма", 2018))
    users.append(User(1, "Тест Юзер", "test@example.com", "0991234567"))

    yield  # Виконання тесту

    # Очищення після тесту
    books.clear()
    users.clear()
    borrows.clear()


# Тест 1: Перевірка створення об'єкта книги
def test_book_creation():
    """Перевірка правильного створення об'єкта книги з усіма атрибутами"""
    book = Book(3, "Нова книга", "Новий автор", "Детектив", 2022)
    assert book.id == 3
    assert book.title == "Нова книга"
    assert book.author == "Новий автор"
    assert book.genre == "Детектив"
    assert book.year == 2022
    assert book.available is True
    assert book.times_borrowed == 0


# Тест 2: Перевірка методу __str__ для книги
def test_book_str_representation():
    """Перевірка правильного рядкового представлення об'єкта книги"""
    book = Book(1, "Тестова книга", "Тестовий автор", "Фантастика", 2020)
    expected_str = "ID: 1, Назва: Тестова книга, Автор: Тестовий автор, Жанр: Фантастика, Рік: 2020, Статус: Доступна"
    assert str(book) == expected_str

    # Перевірка з unavailable книгою
    book.available = False
    expected_str = "ID: 1, Назва: Тестова книга, Автор: Тестовий автор, Жанр: Фантастика, Рік: 2020, Статус: Видана"
    assert str(book) == expected_str


# Тест 3: Перевірка створення об'єкта користувача
def test_user_creation():
    """Перевірка правильного створення об'єкта користувача з усіма атрибутами"""
    user = User(2, "Новий користувач", "new@example.com", "0667654321")
    assert user.id == 2
    assert user.name == "Новий користувач"
    assert user.email == "new@example.com"
    assert user.phone == "0667654321"
    assert user.borrowed_books == []
    assert user.history == []


# Тест 4: Перевірка методу __str__ для користувача
def test_user_str_representation():
    """Перевірка правильного рядкового представлення об'єкта користувача"""
    user = User(1, "Тест Юзер", "test@example.com", "0991234567")
    expected_str = "ID: 1, Ім'я: Тест Юзер, Email: test@example.com, Телефон: 0991234567"
    assert str(user) == expected_str


# Тест 5: Перевірка створення запису про видачу книги
def test_book_borrowing_creation():
    """Перевірка правильного створення запису про видачу книги"""
    borrow_date = "2023-01-01 12:00:00"
    borrowing = BookBorrowing(1, 1, borrow_date)
    assert borrowing.b_id == 1
    assert borrowing.u_id == 1
    assert borrowing.b_date == borrow_date
    assert borrowing.r_date is None
    assert borrowing.is_returned is False


# Тест 6: Перевірка методу __str__ для запису про видачу
def test_book_borrowing_str_representation():
    """Перевірка правильного рядкового представлення запису про видачу"""
    borrow_date = "2023-01-01 12:00:00"
    borrowing = BookBorrowing(1, 1, borrow_date)
    expected_str = "Книга ID: 1, Користувач ID: 1, Дата видачі: 2023-01-01 12:00:00, Статус: Не повернуто"
    assert str(borrowing) == expected_str

    # Перевірка з поверненою книгою
    borrowing.is_returned = True
    expected_str = "Книга ID: 1, Користувач ID: 1, Дата видачі: 2023-01-01 12:00:00, Статус: Повернуто"
    assert str(borrowing) == expected_str


# Тест 7: Перевірка додавання книги через функцію add_book
@patch('builtins.input', side_effect=['Нова книга тест', 'Тестовий автор', 'Фантастика', '2021'])
def test_add_book(mock_input):
    """Перевірка успішного додавання нової книги через функцію add_book"""
    initial_book_count = len(books)

    with captured_output():
        result = add_book()

    assert len(books) == initial_book_count + 1
    assert result.title == "Нова книга тест"
    assert result.author == "Тестовий автор"
    assert result.genre == "Фантастика"
    assert result.year == 2021
    assert result.available is True


# Тест 8: Перевірка обробки некоректного року в add_book
@patch('builtins.input', side_effect=['Тестова книга', 'Тестовий автор', 'Фантастика', 'не число'])
def test_add_book_invalid_year(mock_input):
    """Перевірка коректної обробки некоректного року при додаванні книги"""
    with captured_output():
        result = add_book()

    assert result.year == 2025  # Має використати значення за замовчуванням


# Тест 9: Перевірка додавання користувача через функцію add_user
@patch('builtins.input', side_effect=['Новий Тестовий', 'new.test@example.com', '0501234567'])
def test_add_user(mock_input):
    """Перевірка успішного додавання нового користувача через функцію add_user"""
    initial_user_count = len(users)

    with captured_output():
        result = add_user()

    assert len(users) == initial_user_count + 1
    assert result.name == "Новий Тестовий"
    assert result.email == "new.test@example.com"
    assert result.phone == "0501234567"


# Тест 10: Перевірка обробки некоректного email в add_user
@patch('builtins.input', side_effect=['Тест Без Email', 'неправильний_email', '0501234567'])
def test_add_user_invalid_email(mock_input):
    """Перевірка коректної обробки некоректного email при додаванні користувача"""
    with captured_output():
        result = add_user()

    assert result.email == "тест.без.email@example.com"  # Має згенерувати email


# Тест 11: Перевірка успішної видачі книги
@patch('builtins.input', side_effect=['1', '1'])
def test_borrow_book_success(mock_input):
    """Перевірка успішної видачі книги користувачу"""
    book = books[0]  # Перша тестова книга
    user = users[0]  # Перший тестовий користувач

    assert book.available is True
    initial_borrow_count = len(borrows)

    with captured_output():
        result = borrow_book()

    assert len(borrows) == initial_borrow_count + 1
    assert book.available is False
    assert book.times_borrowed == 1
    assert book.id in user.borrowed_books
    assert result.b_id == book.id
    assert result.u_id == user.id


# Тест 12: Перевірка невдалої видачі книги (книга вже видана)
@patch('builtins.input', side_effect=['1', '1'])
def test_borrow_book_already_borrowed(mock_input):
    """Перевірка обробки спроби видати книгу, яка вже видана"""
    book = books[0]
    book.available = False  # Книга вже видана

    with captured_output():
        result = borrow_book()

    assert result is None  # Має повернути None, бо книга недоступна


# Тест 13: Перевірка повернення книги
def test_return_book():
    """Перевірка успішного повернення книги"""
    # Спочатку видаємо книгу
    book = books[0]
    user = users[0]
    borrow_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_borrowing = BookBorrowing(book.id, user.id, borrow_date)
    borrows.append(new_borrowing)
    book.available = False
    user.borrowed_books.append(book.id)

    with patch('builtins.input', return_value='1'), captured_output():
        result = return_book()

    assert book.available is True
    assert book.id not in user.borrowed_books
    assert result.is_returned is True
    assert result.r_date is not None


# Тест 14: Перевірка пошуку книг за назвою
@patch('builtins.input', side_effect=['1', 'тестова'])
def test_search_books_by_title(mock_input):
    """Перевірка успішного пошуку книг за назвою"""
    with captured_output():
        results = search_books()

    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].title == "Тестова книга"


# Тест 15: Перевірка пошуку книг за автором
@patch('builtins.input', side_effect=['2', 'інший'])
def test_search_books_by_author(mock_input):
    """Перевірка успішного пошуку книг за автором"""
    with captured_output():
        results = search_books()

    assert len(results) == 1
    assert results[0].id == 2
    assert results[0].author == "Інший автор"


# Тест 16: Перевірка пошуку книг за жанром
@patch('builtins.input', side_effect=['3', 'Драма'])
def test_search_books_by_genre(mock_input):
    """Перевірка успішного пошуку книг за жанром"""
    with captured_output():
        results = search_books()

    assert len(results) == 1
    assert results[0].id == 2
    assert results[0].genre == "Драма"


# Тест 17: Перевірка пошуку книг за доступністю
@patch('builtins.input', side_effect=['4', '1'])
def test_search_books_by_availability(mock_input):
    """Перевірка успішного пошуку книг за доступністю"""
    with captured_output():
        results = search_books()

    assert len(results) == 2  # Обидві книги доступні

    # Встановлюємо першу книгу як видану
    books[0].available = False

    with patch('builtins.input', side_effect=['4', '2']), captured_output():
        results = search_books()

    assert len(results) == 1  # Тепер тільки одна книга видана
    assert results[0].id == 1


# Тест 18: Перевірка завантаження даних
@patch('os.path.exists', return_value=True)
@patch('builtins.open')
@patch('json.load')
def test_load_data(mock_json_load, mock_open, mock_exists):
    """Перевірка успішного завантаження даних"""
    books.clear()
    users.clear()
    borrows.clear()

    books_data = [
        {
            "id": 5,
            "title": "Тест книга",
            "author": "Тест автор",
            "genre": "Тест жанр",
            "year": 2022,
            "available": True,
            "times_borrowed": 0,
            "publisher": "Тест видавець",
            "page_count": 100,
            "description": "Тестовий опис"
        }
    ]
    users_data = []
    borrows_data = []

    mock_json_load.side_effect = [books_data, users_data, borrows_data]

    load_data()

    assert len(books) == 1
    assert books[0].id == 5
    assert books[0].title == "Тест книга"


# Тест 19: Перевірка збереження даних
@patch('builtins.open', new_callable=unittest.mock.mock_open)
def test_save_data(mock_open):
    """Перевірка успішного збереження даних"""
    books.append(Book(1, "Тестова книга", "Тестовий автор", "Фантастика", 2020))
    users.append(User(1, "Тест Юзер", "test@example.com", "0991234567"))

    with patch('json.dump') as mock_json_dump:
        save_data()
        # Перевіряємо, що json.dump викликався 3 рази (для books, users, borrows)
        assert mock_json_dump.call_count == 3


# Тест 20: Перевірка додавання тестових даних
def test_add_test_data():
    """Перевірка успішного додавання тестових даних"""
    books.clear()
    users.clear()

    _add_test_data()

    assert len(books) == 3
    assert len(users) == 2
    assert books[0].title == "Гаррі Поттер"
    assert users[0].name == "Іван Петренко"


if __name__ == '__main__':
    pytest.main(['-v', '--durations=0', __file__])
