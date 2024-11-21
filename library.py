"""Класс Библиотека."""
import json
from functools import wraps

from constants import END_YEAR, INDENT, START_YEAR
from exceptions import AddBookError, ChangeBookError, DeleteBookError


def print_string_result(func):
    """Вывод доп. строки."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('=============Результат================')
        return func(*args, **kwargs)
    return wrapper


class Library:
    """Класс Библиотека."""

    def __init__(self, file_name):
        """Конструктор класса."""
        self.__file_name = file_name
        self.__next_book_id, self.__books = self.read_data_from_file()

    def read_data_from_file(self):
        """Чтение данных из файла."""
        try:
            with open(self.__file_name, 'r', encoding='UTF-8') as file:
                books_info = json.load(file)
                return books_info[0]['next_id'], books_info[0]['books']
        except IOError as err:
            print(f"Что-то пошло не так... Ошибка: {err}")

    def write_data_to_file(self):
        """Запись данных в файл."""
        try:
            with open(self.__file_name, 'w', encoding='UTF-8') as file:
                json.dump(
                    [{"next_id": self.__next_book_id, "books": self.__books}],
                    file,
                    indent=INDENT
                )
        except IOError as err:
            print(f"Что-то пошло не так... Ошибка: {err}")

    @print_string_result
    def add_book(self):
        """Добавление новой книги."""
        book = {
            'id': self.__next_book_id,
            'title': self.set_title(input('Введите название книги: ')),
            'author': self.set_author(input('Введите автора книги: ')),
            'year': self.set_year_book(input('Введите год издания книги: ')),
            'status': self.set_status_book(
                input('Введите статус книги: 1 - в наличии/0 - выдана: ')
                )
        }
        self.__books.append(book)
        self.__next_book_id += 1

        self.write_data_to_file()
        if self.__books != self.read_data_from_file()[-1]:
            raise AddBookError('Ошибка добавления книги в файл.')
        print('Книга успешно добавлена!')

    def get_book(self, book):
        """Отображение информации о книге."""
        for col_name, value in book.items():
            print(col_name, value, sep=': ')

    @print_string_result
    def get_all_books(self):
        """Отображение информации о всех книгах."""
        if len(self.__books) == 0:
            print('Список книг пуст...')
        else:
            for book in self.__books:
                self.get_book(book)
                print('======================================')

    @print_string_result
    def change_status_of_book(self):
        """Изменение статуса книги."""
        book_id = self.get_book_by_id()
        if book_id is None:
            print('Книга не найдена...')
        else:
            self.__books[book_id]['status'] = self.set_status_book()
            self.write_data_to_file()
            if self.__books != self.read_data_from_file()[-1]:
                raise ChangeBookError('Ошибка изменения статуса книги.')
            print('Статус книги успешно изменён!')

    def delete_book(self):
        """Удаление книги."""
        book_id = self.get_book_by_id()
        if book_id is None:
            print('Книга не найдена...')
        else:
            self.__books.pop(book_id)
            self.write_data_to_file()
            if self.__books != self.read_data_from_file()[-1]:
                raise DeleteBookError('Ошибка удаления книги из файла.')
            print('Книга успешно удалена!')

    def get_book_by_id(self):
        """Получения книги по id."""
        book_id = int(input('Введите id книги: '))
        for book in self.__books:
            if book['id'] == book_id:
                return self.__books.index(book)

    def set_title(self, title):
        """Задание названия книги."""
        while True:
            try:
                # title = input('Введите название книги: ')
                if len(title.strip()) == 0:
                    raise ValueError
                return title.capitalize()
            except ValueError:
                print('Название книги не может быть пустым...')
                continue

    def set_author(self, author):
        """Задание автора книги."""
        while True:
            try:
                # author = input('Введите автора книги: ')
                if len(author.strip()) == 0:
                    raise ValueError
                return author.title()
            except ValueError:
                print('Имя автора книги не может быть пустым...')
                continue

    def set_year_book(self, year):
        """Задание года издания книги."""
        while True:
            try:
                year = int(year)
                if year in range(START_YEAR, END_YEAR):
                    return year

                raise ValueError
            except ValueError:
                print(
                    'Ошибка ввода... '
                    'Год издания должен быть в диапазоне с 1457 по 2024 '
                )
                continue

    def set_status_book(self, status):
        """Задание статуса книги."""
        while True:
            try:
                status = int(status)
                if status == 1:
                    return 'в наличии'
                elif status == 0:
                    return 'выдана'
                raise ValueError
            except ValueError:
                print('Ошибка ввода...')
                continue

    def search_book(self):
        """Поиск книг."""
        search_field = input('Введите критерий поиска: ').lower()
        found_books = []
        for book in self.__books:
            if (
                search_field in book['title'].lower()
                or search_field in book['author'].lower()
                or search_field in str(book['year'])
            ):
                found_books.append(book)
        if len(found_books) > 0:
            for book in found_books:
                self.get_book(book)
                print('======================================')
        else:
            print('По такому критерию книг не найдено...')
