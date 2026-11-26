import math
import pytest
from lab7.shapes import Shape, Rect, Circle


def test_shape_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Shape()


def test_subclass_missing_method_cannot_be_instantiated():
    class Incomplete(Shape):
        def area(self):
            return 1
    with pytest.raises(TypeError):
        Incomplete()


def test_rect():
    r = Rect(3, 4)
    assert r.area() == 12 and r.perimeter() == 14


def test_circle():
    c = Circle(1)
    assert c.area() == pytest.approx(math.pi)
    assert c.perimeter() == pytest.approx(2 * math.pi)


def test_describe_rect():
    assert Rect(3, 4).describe() == "Rect: area=12.00, perimeter=14.00"


def test_describe_circle():
    assert Circle(1).describe() == "Circle: area=3.14, perimeter=6.28"


def test_describe_works_for_custom_implementation():
    class Unit(Shape):
        def area(self):
            return 1
        def perimeter(self):
            return 4
    assert Unit().describe() == "Unit: area=1.00, perimeter=4.00"


@pytest.mark.parametrize("obj", [Rect(1, 1), Circle(1)])
def test_isinstance_shape(obj):
    assert isinstance(obj, Shape)


def test_float_sides():
    assert Rect(0.5, 2).area() == pytest.approx(1.0)


@pytest.mark.parametrize("bad", [0, -1, "a", None, float("inf")])
def test_circle_invalid(bad):
    with pytest.raises(ValueError):
        Circle(bad)


def test_rect_invalid():
    with pytest.raises(ValueError):
        Rect(0, 5)
    with pytest.raises(ValueError):
        Rect(5, -1)
