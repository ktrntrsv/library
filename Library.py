from calendar import TextCalendar, Calendar, month_name
from collections import OrderedDict

from stepik_course_tasks.Books.Page_and_Book import *


class Person:
    """класс описывающий человека"""

    def __init__(self, name):
        self.name = name

    def set_bookmark(self, *args, **kwargs):
        raise NotImplementedError

    def get_bookmark(self, *args, **kwargs):
        raise NotImplementedError

    def del_bookmark(self, *args, **kwargs):
        raise NotImplementedError


class Reader:
    def read(self, book, num_page):
        """
        return:: str (content of a page {num_page})
        """
        return book[num_page].__str__()


class Writer:
    """
    return:: None
    """
    def write(self, book, num_page, text):
        book[num_page] += text


class AdvancedPerson(Person, Reader, Writer):
    """класс человека умеющего читать, писать, пользоваться закладками"""

    def set_bookmark(self, book, num_page):
        book.set_bookmark(self, num_page)

    def get_bookmark(self, book):
        book.get_bookmark(self)

    def del_bookmark(self, book, person):
        book.del_bookmark(person)

    @staticmethod
    def search(book, chapter):
        """
        return:: int (a number of first page of chapter)
        """
        if not isinstance(book[len(book)], PageTableContents):
            raise NotExistingExtensionError
        return book[len(book)].search(chapter)

    def read(self, book, page):
        """
        return:: str (content of a page)
        """
        if isinstance(page, str):
            return book[self.search(book, page)].__str__()
        elif isinstance(page, int):
            return book[page].__str__()
        else:
            raise TypeError

    def write(self, book, page, text):
        """
        return:: None
        """
        if isinstance(page, str):
            book[self.search(book, page)] += text
        elif isinstance(page, int):
            book[page] += text
        else:
            raise TypeError


class PageTableContents(Page):  # i think, it's ok

    def __init__(self, text=None, max_sign=2000):
        self.max_sign = max_sign
        self._table = text or ''
        if type(self._table) == str:
            self._table = self.generator_content_table_from_str_to_ordered_dict()

    def generator_content_table_from_str_to_ordered_dict(self):
        """
        return:: Ordered dict (content table {chapter: page}
        """
        if self._table == '':
            return OrderedDict()
        table = self._table.split("\n")
        chapters = [i.split(':')[0] for i in table[1:-1]]
        pages = [int(i.split(':')[1]) for i in table[1:-1]]
        return OrderedDict(zip(chapters, pages))

    def search(self, chapter):
        """
        Search a number of first page of chapter.
        If chapter not in book, raise PageNotFoundError
        returns:: int (number of page)
        """
        if chapter not in self._table:
            raise PageNotFoundError
        return self._table[chapter]

    def __str__(self):
        page = "TABLE OF CONTENT\n"
        if self._table == OrderedDict():
            return page
        for key, val in self._table.items():
            page += f"{key}:{val}\n"
        return page

    def __len__(self):
        return len(self.__str__())

    def __add__(self, other):
        raise PermissionDeniedError

    def __radd__(self, other):
        raise PermissionDeniedError

    def __iadd__(self, other):
        raise PermissionDeniedError


class CalendarBookmark:

    def __init__(self, label=None):
        self.bookmark = label or 0

    def __str__(self):
        return str(self.bookmark)

    def __get__(self, book, class_of_book):
        # print("__get__")
        return book.__dict__.get(self.bookmark) or 0

    def __set__(self, book, page):
        # print("__set__")
        if page < 1 or page > book.max_size:
            raise PageNotFoundError
        book.__dict__[self.bookmark] = page


class CalendarBook(Book):
    """Daily with bookmark"""

    bookmark = CalendarBookmark()

    def __init__(self, title: str, content=None):
        super().__init__(title)
        self._content = content or []
        self._calendar_pages = []
        self.generating_calendar_content()
        self._content_table = PageTableContents(self.generating_content_table())
        self._content.append(self._content_table)  # adding to book a page with table content
        self.max_size = len(self._content)

    def generating_calendar_content(self):
        """
        return:: None
        """
        for i in range(1, 13):
            self._content.append(TextCalendar(firstweekday=0).formatmonth(int(self.title), i))
            self._calendar_pages.append(len(self._content))
            for k in Calendar().itermonthdates(int(self.title), i):
                if k.month == i:
                    self._content.append(str(k))

    def generating_content_table(self):
        """
        Return:: ordered dict (content table)
        """
        list_of_months = [month_name[i] for i in range(1, 13)]
        list_of_pages = [i for i in self._calendar_pages]
        content_table = OrderedDict(zip(list_of_months, list_of_pages))
        return content_table

    @staticmethod
    def ordered_dict_to_str(ordered_dict):
        """
        return:: str
        """
        page = "TABLE OF CONTENT\n"
        for key, val in ordered_dict.items():
            page += f"{key}:{val}\n"
        return page
