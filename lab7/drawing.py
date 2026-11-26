"""Задача 7.5: Protocol Drawable (структурна типізація, без наслідування)."""
from typing import Protocol, runtime_checkable

from .validation import require_str, require_number


@runtime_checkable
class Drawable(Protocol):
    """Протокол: усе, що має метод draw() -> str."""

    def draw(self) -> str:
        ...


class Circle:
    """Коло. Drawable не наслідує — відповідає протоколу структурно."""

    def __init__(self, radius):
        self.radius = require_number(radius, "radius", positive=True)

    def draw(self):
        return f"Circle(r={self.radius})"


class Label:
    """Текстова мітка (також без наслідування)."""

    def __init__(self, text):
        self.text = require_str(text, "text")

    def draw(self):
        return f"Label: {self.text}"


def render_all(items):
    """Малює лише об'єкти, що відповідають протоколу Drawable."""
    return [item.draw() for item in items if isinstance(item, Drawable)]
