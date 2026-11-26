"""Задача 7.2: шаблонний метод. Report.build() = шапка + рядки + підвал."""
from abc import ABC, abstractmethod

from .validation import require_str, require_number, require_int


class Report(ABC):
    """Абстрактний звіт. build() фіксує порядок, кроки задають нащадки."""

    def build(self):
        """Шаблонний метод: шапка, рядки, підвал."""
        lines = [self.header(), *self.rows(), self.footer()]
        return "\n".join(lines)

    @abstractmethod
    def header(self):
        """Шапка звіту."""

    @abstractmethod
    def rows(self):
        """Список рядків тіла звіту."""

    def footer(self):
        """Підвал за замовчуванням (нащадки можуть перевизначити)."""
        return "-- end of report --"


def _check_dict(data):
    if not isinstance(data, dict):
        raise TypeError("data must be a dict")


class SalesReport(Report):
    """Звіт про продажі: товар -> сума; у підвалі загальна сума."""

    def __init__(self, sales):
        _check_dict(sales)
        self.sales = {require_str(k, "product"): require_number(v, "amount", minimum=0)
                      for k, v in sales.items()}

    def header(self):
        return "Sales report"

    def rows(self):
        return [f"{name}: {amount:.2f}" for name, amount in self.sales.items()]

    def footer(self):
        return f"Total: {sum(self.sales.values()):.2f}"


class InventoryReport(Report):
    """Звіт про склад: товар -> кількість; підвал за замовчуванням."""

    def __init__(self, items):
        _check_dict(items)
        self.items = {require_str(k, "item"): require_int(v, "quantity", minimum=0)
                      for k, v in items.items()}

    def header(self):
        return "Inventory report"

    def rows(self):
        return [f"{name}: {qty} pcs" for name, qty in self.items.items()]
