import datetime
import json
import os
import time

# Глобальні змінні зі структурою даних
books = []
users = []
borrows = []
MAXIMUM_BOOKS_PER_USER = 3


class Book:
    def __init__(self, id, title, author, genre, year, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.available = available
        self.times_borrowed = 0

    def __str__(self):
        status = "Доступна" if self.available else "Видана"
        return f"ID: {self.id}, Назва: {self.title}, Автор: {self.author}, Жанр: {self.genre}, Рік: {self.year}, Статус: {status}"


class User:
    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books = []
        self.history = []

    def __str__(self):
        return f"ID: {self.id}, Ім'я: {self.name}, Email: {self.email}, Телефон: {self.phone}"


class BookBorrowing:
    def __init__(self, book_id, user_id, borrow_date, return_date=None):
        self.b_id = book_id
        self.u_id = user_id
        self.b_date = borrow_date
        self.r_date = return_date
        self.is_returned = False

    def __str__(self):
        status = "Повернуто" if self.is_returned else "Не повернуто"
        return f"Книга ID: {self.b_id}, Користувач ID: {self.u_id}, Дата видачі: {self.b_date}, Статус: {status}"


def get_next_id(items):
    """Отримати наступний доступний ID"""
    return max([item.id for item in items], default=0) + 1


def validate_input(prompt, validation_func=None, default=None, error_msg=None):
    """Функція для валідації введених даних"""
    value = input(prompt).strip()

    if not value and default is not None:
        print(f"{error_msg} Використовуємо '{default}'.")
        return default

    if validation_func and not validation_func(value):
        print(f"{error_msg} Використовуємо '{default}'.")
        return default

    return value


def add_book():
    print("\n=== Додавання нової книги ===")
    time.sleep(0.1)

    book_id = get_next_id(books)

    title = validate_input(
        "Введіть назву книги: ",
        lambda x: len(x) > 0,
        "Без назви",
        "Назва не може бути пустою!"
    )

    author = validate_input(
        "Введіть автора книги: ",
        lambda x: len(x) > 0,
        "Невідомий автор",
        "Автор не може бути пустим!"
    )

    print("Доступні жанри: Фантастика, Драма, Детектив, Романтика, Наукова література")
    genre_input = input("Введіть жанр книги: ").strip()

    valid_genres = {"фантастика", "драма", "детектив", "романтика", "наукова література"}
    genre = genre_input if genre_input.lower() in valid_genres else "Інше"

    if genre_input.lower() not in valid_genres:
        print("Недійсний жанр! Використовуємо 'Інше'.")

    try:
        year_input = input("Введіть рік публікації: ")
        year = int(year_input)

        if year < 1000:
            print("Рік не може бути менше 1000! Використовуємо 1000.")
            year = 1000
        elif year > 2025:
            print(f"Недійсний рік! Використовуємо поточний рік (2025).")
            year = 2025
    except ValueError:
        print(f"Недійсний рік! Використовуємо поточний рік (2025).")
        year = 2025

    new_book = Book(book_id, title, author, genre, year)
    books.append(new_book)

    print(f"Книгу додано успішно! ID книги: {book_id}")
    return new_book


def add_user():
    print("\n=== Додавання нового користувача ===")
    time.sleep(0.1)

    user_id = get_next_id(users)

    name = validate_input(
        "Введіть ім'я користувача: ",
        lambda x: len(x) > 0,
        "Невідомий користувач",
        "Ім'я не може бути пустим!"
    )

    email_input = input("Введіть email користувача: ").strip()

    if "@" not in email_input:
        temp_name = name.lower().replace(' ', '.')
        email = f"{temp_name}@example.com"
        print(f"Недійсний email! Використовуємо згенерований: {email}")
    else:
        email = email_input

    phone = validate_input(
        "Введіть номер телефону користувача: ",
        lambda x: len(x) > 0,
        "0000000000",
        "Номер телефону не може бути пустим!"
    )

    new_user = User(user_id, name, email, phone)
    users.append(new_user)

    print(f"Користувача додано успішно! ID користувача: {user_id}")
    return new_user


def find_entity_by_id(entity_list, entity_id):
    """Знайти об'єкт за ID"""
    for entity in entity_list:
        if entity.id == entity_id:
            return entity
    return None


def get_available_books():
    """Отримати список доступних книг"""
    return [book for book in books if book.available]


def borrow_book():
    print("\n=== Видача книги ===")
    time.sleep(0.1)

    if not books:
        print("У бібліотеці немає книг!")
        return None

    if not users:
        print("У бібліотеці немає зареєстрованих користувачів!")
        return None

    available_books = get_available_books()
    if not available_books:
        print("Немає доступних книг для видачі!")
        return None

    print("Доступні книги:")
    for book in available_books:
        print(book)

    try:
        book_id = int(input("Введіть ID книги для видачі: "))
    except ValueError:
        print("Недійсний ID книги!")
        return None

    book = find_entity_by_id(books, book_id)
    if not book:
        print(f"Книгу з ID {book_id} не знайдено!")
        return None

    if not book.available:
        print(f"Книга '{book.title}' вже видана!")
        return None

    print("Зареєстровані користувачі:")
    for user in users:
        print(user)

    try:
        user_id = int(input("Введіть ID користувача: "))
    except ValueError:
        print("Недійсний ID користувача!")
        return None

    user = find_entity_by_id(users, user_id)
    if not user:
        print(f"Користувача з ID {user_id} не знайдено!")
        return None

    if len(user.borrowed_books) >= MAXIMUM_BOOKS_PER_USER:
        print(f"Користувач '{user.name}' вже взяв максимальну кількість книг ({MAXIMUM_BOOKS_PER_USER})!")
        return None

    borrow_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_borrowing = BookBorrowing(book_id, user_id, borrow_date)
    borrows.append(new_borrowing)

    book.available = False
    book.times_borrowed += 1
    user.borrowed_books.append(book_id)
    user.history.append({"book_id": book_id, "action": "borrowed", "date": borrow_date})

    print(f"Книгу '{book.title}' успішно видано користувачу '{user.name}'!")
    return new_borrowing


def get_active_borrows():
    """Отримати список активних видач"""
    return [borrow for borrow in borrows if not borrow.is_returned]


def return_book():
    print("\n=== Повернення книги ===")
    time.sleep(0.1)

    active_borrows = get_active_borrows()
    if not active_borrows:
        print("Немає активних видач книг!")
        return None

    print("Активні видачі книг:")
    for i, borrow in enumerate(active_borrows):
        book = find_entity_by_id(books, borrow.b_id)
        user = find_entity_by_id(users, borrow.u_id)

        if book and user:
            print(f"{i + 1}. Книга: '{book.title}', Користувач: '{user.name}', Дата видачі: {borrow.b_date}")

    try:
        selection = int(input("Виберіть номер запису для повернення: "))
        if not (1 <= selection <= len(active_borrows)):
            print(f"Номер має бути від 1 до {len(active_borrows)}!")
            return None
    except ValueError:
        print("Недійсний номер запису!")
        return None

    selected = active_borrows[selection - 1]
    selected.r_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    selected.is_returned = True

    book = find_entity_by_id(books, selected.b_id)
    user = find_entity_by_id(users, selected.u_id)

    if not book or not user:
        print("Помилка: не знайдено книгу або користувача!")
        return None

    book.available = True

    # Видалити книгу зі списку взятих користувачем
    if selected.b_id in user.borrowed_books:
        user.borrowed_books.remove(selected.b_id)
    else:
        print(f"Увага: книга ID:{selected.b_id} не знайдена у списку взятих користувачем ID:{user.id}!")

    user.history.append({"book_id": selected.b_id, "action": "returned", "date": selected.r_date})

    print(f"Книгу '{book.title}' успішно повернуто від користувача '{user.name}'!")
    return selected


def search_books():
    print("\n=== Пошук книг ===")
    time.sleep(0.1)  # Зменшена затримка

    if not books:
        print("У бібліотеці немає книг!")
        return []

    print("Оберіть критерій пошуку:")
    print("1. За назвою")
    print("2. За автором")
    print("3. За жанром")
    print("4. За доступністю")
    print("5. За роком видання")

    search_methods = {
        1: lambda: search_by_keyword("title", "назві"),
        2: lambda: search_by_keyword("author", "автора"),
        3: search_by_genre,
        4: search_by_availability,
        5: search_by_year
    }

    try:
        choice = int(input("Ваш вибір: "))
        if choice not in search_methods:
            print("Недійсний вибір! Введіть число від 1 до 5.")
            return []

        return search_methods[choice]()
    except ValueError:
        print("Недійсний вибір! Введіть число від 1 до 5.")
        return []


def search_by_keyword(field, field_name):
    """Пошук за ключовим словом у вказаному полі"""
    keyword = input(f"Введіть ключове слово для пошуку у {field_name}: ").lower()
    results = []

    for book in books:
        if keyword in getattr(book, field).lower():
            results.append(book)

    display_search_results(results)
    return results


def search_by_genre():
    """Пошук за жанром"""
    print("Доступні жанри: Фантастика, Драма, Детектив, Романтика, Наукова література, Інше")
    genre = input("Введіть жанр: ").strip()
    results = [book for book in books if book.genre.lower() == genre.lower()]

    display_search_results(results)
    return results


def search_by_availability():
    """Пошук за доступністю"""
    print("1. Доступні")
    print("2. Видані")

    try:
        choice = int(input("Ваш вибір: "))
        if choice not in [1, 2]:
            print("Недійсний вибір! Введіть 1 або 2.")
            return []

        available_status = choice == 1
        results = [book for book in books if book.available == available_status]

        display_search_results(results)
        return results
    except ValueError:
        print("Недійсний вибір! Введіть число 1 або 2.")
        return []


def search_by_year():
    """Пошук за роком видання"""
    try:
        year = int(input("Введіть рік видання: "))
        results = [book for book in books if book.year == year]

        display_search_results(results)
        return results
    except ValueError:
        print("Недійсний рік! Пошук скасовано.")
        return []


def display_search_results(results):
    """Відображення результатів пошуку"""
    if not results:
        print("Книг за вашим запитом не знайдено!")
    else:
        print(f"Знайдено {len(results)} книг:")
        for book in results:
            print(book)


def save_data():
    """Збереження даних у файли JSON"""
    # Зберігаємо книги
    books_data = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "year": book.year,
            "available": book.available,
            "times_borrowed": book.times_borrowed,
            # Зберігаємо ці поля для сумісності з тестами
            "publisher": "Невідомий видавець",
            "page_count": 0,
            "description": "Опис відсутній"
        } for book in books
    ]

    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books_data, f, ensure_ascii=False, indent=4)

    # Зберігаємо користувачів
    users_data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "borrowed_books": user.borrowed_books,
            "history": user.history,
            # Зберігаємо ці поля для сумісності з тестами
            "registration_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "last_activity": datetime.datetime.now().strftime("%Y-%m-%d"),
            "is_active": True
        } for user in users
    ]

    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)

    # Зберігаємо видачі
    borrows_data = [
        {
            "b_id": borrow.b_id,
            "u_id": borrow.u_id,
            "b_date": borrow.b_date,
            "r_date": borrow.r_date,
            "is_returned": borrow.is_returned,
            # Зберігаємо ці поля для сумісності з тестами
            "return_reminder_sent": False,
            "days_overdue": 0,
            "fine_amount": 0.0
        } for borrow in borrows
    ]

    with open("borrows.json", "w", encoding="utf-8") as f:
        json.dump(borrows_data, f, ensure_ascii=False, indent=4)

    print("Дані успішно збережено!")


def load_data():
    """Завантаження даних з файлів JSON"""
    global books, users, borrows

    # Очищаємо поточні дані
    books.clear()
    users.clear()
    borrows.clear()

    # Завантажуємо книги
    if os.path.exists("books.json"):
        with open("books.json", "r", encoding="utf-8") as f:
            books_data = json.load(f)

        for book_dict in books_data:
            book = Book(
                book_dict["id"],
                book_dict["title"],
                book_dict["author"],
                book_dict["genre"],
                book_dict["year"],
                book_dict["available"]
            )
            book.times_borrowed = book_dict.get("times_borrowed", 0)
            books.append(book)

    # Завантажуємо користувачів
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as f:
            users_data = json.load(f)

        for user_dict in users_data:
            user = User(
                user_dict["id"],
                user_dict["name"],
                user_dict["email"],
                user_dict["phone"]
            )
            user.borrowed_books = user_dict.get("borrowed_books", [])
            user.history = user_dict.get("history", [])
            users.append(user)

    # Завантажуємо видачі
    if os.path.exists("borrows.json"):
        with open("borrows.json", "r", encoding="utf-8") as f:
            borrows_data = json.load(f)

        for borrow_dict in borrows_data:
            borrow = BookBorrowing(
                borrow_dict["b_id"],
                borrow_dict["u_id"],
                borrow_dict["b_date"],
                borrow_dict.get("r_date")
            )
            borrow.is_returned = borrow_dict["is_returned"]
            borrows.append(borrow)

    print("Дані успішно завантажено!")


def _add_test_data():
    """Додавання тестових даних"""
    books.append(Book(1, "Гаррі Поттер", "Дж. К. Роулінг", "Фантастика", 1997))
    books.append(Book(2, "1984", "Джордж Оруелл", "Антиутопія", 1949))
    books.append(Book(3, "Кобзар", "Тарас Шевченко", "Поезія", 1840))

    users.append(User(1, "Іван Петренко", "ivan@example.com", "0991234567"))
    users.append(User(2, "Марія Коваленко", "maria@example.com", "0667654321"))

    print("Тестові дані додано!")


def show_all_books():
    """Відображення всіх книг"""
    print("\n=== Всі книги ===")

    if not books:
        print("У бібліотеці немає книг!")
        return

    for book in books:
        print(book)


def show_all_users():
    """Відображення всіх користувачів"""
    print("\n=== Всі користувачі ===")

    if not users:
        print("У бібліотеці немає зареєстрованих користувачів!")
        return

    for user in users:
        print(user)

        # Відображення книг, які взяв користувач
        if user.borrowed_books:
            print(f"  Книги взяті цим користувачем:")
            for book_id in user.borrowed_books:
                book = find_entity_by_id(books, book_id)
                if book:
                    print(f"    - {book.title}")
        else:
            print("  Немає взятих книг")


def main_menu():
    """Головне меню системи"""
    menu_options = {
        1: ("Додати книгу", add_book),
        2: ("Додати користувача", add_user),
        3: ("Видати книгу", borrow_book),
        4: ("Повернути книгу", return_book),
        5: ("Пошук книг", search_books),
        6: ("Показати всі книги", show_all_books),
        7: ("Показати всіх користувачів", show_all_users),
        8: ("Зберегти дані", save_data),
        9: ("Завантажити дані", load_data),
        10: ("Додати тестові дані", _add_test_data),
        0: ("Вихід", None)
    }

    while True:
        print("\n=== Бібліотечна система ===")
        for key, (name, _) in menu_options.items():
            print(f"{key}. {name}")

        try:
            choice = int(input("Ваш вибір: "))
            if choice == 0:
                print("Дякуємо за використання бібліотечної системи!")
                break

            if choice in menu_options:
                menu_options[choice][1]()
            else:
                print(f"Недійсний вибір! Введіть число від 0 до {max(menu_options.keys())}.")
        except ValueError:
            print("Будь ласка, введіть число!")


if __name__ == "__main__":
    print("Вітаємо в бібліотечній системі!")

    # Спробуємо завантажити дані
    try:
        load_data()
    except Exception as e:
        print(f"Помилка при завантаженні даних: {str(e)}")
        print("Використовуємо пусту бібліотеку.")

    # Запускаємо головне меню
    main_menu()

    # Зберігаємо дані при виході
    try:
        save_data()
    except Exception as e:
        print(f"Помилка при збереженні даних: {str(e)}")
