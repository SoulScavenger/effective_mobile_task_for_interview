"""Основная логика программы."""
import json
import os

from library import Library
from constants import INDENT


def show_main_menu():
    """Отображение главного меню."""
    print(
        '=============Главное меню=============',
        '1. Добавить книгу',
        '2. Удалить книгу по id',
        '3. Найти книгу',
        '4. Отобразить список книг',
        '5. Изменить статус книги по id.',
        '6. Выйти из программы',
        sep='\n'
    )


def get_file_name() -> str:
    """Проверка имени файла."""
    file_name = input('Введите имя файла: ')
    while len(file_name.strip()) == 0:
        print(
            'Имя файла не может быть пустым...'
            'Пожалуйста, повторите ввод...',
            sep='\n')
        file_name = input('Введите имя файла: ')
    file_name += '.json'
    return file_name


def basic_functional(choice, library: Library):
    """Основной функционал библиотеки."""
    if choice == 1:
        library.add_book()
    elif choice == 2:
        library.delete_book()
    elif choice == 3:
        library.search_book()
    elif choice == 4:
        library.get_all_books()
    elif choice == 5:
        library.change_status_of_book()
    elif choice == 6:
        return False
    return True


def main():
    """Точка входа в программу."""
    file_name = get_file_name()
    path_to_file = os.path.join(os.getcwd(), file_name)
    if not os.path.lexists(path_to_file):
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump([{"next_id": 1, "books": []}], file, indent=INDENT)
    library = Library(file_name)
    is_program_active = True

    while is_program_active:
        show_main_menu()
        try:
            choice = int(input('Ваш выбор (Введите цифру согласно меню): '))
            if choice in range(1, 7):
                is_program_active = basic_functional(choice, library)
            else:
                raise ValueError
        except ValueError:
            print('Ошибка ввода... Ввод должен быть цифрой от 1 до 6...')
            continue


if __name__ == '__main__':
    main()
