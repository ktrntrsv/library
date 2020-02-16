from functools import total_ordering
from collections import defaultdict

from stepik_course_tasks.Books.Errors_hierarchy import *


@total_ordering
class Page:
    """класс страница"""

    def __init__(self, text: str = None, max_sign: int = 2000):
        self._text = '' if text is None else text
        self.max_sign = max_sign
        if not isinstance(self._text, str) or not isinstance(max_sign, int):
            raise TypeError
        if len(self._text) > self.max_sign:
            raise TooLongTextError

    @property
    def text(self):
        if not isinstance(self._text, str):
            raise TypeError

    def __len__(self):
        return len(self._text)

    def __str__(self):
        return self._text.__str__()

    def __add__(self, other):
        if len(self._text) + len(other) > self.max_sign:
            raise TooLongTextError
        self._text += other
        return self

    def __iadd__(self, other):
        return self.__add__(other)

    def __radd__(self, other):
        return other + self._text

    def __eq__(self, other):
        if isinstance(other, Page) or isinstance(other, str):
            return len(self) == len(other)
        else:
            raise TypeError

    def __lt__(self, other):
        if isinstance(other, Page) or isinstance(other, str):
            return len(self) < len(other)
        else:
            raise TypeError


@total_ordering
class Book:
    """класс книга"""

    bookmark = defaultdict(None)

    def __init__(self, title: str, content: list = None):
        self.title = title
        self._content = [] if content is None else content
        if not isinstance(self._content, list):
            raise TypeError
        for i in self._content:
            if not isinstance(i, Page):
                raise TypeError

    @property
    def content(self):
        if not isinstance(self._content, list):
            raise TypeError
        for i in self._content:
            if not isinstance(i, Page):
                raise TypeError
        return self._content

    def __len__(self):
        return len(self._content)

    def __getitem__(self, page):
        if not isinstance(page, int):
            raise TypeError
        if page < 1 or page > len(self._content):
            raise PageNotFoundError
        return self._content[page - 1]

    def __setitem__(self, page_number, page_content):
        if (page_number < 1 or
                page_number > len(self._content)):
            raise PageNotFoundError
        if not isinstance(page_number, int):
            raise TypeError
        new_page = Page(str(page_content))
        self._content[page_number - 1] = new_page

    def __eq__(self, other):
        if type(self) == Book and type(other) == Book:
            return len(self) == len(other)
        else:
            raise TypeError

    def __lt__(self, other):
        if type(self) == Book and type(other) == Book:
            return len(self) < len(other)
        else:
            raise TypeError
