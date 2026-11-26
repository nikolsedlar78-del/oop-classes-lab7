from collections.abc import Sequence
import pytest
from lab7.countdown import Countdown


def test_len_and_iteration():
    c = Countdown(3)
    assert len(c) == 3 and list(c) == [3, 2, 1]


def test_getitem_and_negative_index():
    c = Countdown(5)
    assert c[0] == 5 and c[4] == 1 and c[-1] == 1 and c[-5] == 5


def test_index_out_of_range():
    c = Countdown(3)
    with pytest.raises(IndexError):
        c[3]
    with pytest.raises(IndexError):
        c[-4]


def test_empty_countdown_boundary():
    c = Countdown(0)
    assert len(c) == 0 and list(c) == []
    with pytest.raises(IndexError):
        c[0]


def test_contains_for_free():
    c = Countdown(5)
    assert 3 in c and 0 not in c and 6 not in c


def test_index_for_free():
    c = Countdown(5)
    assert c.index(5) == 0 and c.index(1) == 4
    with pytest.raises(ValueError):
        c.index(10)


def test_count_for_free():
    c = Countdown(5)
    assert c.count(3) == 1 and c.count(99) == 0


def test_reversed_for_free():
    assert list(reversed(Countdown(3))) == [1, 2, 3]


def test_slicing():
    c = Countdown(5)
    assert c[1:3] == [4, 3] and c[::2] == [5, 3, 1]


def test_is_sequence_and_only_two_methods_defined():
    assert isinstance(Countdown(1), Sequence)
    own = {k for k, v in vars(Countdown).items() if callable(v) and not k.startswith("__init")}
    assert own == {"__len__", "__getitem__"}


def test_sequence_subclass_without_required_methods_cannot_be_instantiated():
    class Broken(Sequence):
        def __len__(self):
            return 0
    with pytest.raises(TypeError):
        Broken()


@pytest.mark.parametrize("bad", [-1, 2.5, "3", None, True])
def test_invalid_n(bad):
    with pytest.raises(ValueError):
        Countdown(bad)
