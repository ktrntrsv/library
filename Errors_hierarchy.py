class BookIOErrors(Exception):
    """базовый класс исключений для работы с книгой"""


class PageNotFoundError(BookIOErrors):
    """имя не существует"""


class TooLongTextError(BookIOErrors):
    """слишком большой текст, не поместится на странице"""


class PermissionDeniedError(BookIOErrors):
    """операция не позволяется"""


class NotExistingExtensionError(BookIOErrors):
    """вызываемый метод не существует"""
