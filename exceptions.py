"""Кастомные исключения."""


class AddBookError(Exception):
    """Кастомное исключения для добавления книги."""


class DeleteBookError(Exception):
    """Кастомное исключения для удаления книги."""


class ChangeBookError(Exception):
    """Кастомное исключения для изменения книги."""
