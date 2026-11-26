"""Демонстрація лабораторної 7: запуск `python demo.py`."""
import io

from lab7.shapes import Shape, Rect, Circle
from lab7.reports import SalesReport, InventoryReport
from lab7.storage import MemoryStorage, CountingStorage, backup
from lab7.vehicles import Car, Bicycle, Plane
from lab7.drawing import Circle as DrawCircle, Label, render_all
from lab7.repository import InMemoryRepository, Student
from lab7.loggers import ListLogger, StreamLogger, NullLogger, OrderService, OrderError
from lab7.countdown import Countdown
from lab7.plugins import PluginManager, UpperPlugin, StripPlugin, ExclaimPlugin
from lab7.streams import MemoryFile, ReadOnlyFile, copy


def section(title):
    print(f"\n=== {title} ===")


section("7.1 Shape")
try:
    Shape()
except TypeError as e:
    print("TypeError:", e)
for s in (Rect(3, 4), Circle(1)):
    print(s.describe())

section("7.2 Report (template method)")
print(SalesReport({"apple": 10, "pear": 5.5}).build())
print()
print(InventoryReport({"bolt": 100, "nut": 0}).build())

section("7.3 Storage")
src = MemoryStorage()
src.save("a", 1)
src.save("b", 2)
dst = CountingStorage(MemoryStorage())
print("copied:", backup(src, dst), "| counts:", dst.counts)
try:
    dst.load("missing")
except KeyError as e:
    print("KeyError:", e)

section("7.4 Vehicle")
for v in (Car(), Bicycle(), Plane()):
    print(f"{type(v).__name__}: {v.max_speed} km/h, 360 km takes {v.travel_time(360):.2f} h")

section("7.5 Protocol Drawable")
print(render_all([DrawCircle(2), "not drawable", Label("Hi"), 42]))

section("7.6 Repository")
repo = InMemoryRepository()
repo.add(Student(1, "Ann"))
repo.add(Student(2, "Bob"))
try:
    repo.add(Student(1, "Clone"))
except ValueError as e:
    print("ValueError:", e)
print(repo.all())

section("7.7 Logger")
buf = io.StringIO()
for logger in (ListLogger(), StreamLogger(buf), NullLogger()):
    svc = OrderService(logger, {"apple": 2})
    svc.place_order("apple", 1)
    try:
        svc.place_order("apple", 5)
    except OrderError:
        pass
    print(type(logger).__name__, "->", getattr(logger, "records", "(see stream / nothing)"))
print("stream content:", repr(buf.getvalue()))

section("7.8 Countdown (Sequence)")
c = Countdown(5)
print(list(c), "| 3 in c:", 3 in c, "| index(2):", c.index(2), "| count(4):", c.count(4), "| reversed:", list(reversed(c)))

section("7.9 Plugins")
pm = PluginManager()
for cls in (StripPlugin, UpperPlugin, ExclaimPlugin):
    pm.register(cls)
print(pm.names(), "->", repr(pm.run_all("  hello ")))
try:
    pm.register(str)
except TypeError as e:
    print("TypeError:", e)

section("7.10 Readable / Writable")
out = MemoryFile()
print("copied chars:", copy(ReadOnlyFile("some text"), out), "->", repr(out.read()))
try:
    copy(MemoryFile("x"), ReadOnlyFile())
except TypeError as e:
    print("TypeError:", e)
