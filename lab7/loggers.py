"""Задача 7.7: інтерфейс Logger, ListLogger, StreamLogger, NullLogger, OrderService."""
from abc import ABC, abstractmethod

LEVELS = ("INFO", "WARNING", "ERROR")


class Logger(ABC):
    """Інтерфейс логера."""

    @abstractmethod
    def log(self, level, msg):
        """Записує повідомлення рівня INFO / WARNING / ERROR."""

    @staticmethod
    def _validate(level, msg):
        if level not in LEVELS:
            raise ValueError(f"level must be one of {LEVELS}")
        if not isinstance(msg, str) or not msg:
            raise ValueError("msg must be a non-empty string")


class ListLogger(Logger):
    """Зберігає записи (level, msg) у списку records."""

    def __init__(self):
        self.records = []

    def log(self, level, msg):
        self._validate(level, msg)
        self.records.append((level, msg))


class StreamLogger(Logger):
    """Пише рядки `[LEVEL] msg` у потік (будь-який об'єкт із write())."""

    def __init__(self, stream):
        if not callable(getattr(stream, "write", None)):
            raise TypeError("stream must have a write() method")
        self._stream = stream

    def log(self, level, msg):
        self._validate(level, msg)
        self._stream.write(f"[{level}] {msg}\n")


class NullLogger(Logger):
    """Нічого не записує (але перевіряє дані)."""

    def log(self, level, msg):
        self._validate(level, msg)


class OrderError(ValueError):
    """Замовлення відхилено."""


class OrderService:
    """Приймає замовлення зі складу; залежить лише від абстракції Logger."""

    def __init__(self, logger, stock):
        if not isinstance(logger, Logger):
            raise TypeError("logger must be a Logger")
        self._logger = logger
        self._stock = dict(stock)
        self._next_id = 1

    def stock_of(self, item):
        """Залишок товару на складі."""
        return self._stock[item]

    def place_order(self, item, quantity):
        """Оформлює замовлення, повертає його номер; помилки логує й кидає OrderError."""
        try:
            self._check(item, quantity)
        except OrderError as e:
            self._logger.log("ERROR", f"Order rejected: {e}")
            raise
        self._stock[item] -= quantity
        order_id = self._next_id
        self._next_id += 1
        self._logger.log("INFO", f"Order #{order_id} placed: {item} x{quantity}")
        return order_id

    def _check(self, item, quantity):
        if not isinstance(item, str) or not item:
            raise OrderError("invalid item")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise OrderError("quantity must be a positive integer")
        if item not in self._stock:
            raise OrderError(f"unknown item '{item}'")
        if self._stock[item] < quantity:
            raise OrderError(f"not enough '{item}' in stock")
