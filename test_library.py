"""Тестирование."""
import json
import unittest

from constants import INDENT
from library import Library


class TestLibrary(unittest.TestCase):
    """Проверка класса Library."""

    @classmethod
    def setUpClass(cls):
        """Фикстуры."""
        with open('test.json', 'w', encoding='UTF-8') as file:
            json.dump([{"next_id": 1, "books": []}], file, indent=INDENT)
        cls.library = Library('test.json')

    def test_title(self):
        """Проверка метода задания названия книги."""
        act = TestLibrary.library.set_title('Война и мир')
        self.assertEqual(act, 'Война и мир', 'тест провален')

    def test_author(self):
        """Проверка метода задания автора книги."""
        act = TestLibrary.library.set_author('Лев Толстой')
        self.assertEqual(act, 'Лев Толстой', 'тест провален')

    def test_age(self):
        """Проверка метода задания даты публикации книги."""
        act = TestLibrary.library.set_year_book(2003)
        self.assertEqual(act, 2003, 'тест провален')

    def test_status(self):
        """Проверка метода задания статуса книги."""
        act = TestLibrary.library.set_status_book(1)
        self.assertEqual(act, 'в наличии', 'тест провален')


if __name__ == '__main__':
    unittest.main()
