"""Задача 7.8: Countdown на основі collections.abc.Sequence."""
from collections.abc import Sequence

from .validation import require_int


class Countdown(Sequence):
    """Послідовність n, n-1, ..., 1. Реалізовано лише __len__ і __getitem__;
    __iter__, __contains__, __reversed__, index() і count() надає Sequence.
    """

    def __init__(self, n):
        self._n = require_int(n, "n", minimum=0)

    def __len__(self):
        return self._n

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(self._n))]
        if index < 0:
            index += self._n
        if not 0 <= index < self._n:
            raise IndexError("Countdown index out of range")
        return self._n - index
