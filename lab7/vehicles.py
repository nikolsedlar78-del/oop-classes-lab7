"""Задача 7.4: абстрактний Vehicle з властивістю max_speed."""
from abc import ABC, abstractmethod

from .validation import require_number


class Vehicle(ABC):
    """Транспорт: max_speed (км/год) — абстрактна властивість."""

    @property
    @abstractmethod
    def max_speed(self):
        """Максимальна швидкість, км/год."""

    def travel_time(self, km):
        """Час у дорозі в годинах (km >= 0)."""
        km = require_number(km, "km", minimum=0)
        speed = self.max_speed
        if speed <= 0:
            raise ValueError("max_speed must be positive")
        return km / speed


class Car(Vehicle):
    """Автомобіль: 180 км/год."""

    @property
    def max_speed(self):
        return 180


class Bicycle(Vehicle):
    """Велосипед: 25 км/год."""

    @property
    def max_speed(self):
        return 25


class Plane(Vehicle):
    """Літак: 900 км/год."""

    @property
    def max_speed(self):
        return 900
