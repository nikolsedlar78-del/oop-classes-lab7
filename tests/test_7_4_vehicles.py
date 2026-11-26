import pytest
from lab7.vehicles import Vehicle, Car, Bicycle, Plane


def test_vehicle_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Vehicle()


def test_subclass_without_max_speed_cannot_be_instantiated():
    class NoSpeed(Vehicle):
        pass
    with pytest.raises(TypeError):
        NoSpeed()


@pytest.mark.parametrize("cls,speed", [(Car, 180), (Bicycle, 25), (Plane, 900)])
def test_max_speed(cls, speed):
    assert cls().max_speed == speed


def test_travel_time():
    assert Car().travel_time(360) == 2.0
    assert Bicycle().travel_time(50) == 2.0
    assert Plane().travel_time(1800) == 2.0


def test_travel_time_zero_distance_boundary():
    assert Car().travel_time(0) == 0


def test_plane_is_fastest():
    times = {type(v).__name__: v.travel_time(900) for v in (Car(), Bicycle(), Plane())}
    assert min(times, key=times.get) == "Plane"


def test_max_speed_is_read_only_property():
    with pytest.raises(AttributeError):
        Car().max_speed = 1


def test_custom_implementation_via_class_attribute():
    class Skate(Vehicle):
        max_speed = 20
    assert Skate().travel_time(40) == 2.0


@pytest.mark.parametrize("cls", [Car, Bicycle, Plane])
def test_isinstance_vehicle(cls):
    assert isinstance(cls(), Vehicle)


@pytest.mark.parametrize("bad", [-1, "10", None, float("nan")])
def test_invalid_distance(bad):
    with pytest.raises(ValueError):
        Car().travel_time(bad)


def test_non_positive_speed_is_rejected():
    class Broken(Vehicle):
        max_speed = 0
    with pytest.raises(ValueError):
        Broken().travel_time(10)
