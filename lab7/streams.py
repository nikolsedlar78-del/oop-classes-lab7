"""Задача 7.10: інтерфейси Readable і Writable; MemoryFile, ReadOnlyFile, copy."""
from abc import ABC, abstractmethod


class Readable(ABC):
    """Інтерфейс читання."""

    @abstractmethod
    def read(self):
        """Повертає весь вміст як рядок."""


class Writable(ABC):
    """Інтерфейс запису."""

    @abstractmethod
    def write(self, text):
        """Дописує текст."""


def _check_text(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text


class MemoryFile(Readable, Writable):
    """Файл у пам'яті: читання та запис."""

    def __init__(self, content=""):
        self._content = _check_text(content)

    def read(self):
        return self._content

    def write(self, text):
        self._content += _check_text(text)


class ReadOnlyFile(Readable):
    """Файл лише для читання."""

    def __init__(self, content=""):
        self._content = _check_text(content)

    def read(self):
        return self._content


def copy(src, dst):
    """Копіює вміст src у dst; повертає кількість символів.

    TypeError, якщо src не Readable або dst не Writable.
    """
    if not isinstance(src, Readable):
        raise TypeError("src must be Readable")
    if not isinstance(dst, Writable):
        raise TypeError("dst must be Writable")
    text = src.read()
    dst.write(text)
    return len(text)
