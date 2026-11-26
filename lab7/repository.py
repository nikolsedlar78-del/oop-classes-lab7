"""Задача 7.6: інтерфейс Repository, InMemoryRepository, сутність Student."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .validation import require_str, require_int


@dataclass(frozen=True)
class Student:
    """Студент: id (>= 1) і ім'я."""

    id: int
    name: str

    def __post_init__(self):
        require_int(self.id, "id", minimum=1)
        require_str(self.name, "name")


class Repository(ABC):
    """Інтерфейс репозиторію сутностей з полем id."""

    @abstractmethod
    def add(self, entity):
        """Додає сутність; ValueError при дублікаті id."""

    @abstractmethod
    def get(self, id):
        """Повертає сутність; KeyError, якщо немає."""

    @abstractmethod
    def all(self):
        """Список усіх сутностей."""

    @abstractmethod
    def remove(self, id):
        """Видаляє сутність; KeyError, якщо немає."""


class InMemoryRepository(Repository):
    """Репозиторій студентів у пам'яті."""

    def __init__(self):
        self._items = {}

    def add(self, entity):
        if not isinstance(entity, Student):
            raise TypeError("only Student entities are supported")
        if entity.id in self._items:
            raise ValueError(f"duplicate id: {entity.id}")
        self._items[entity.id] = entity

    def get(self, id):
        return self._items[id]

    def all(self):
        return list(self._items.values())

    def remove(self, id):
        del self._items[id]

    def __len__(self):
        return len(self._items)
