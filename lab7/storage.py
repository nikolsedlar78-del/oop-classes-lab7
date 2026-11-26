"""Задача 7.3: інтерфейс Storage, MemoryStorage, CountingStorage, backup."""
from abc import ABC, abstractmethod


def _check_key(key):
    if not isinstance(key, str) or not key:
        raise ValueError("key must be a non-empty string")
    return key


class Storage(ABC):
    """Інтерфейс сховища «ключ → значення»."""

    @abstractmethod
    def save(self, key, value):
        """Зберігає значення (перезаписує існуюче)."""

    @abstractmethod
    def load(self, key):
        """Повертає значення; KeyError, якщо ключа немає."""

    @abstractmethod
    def delete(self, key):
        """Видаляє ключ; KeyError, якщо його немає."""

    @abstractmethod
    def keys(self):
        """Список ключів."""


class MemoryStorage(Storage):
    """Сховище в пам'яті (словник)."""

    def __init__(self):
        self._data = {}

    def save(self, key, value):
        self._data[_check_key(key)] = value

    def load(self, key):
        return self._data[_check_key(key)]

    def delete(self, key):
        del self._data[_check_key(key)]

    def keys(self):
        return list(self._data)


class CountingStorage(Storage):
    """Обгортка над будь-яким Storage, що рахує кожен виклик операцій."""

    OPS = ("save", "load", "delete", "keys")

    def __init__(self, inner):
        if not isinstance(inner, Storage):
            raise TypeError("inner must be a Storage")
        self._inner = inner
        self.counts = {op: 0 for op in self.OPS}

    @property
    def total(self):
        """Загальна кількість викликів."""
        return sum(self.counts.values())

    def save(self, key, value):
        self.counts["save"] += 1
        self._inner.save(key, value)

    def load(self, key):
        self.counts["load"] += 1
        return self._inner.load(key)

    def delete(self, key):
        self.counts["delete"] += 1
        self._inner.delete(key)

    def keys(self):
        self.counts["keys"] += 1
        return self._inner.keys()


def backup(src, dst):
    """Копіює всі пари з src у dst (перезаписує); повертає кількість ключів."""
    if not isinstance(src, Storage) or not isinstance(dst, Storage):
        raise TypeError("src and dst must be Storage instances")
    count = 0
    for key in src.keys():
        dst.save(key, src.load(key))
        count += 1
    return count
