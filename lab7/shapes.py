"""Задача 7.1: абстрактний Shape і реалізації Rect, Circle."""
import math
from abc import ABC, abstractmethod

from .validation import require_number


class Shape(ABC):
    """Абстрактна фігура: area() і perimeter() обов'язкові, describe() готовий."""

    @abstractmethod
    def area(self):
        """Площа."""

    @abstractmethod
    def perimeter(self):
        """Периметр."""

    def describe(self):
        """Текстовий опис, що спирається лише на абстрактний інтерфейс."""
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Rect(Shape):
    """Прямокутник (сторони > 0)."""

    def __init__(self, width, height):
        self.width = require_number(width, "width", positive=True)
        self.height = require_number(height, "height", positive=True)

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    """Коло (радіус > 0)."""

    def __init__(self, radius):
        self.radius = require_number(radius, "radius", positive=True)

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius
