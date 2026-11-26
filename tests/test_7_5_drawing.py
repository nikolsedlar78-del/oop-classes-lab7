import pytest
from lab7.drawing import Drawable, Circle, Label, render_all


class Square:
    """Не має draw()."""


def test_protocol_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Drawable()


def test_classes_do_not_inherit_protocol():
    assert Drawable not in Circle.__mro__ and Drawable not in Label.__mro__


def test_structural_isinstance():
    assert isinstance(Circle(1), Drawable)
    assert isinstance(Label("x"), Drawable)
    assert not isinstance(Square(), Drawable)


def test_render_all_draws_only_drawables():
    items = [Circle(2), Square(), Label("hi"), 42, None]
    assert render_all(items) == ["Circle(r=2)", "Label: hi"]


def test_render_all_empty():
    assert render_all([]) == []


def test_render_all_nothing_drawable():
    assert render_all([Square(), "text"]) == []


def test_render_all_preserves_order():
    assert render_all([Label("b"), Label("a")]) == ["Label: b", "Label: a"]


def test_user_class_matching_protocol_is_accepted():
    class Dot:
        def draw(self):
            return "."
    assert render_all([Dot()]) == ["."]


def test_render_all_accepts_generator():
    assert render_all(Label(c) for c in "ab") == ["Label: a", "Label: b"]


@pytest.mark.parametrize("bad", [0, -1, "a", None])
def test_circle_invalid(bad):
    with pytest.raises(ValueError):
        Circle(bad)


@pytest.mark.parametrize("bad", ["", "  ", None, 5])
def test_label_invalid(bad):
    with pytest.raises(ValueError):
        Label(bad)
