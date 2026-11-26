import io
import pytest
from lab7.loggers import Logger, ListLogger, StreamLogger, NullLogger, OrderService, OrderError


def test_logger_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Logger()


def test_list_logger_stores_records():
    lg = ListLogger()
    lg.log("INFO", "hello")
    lg.log("ERROR", "boom")
    assert lg.records == [("INFO", "hello"), ("ERROR", "boom")]


def test_stream_logger_writes_to_stream():
    buf = io.StringIO()
    StreamLogger(buf).log("WARNING", "careful")
    assert buf.getvalue() == "[WARNING] careful\n"


def test_null_logger_accepts_and_discards():
    assert NullLogger().log("INFO", "x") is None


@pytest.mark.parametrize("cls", [ListLogger, NullLogger])
def test_invalid_level_and_message(cls):
    lg = cls()
    with pytest.raises(ValueError):
        lg.log("DEBUG", "x")
    with pytest.raises(ValueError):
        lg.log("INFO", "")
    with pytest.raises(ValueError):
        lg.log("INFO", None)


def test_stream_logger_needs_writable_stream():
    with pytest.raises(TypeError):
        StreamLogger(object())


def test_order_success_is_logged():
    lg = ListLogger()
    svc = OrderService(lg, {"apple": 5})
    assert svc.place_order("apple", 2) == 1
    assert lg.records == [("INFO", "Order #1 placed: apple x2")]
    assert svc.stock_of("apple") == 3


def test_order_ids_increment():
    svc = OrderService(NullLogger(), {"a": 10})
    assert [svc.place_order("a", 1), svc.place_order("a", 1)] == [1, 2]


def test_order_exact_stock_boundary():
    svc = OrderService(NullLogger(), {"a": 3})
    svc.place_order("a", 3)
    assert svc.stock_of("a") == 0


def test_order_failure_is_logged_and_raised():
    lg = ListLogger()
    svc = OrderService(lg, {"apple": 1})
    with pytest.raises(OrderError):
        svc.place_order("apple", 2)
    assert lg.records == [("ERROR", "Order rejected: not enough 'apple' in stock")]
    assert svc.stock_of("apple") == 1


@pytest.mark.parametrize("item,qty", [("pear", 1), ("", 1), (None, 1), ("apple", 0),
                                      ("apple", -1), ("apple", 1.5), ("apple", True)])
def test_invalid_orders_are_logged_as_errors(item, qty):
    lg = ListLogger()
    svc = OrderService(lg, {"apple": 5})
    with pytest.raises(ValueError):
        svc.place_order(item, qty)
    assert len(lg.records) == 1 and lg.records[0][0] == "ERROR"


def test_service_works_with_any_logger_implementation():
    buf = io.StringIO()
    for lg in (ListLogger(), StreamLogger(buf), NullLogger()):
        OrderService(lg, {"a": 1}).place_order("a", 1)
    assert "Order #1 placed" in buf.getvalue()


def test_service_requires_logger():
    with pytest.raises(TypeError):
        OrderService("not a logger", {})


@pytest.mark.parametrize("cls", [ListLogger, NullLogger])
def test_isinstance_logger(cls):
    assert isinstance(cls(), Logger)
