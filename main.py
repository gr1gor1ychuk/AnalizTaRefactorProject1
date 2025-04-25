import datetime
import json
import os
import random
import time

# Глобальні змінні без належної структури збільшені в кількості
books = []
users = []
borrows = []
last_book_id = 0  # Dead Code - не використовується, але створює плутанину
last_user_id = 0  # Dead Code - не використовується, але створює плутанину
system_logs = []  # Dead Code - не використовується
MAXIMUM_BOOKS_PER_USER = 3  # Магічне число винесене в константу, але не використовується послідовно
DEFAULT_BORROWING_DAYS = 14  # Dead Code - не використовується

# Клас з надлишковими методами та неоптимальною структурою
class Book:
    def __init__(self, id, title, author, genre, year, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.available = available
        self.times_borrowed = 0
        # Додаткові непотрібні поля - Data Clumps
        self.publisher = "Невідомий видавець"  # Dead Code - не використовується
        self.page_count = 0  # Dead Code - не використовується
        self.description = "Опис відсутній"  # Dead Code - не використовується

    def __str__(self):
        avail = "Доступна" if self.available else "Видана"
        return f"ID: {self.id}, Назва: {self.title}, Автор: {self.author}, Жанр: {self.genre}, Рік: {self.year}, Статус: {avail}"

    # Надлишкові методи, які можуть бути частиною основного класу - Feature Envy
    def get_book_details(self):  # Dead Code - не використовується
        # Надлишковий коментар, який не пояснює що робить метод
        # Створює деталі для книги, які вже зберігаються в об'єкті
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "available": self.available,
            "times_borrowed": self.times_borrowed
        }

    def get_availability_text(self):  # Dead Code - не використовується але може створювати плутанину
        # Дублює логіку з __str__
        return "Доступна" if self.available else "Видана"

# Дублювання логіки в методах різних класів
class User:
    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books = []
        self.history = []
        # Додаткові непотрібні поля - Data Clumps
        self.registration_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Dead Code
        self.last_activity = datetime.datetime.now().strftime("%Y-%m-%d")  # Dead Code
        self.is_active = True  # Dead Code

    def __str__(self):
        return f"ID: {self.id}, Ім'я: {self.name}, Email: {self.email}, Телефон: {self.phone}"

    # Feature Envy - метод більше зацікавлений у класі Book
    def can_borrow_book(self, book_id):  # Dead Code - не використовується
        # Перевірка чи користувач може брати книгу
        # Магічне число 3 замість константи
        if len(self.borrowed_books) >= 3:
            return False

        # Дублює перевірку з borrow_book
        for book_id_in_list in self.borrowed_books:
            if book_id_in_list == book_id:
                return False

        return True

    # Duplicate Code - повторює логіку з borrow_book та return_book
    def get_current_borrows(self):  # Dead Code - не використовується
        borrowed_books_objects = []
        for book_id in self.borrowed_books:
            for book in books:  # Message Chain - доступ до глобальних даних
                if book.id == book_id:
                    borrowed_books_objects.append(book)
                    break
        return borrowed_books_objects

# Надлишковий клас з поганим іменуванням змінних
class BookBorrowing:
    def __init__(self, b_id, u_id, b_date, r_date=None):
        self.b_id = b_id  # Незрозуміле іменування
        self.u_id = u_id  # Незрозуміле іменування
        self.b_date = b_date  # Незрозуміле іменування
        self.r_date = r_date  # Незрозуміле іменування
        self.is_returned = False
        # Додаткові непотрібні поля - Data Clumps
        self.return_reminder_sent = False  # Dead Code
        self.days_overdue = 0  # Dead Code
        self.fine_amount = 0.0  # Dead Code

    def __str__(self):
        s = "Повернуто" if self.is_returned else "Не повернуто"
        return f"Книга ID: {self.b_id}, Користувач ID: {self.u_id}, Дата видачі: {self.b_date}, Статус: {s}"

    # Dead Code - не використовується, дублює логіку
    def calculate_overdue_days(self):
        if self.is_returned:
            return 0

        today = datetime.datetime.now()
        borrow_date = datetime.datetime.strptime(self.b_date, "%Y-%m-%d %H:%M:%S")
        # Магічне число 14 замість константи
        due_date = borrow_date + datetime.timedelta(days=14)

        if today > due_date:
            return (today - due_date).days
        return 0

    # Dead Code - не використовується, дублює логіку
    def calculate_fine(self):
        overdue_days = self.calculate_overdue_days()
        # Магічне число 0.5 - штраф за день прострочення
        return overdue_days * 0.5

# Функція з надмірно довгим кодом та поганою обробкою помилок
# Long Method - погіршуємо метод, додаючи більше коду і логіки
def add_book():
    print("\n=== Додавання нової книги ===")

    # Додаємо непотрібну затримку
    time.sleep(0.3)  # Магічне число

    # Дублюємо логіку багато разів
    # Магічні числа і відсутність валідації
    if len(books) > 0:
        book_id = books[-1].id + 1
    else:
        book_id = 1

    # Message Chain - зайві змінні у послідовностях операцій
    title_prompt = "Введіть назву книги: "
    title_input = input(title_prompt)
    title = title_input.strip()

    # Надлишкові перевірки, які нічого не роблять
    if len(title) == 0:
        print("Назва не може бути пустою! Використовуємо 'Без назви'.")
        title = "Без назви"

    # Message Chain - продовжуємо ланцюжок
    author_prompt = "Введіть автора книги: "
    author_input = input(author_prompt)
    author = author_input.strip()

    if len(author) == 0:
        print("Автор не може бути пустим! Використовуємо 'Невідомий автор'.")
        author = "Невідомий автор"

    print("Доступні жанри: Фантастика, Драма, Детектив, Романтика, Наукова література")
    genre_prompt = "Введіть жанр книги: "
    genre_input = input(genre_prompt)
    genre = genre_input.strip()

    # Повторюваний код для перевірки - Switch Statement без використання словника
    # Погіршуємо код, додаючи більше перевірок і не використовуючи словник
    valid_genre = False
    if genre == "Фантастика":
        valid_genre = True
    elif genre == "Драма":
        valid_genre = True
    elif genre == "Детектив":
        valid_genre = True
    elif genre == "Романтика":
        valid_genre = True
    elif genre == "Наукова література":
        valid_genre = True

    if not valid_genre:
        print("Недійсний жанр! Використовуємо 'Інше'.")
        genre = "Інше"

    # Незахищений код без належної обробки виключень
    try:
        year_prompt = "Введіть рік публікації: "
        year_input = input(year_prompt)
        year = int(year_input)

        # Multiple magic numbers
        if year < 1000:
            print(f"Рік не може бути менше 1000! Використовуємо 1000.")
            year = 1000
        elif year > 2030:
            print(f"Рік не може бути більше 2030! Використовуємо 2025.")
            year = 2025
        elif year > 2025:
            print(f"Недійсний рік! Використовуємо поточний рік (2025).")
            year = 2025
    except:  # Надто широкий обробник виключень
        print(f"Недійсний рік! Використовуємо поточний рік (2025).")
        year = 2025

    # Додамо непотрібну логіку, що заплутує код
    is_added = False
    new_book = None

    try:
        # Створення книги
        new_book = Book(book_id, title, author, genre, year)

        # Надлишкова логіка перед додаванням
        # Dead Code - не має жодного ефекту
        if new_book:
            if new_book.id > 0 and len(new_book.title) > 0:
                if new_book.year > 0:
                    books.append(new_book)
                    is_added = True

        if not is_added:
            books.append(new_book)

        print(f"Книгу додано успішно! ID книги: {book_id}")

        # Message Chain - додаємо у глобальний список
        # Feature Envy - метод зацікавлений у змінах глобальної змінної
        log_message = f"Додано книгу ID:{book_id}, '{title}' автора {author}"
        system_logs.append({"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": "add_book", "message": log_message})

    except Exception as e:
        print(f"Помилка при додаванні книги: {str(e)}")
        return None

    return new_book

# Функція з дублюванням коду з add_book, яку ми погіршуємо
# Long Method - робимо метод ще довшим і заплутанішим
def add_user():
    print("\n=== Додавання нового користувача ===")

    # Додаємо непотрібну затримку
    time.sleep(0.3)  # Магічне число

    # Дублювання логіки з add_book
    if len(users) > 0:
        user_id = users[-1].id + 1
    else:
        user_id = 1

    # Message Chain - зайві змінні у послідовностях операцій
    name_prompt = "Введіть ім'я користувача: "
    name_input = input(name_prompt)
    name = name_input.strip()

    # Дублюємо перевірки з add_book
    if len(name) == 0:
        print("Ім'я не може бути пустим! Використовуємо 'Невідомий користувач'.")
        name = "Невідомий користувач"

    # Message Chain - продовжуємо ланцюжок
    email_prompt = "Введіть email користувача: "
    email_input = input(email_prompt)
    email = email_input.strip()

    # Надмірно спрощена валідація
    if "@" not in email:
        # Duplicate Code - копіюємо код замість створення окремої функції
        temp_name = name.lower()
        temp_name = temp_name.replace(' ', '.')
        email = f"{temp_name}@example.com"
        print(f"Недійсний email! Використовуємо згенерований: {email}")

    # Message Chain
    phone_prompt = "Введіть номер телефону користувача: "
    phone_input = input(phone_prompt)
    phone = phone_input.strip()

    # Додаємо непотрібну валідацію
    if len(phone) == 0:
        phone = "0000000000"
        print(f"Номер телефону не може бути пустим! Використовуємо {phone}")

    # Додамо непотрібну логіку, що заплутує код
    is_added = False
    new_user = None

    try:
        # Створення користувача
        new_user = User(user_id, name, email, phone)

        # Надлишкова логіка перед додаванням
        # Dead Code - не має жодного ефекту
        if new_user:
            if new_user.id > 0 and len(new_user.name) > 0:
                if "@" in new_user.email:
                    users.append(new_user)
                    is_added = True

        if not is_added:
            users.append(new_user)

        print(f"Користувача додано успішно! ID користувача: {user_id}")

        # Message Chain - додаємо у глобальний список
        # Feature Envy - метод зацікавлений у змінах глобальної змінної
        log_message = f"Додано користувача ID:{user_id}, '{name}', email: {email}"
        system_logs.append({"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": "add_user", "message": log_message})

    except Exception as e:
        print(f"Помилка при додаванні користувача: {str(e)}")
        return None

    return new_user

# Функція з надмірною складністю і дублюванням коду
# Long Method - робимо метод ще довшим і складнішим
def borrow_book():
    print("\n=== Видача книги ===")

    # Непотрібна затримка
    time.sleep(0.3)  # Магічне число

    # Погана перевірка умов - дублювання коду з перевірками
    if len(books) == 0:
        print("У бібліотеці немає книг!")
        return None

    if len(users) == 0:
        print("У бібліотеці немає зареєстрованих користувачів!")
        return None

    # Неоптимальний код для пошуку доступних книг
    # Duplicate Code - повторюємо цикл замість того, щоб винести у метод
    print("Доступні книги:")
    available_count = 0
    available = []

    for b in books:
        if b.available:
            available.append(b)
            print(b)
            available_count += 1

    # Дублюємо умову перевірки
    if available_count == 0:
        print("Немає доступних книг для видачі!")
        return None

    # Відсутність валідації введення
    try:
        book_id_prompt = "Введіть ID книги для видачі: "
        book_id_input = input(book_id_prompt)
        book_id = int(book_id_input)
    except:
        print("Недійсний ID книги!")
        return None

    # Неефективний пошук - Duplicate Code
    # Повторюємо цикл замість того, щоб створити функцію пошуку
    book_found = None
    for b in books:
        if b.id == book_id:
            book_found = b
            break

    if book_found is None:
        print(f"Книгу з ID {book_id} не знайдено!")
        return None

    if not book_found.available:
        print(f"Книга '{book_found.title}' вже видана!")
        return None

    # Duplicate Code - повторюємо цикл виводу
    print("Зареєстровані користувачі:")
    for u in users:
        print(u)

    # Duplicate Code - дублювання коду для введення ID користувача
    try:
        user_id_prompt = "Введіть ID користувача: "
        user_id_input = input(user_id_prompt)
        user_id = int(user_id_input)
    except:
        print("Недійсний ID користувача!")
        return None

    # Duplicate Code - дублювання логіки пошуку
    user_found = None
    for u in users:
        if u.id == user_id:
            user_found = u
            break

    if user_found is None:
        print(f"Користувача з ID {user_id} не знайдено!")
        return None

    # Shotgun Surgery - створюємо умову, яку потрібно буде змінювати в багатьох місцях
    # Жорстко закодоване обмеження з повторенням магічного числа
    max_books = 3  # Магічне число
    if len(user_found.borrowed_books) >= max_books:
        print(f"Користувач '{user_found.name}' вже взяв максимальну кількість книг ({max_books})!")
        return None

    # Створення запису без перевірки
    borrow_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_borrowing = BookBorrowing(book_id, user_id, borrow_date)
    borrows.append(new_borrowing)

    # Shotgun Surgery - неатомарні операції, розкидані по коду
    book_found.available = False
    book_found.times_borrowed += 1
    user_found.borrowed_books.append(book_id)
    user_found.history.append({"book_id": book_id, "action": "borrowed", "date": borrow_date})

    # Message Chain - додаємо логування
    log_message = f"Книгу ID:{book_id} '{book_found.title}' видано користувачу ID:{user_id} '{user_found.name}'"
    system_logs.append({"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": "borrow_book", "message": log_message})

    print(f"Книгу '{book_found.title}' успішно видано користувачу '{user_found.name}'!")
    return new_borrowing

# Функція, що дублює логіку з borrow_book
# Long Method - робимо метод ще довшим і заплутанішим
def return_book():
    print("\n=== Повернення книги ===")

    # Непотрібна затримка
    time.sleep(0.3)  # Магічне число

    # Неефективний код фільтрації - Duplicate Code
    active = []
    for b in borrows:
        if not b.is_returned:
            active.append(b)

    if len(active) == 0:
        print("Немає активних видач книг!")
        return None

    # Duplicate Code - повторювана логіка виведення і пошуку
    print("Активні видачі книг:")
    for i, borrow in enumerate(active):
        book = None
        user = None

        # Неефективний пошук, що можна замінити на словники
        for b in books:
            if b.id == borrow.b_id:
                book = b
                break

        for u in users:
            if u.id == borrow.u_id:
                user = u
                break

        if book and user:
            print(f"{i + 1}. Книга: '{book.title}', Користувач: '{user.name}', Дата видачі: {borrow.b_date}")

    # Відсутність належної обробки помилок
    try:
        selection_prompt = "Виберіть номер запису для повернення: "
        selection_input = input(selection_prompt)
        selection = int(selection_input)

        # Перевірка валідності вибору з дублюванням
        if selection < 1:
            print("Номер запису не може бути менше 1!")
            return None

        if selection > len(active):
            print(f"Номер запису не може бути більше {len(active)}!")
            return None

    except:
        print("Недійсний номер запису!")
        return None

    # Вибір запису
    selected = active[selection - 1]
    selected.r_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    selected.is_returned = True

    # Duplicate Code - дублювання коду пошуку з попередньої секції
    book = None
    for b in books:
        if b.id == selected.b_id:
            book = b
            break

    user = None
    for u in users:
        if u.id == selected.u_id:
            user = u
            break

    if not book or not user:
        print("Помилка: не знайдено книгу або користувача!")
        return None

    # Неатомарні операції без перевірки на помилки - Shotgun Surgery
    book.available = True

    # Duplicate Code - дублюємо перевірку, яку можна було б винести в метод
    found_book_in_borrowed = False
    for i, borrowed_id in enumerate(user.borrowed_books):
        if borrowed_id == selected.b_id:
            user.borrowed_books.pop(i)
            found_book_in_borrowed = True
            break

    if not found_book_in_borrowed:
        print(f"Увага: книга ID:{selected.b_id} не знайдена у списку взятих користувачем ID:{user.id}!")

    user.history.append({"book_id": selected.b_id, "action": "returned", "date": selected.r_date})

    # Message Chain - додаємо логування
    log_message = f"Книгу ID:{selected.b_id} '{book.title}' повернуто від користувача ID:{user.id} '{user.name}'"
    system_logs.append({"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": "return_book", "message": log_message})

    print(f"Книгу '{book.title}' успішно повернуто від користувача '{user.name}'!")
    return selected

# Неефективна функція пошуку з дублюванням логіки
# Switch Statement - збільшуємо кількість і складність умов
def search_books():
    print("\n=== Пошук книг ===")

    # Непотрібна затримка
    time.sleep(0.3)  # Магічне число

    if len(books) == 0:
        print("У бібліотеці немає книг!")
        return []

    print("Оберіть критерій пошуку:")
    print("1. За назвою")
    print("2. За автором")
    print("3. За жанром")
    print("4. За доступністю")
    print("5. За роком видання")  # Додаємо новий пункт для ускладнення

    # Відсутність обробки виключень
    try:
        choice_prompt = "Ваш вибір: "
        choice_input = input(choice_prompt)
        choice = int(choice_input)
    except ValueError:
        print("Недійсний вибір! Введіть число від 1 до 5.")
        return []

    # Дублювання коду в кожному блоці умов - Switch Statement
    if choice == 1:
        keyword_prompt = "Введіть ключове слово для пошуку у назві: "
        keyword_input = input(keyword_prompt)
        keyword = keyword_input.lower()
        results = []

        # Неефективний цикл пошуку
        for book in books:
            book_title = book.title.lower()
            if keyword in book_title:
                results.append(book)

        # Вивід результатів
        if len(results) == 0:
            print("Книг за вашим запитом не знайдено!")
        else:
            print(f"Знайдено {len(results)} книг:")
            for book in results:
                print(book)

        return results

    elif choice == 2:
        # Дублювання логіки з першого блоку - Duplicate Code
        keyword_prompt = "Введіть ім'я автора: "
        keyword_input = input(keyword_prompt)
        keyword = keyword_input.lower()
        results = []

        for book in books:
            book_author = book.author.lower()
            if keyword in book_author:
                results.append(book)

        if len(results) == 0:
            print("Книг за вашим запитом не знайдено!")
        else:
            print(f"Знайдено {len(results)} книг:")
            for book in results:
                print(book)

        return results

    elif choice == 3:
        # Дублювання логіки з першого блоку - Duplicate Code
        print("Доступні жанри: Фантастика, Драма, Детектив, Романтика, Наукова література, Інше")
        genre_prompt = "Введіть жанр: "
        genre_input = input(genre_prompt)
        genre = genre_input.strip()
        results = []

        # Switch Statement - надмірно ускладнений умовний ланцюжок
        if genre.lower() == "фантастика":
            for book in books:
                if book.genre.lower() == "фантастика":
                    results.append(book)
        elif genre.lower() == "драма":
            for book in books:
                if book.genre.lower() == "драма":
                    results.append(book)
        elif genre.lower() == "детектив":
            for book in books:
                if book.genre.lower() == "детектив":
                    results.append(book)
        elif genre.lower() == "романтика":
            for book in books:
                if book.genre.lower() == "романтика":
                    results.append(book)
        elif genre.lower() == "наукова література":
            for book in books:
                if book.genre.lower() == "наукова література":
                    results.append(book)
        else:
            for book in books:
                if book.genre.lower() == "інше" or book.genre.lower() == genre.lower():
                    results.append(book)

        if len(results) == 0:
            print("Книг за вашим запитом не знайдено!")
        else:
            print(f"Знайдено {len(results)} книг:")
            for book in results:
                print(book)

        return results

    elif choice == 4:
        # Дублювання логіки з першого блоку - Duplicate Code
        print("1. Доступні")
        print("2. Видані")

        try:
            availability_choice_prompt = "Ваш вибір: "
            availability_choice_input = input(availability_choice_prompt)
            availability_choice = int(availability_choice_input)
        except ValueError:
            print("Недійсний вибір! Введіть число від 1 до 2.")
            return []

        results = []
        available_status = availability_choice == 1

        # Пошук книг за доступністю
        for book in books:
            if book.available == available_status:
                results.append(book)

        if len(results) == 0:
            print("Книг за вашим запитом не знайдено!")
        else:
            print(f"Знайдено {len(results)} книг:")
            for book in results:
                print(book)

        return results

    elif choice == 5:
        # Додаємо новий блок для пошуку за роком - Duplicate Code
        try:
            year_prompt = "Введіть рік видання: "
            year_input = input(year_prompt)
            year = int(year_input)
        except ValueError:
            print("Недійсний рік! Пошук скасовано.")
            return []

        results = []

        for book in books:
            if book.year == year:
                results.append(book)

        if len(results) == 0:
            print("Книг за вашим запитом не знайдено!")
        else:
            print(f"Знайдено {len(results)} книг:")
            for book in results:
                print(book)

        return results

    else:
        print("Недійсний вибір! Введіть число від 1 до 5.")
        return []


# Функція для збереження даних у файли JSON
def save_data():
    # Зберігаємо книги
    books_data = []
    for book in books:
        book_dict = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "year": book.year,
            "available": book.available,
            "times_borrowed": book.times_borrowed,
            "publisher": book.publisher,  # Dead Code - зберігаємо незадіяні поля
            "page_count": book.page_count,  # Dead Code
            "description": book.description  # Dead Code
        }
        books_data.append(book_dict)

    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books_data, f, ensure_ascii=False, indent=4)

    # Зберігаємо користувачів
    users_data = []
    for user in users:
        user_dict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "borrowed_books": user.borrowed_books,
            "history": user.history,
            "registration_date": user.registration_date,  # Dead Code
            "last_activity": user.last_activity,  # Dead Code
            "is_active": user.is_active  # Dead Code
        }
        users_data.append(user_dict)

    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)

    # Зберігаємо видачі
    borrows_data = []
    for borrow in borrows:
        borrow_dict = {
            "b_id": borrow.b_id,
            "u_id": borrow.u_id,
            "b_date": borrow.b_date,
            "r_date": borrow.r_date,
            "is_returned": borrow.is_returned,
            "return_reminder_sent": borrow.return_reminder_sent,  # Dead Code
            "days_overdue": borrow.days_overdue,  # Dead Code
            "fine_amount": borrow.fine_amount  # Dead Code
        }
        borrows_data.append(borrow_dict)

    with open("borrows.json", "w", encoding="utf-8") as f:
        json.dump(borrows_data, f, ensure_ascii=False, indent=4)

    print("Дані успішно збережено!")


# Функція для завантаження даних з файлів JSON
def load_data():
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
            # Встановлюємо додаткові поля, які не використовуються - Dead Code
            book.publisher = book_dict.get("publisher", "Невідомий видавець")
            book.page_count = book_dict.get("page_count", 0)
            book.description = book_dict.get("description", "Опис відсутній")
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
            # Встановлюємо додаткові поля, які не використовуються - Dead Code
            user.registration_date = user_dict.get("registration_date",
                                            datetime.datetime.now().strftime("%Y-%m-%d"))
            user.last_activity = user_dict.get("last_activity",
                                        datetime.datetime.now().strftime("%Y-%m-%d"))
            user.is_active = user_dict.get("is_active", True)
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
            # Встановлюємо додаткові поля, які не використовуються - Dead Code
            borrow.return_reminder_sent = borrow_dict.get("return_reminder_sent", False)
            borrow.days_overdue = borrow_dict.get("days_overdue", 0)
            borrow.fine_amount = borrow_dict.get("fine_amount", 0.0)
            borrows.append(borrow)

    print("Дані успішно завантажено!")


# Функція для додавання тестових даних
def _add_test_data():
    # Додамо тестові книги
    books.append(Book(1, "Гаррі Поттер", "Дж. К. Роулінг", "Фантастика", 1997))
    books.append(Book(2, "1984", "Джордж Оруелл", "Антиутопія", 1949))
    books.append(Book(3, "Кобзар", "Тарас Шевченко", "Поезія", 1840))

    # Додамо тестових користувачів
    users.append(User(1, "Іван Петренко", "ivan@example.com", "0991234567"))
    users.append(User(2, "Марія Коваленко", "maria@example.com", "0667654321"))

    print("Тестові дані додано!")


# Головне меню системи
def main_menu():
    while True:
        print("\n=== Бібліотечна система ===")
        print("1. Додати книгу")
        print("2. Додати користувача")
        print("3. Видати книгу")
        print("4. Повернути книгу")
        print("5. Пошук книг")
        print("6. Показати всі книги")
        print("7. Показати всіх користувачів")
        print("8. Зберегти дані")
        print("9. Завантажити дані")
        print("10. Додати тестові дані")
        print("0. Вихід")

        try:
            choice = int(input("Ваш вибір: "))
        except ValueError:
            print("Будь ласка, введіть число!")
            continue

        if choice == 1:
            add_book()
        elif choice == 2:
            add_user()
        elif choice == 3:
            borrow_book()
        elif choice == 4:
            return_book()
        elif choice == 5:
            search_books()
        elif choice == 6:
            show_all_books()
        elif choice == 7:
            show_all_users()
        elif choice == 8:
            save_data()
        elif choice == 9:
            load_data()
        elif choice == 10:
            _add_test_data()
        elif choice == 0:
            print("Дякуємо за використання бібліотечної системи!")
            break
        else:
            print("Недійсний вибір! Введіть число від 0 до 10.")


# Функція для відображення всіх книг
def show_all_books():
    print("\n=== Всі книги ===")

    if len(books) == 0:
        print("У бібліотеці немає книг!")
        return

    for book in books:
        print(book)


# Функція для відображення всіх користувачів
def show_all_users():
    print("\n=== Всі користувачі ===")

    if len(users) == 0:
        print("У бібліотеці немає зареєстрованих користувачів!")
        return

    for user in users:
        print(user)

        # Відображення книг, які взяв користувач
        if len(user.borrowed_books) > 0:
            print(f"  Книги взяті цим користувачем:")
            for book_id in user.borrowed_books:
                for book in books:
                    if book.id == book_id:
                        print(f"    - {book.title}")
                        break
        else:
            print("  Немає взятих книг")


# Стартова точка програми
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
