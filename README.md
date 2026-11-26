# Лабораторна 7. Абстракції: ABC, Protocol та їхні реалізації

Python 3.10+, тести — `pytest`.

## Структура

| Задача | Модуль | Тести |
|---|---|---|
| 7.1 Shape (ABC) → Rect, Circle | `lab7/shapes.py` | `tests/test_7_1_shapes.py` |
| 7.2 Report (шаблонний метод) → SalesReport, InventoryReport | `lab7/reports.py` | `tests/test_7_2_reports.py` |
| 7.3 Storage → MemoryStorage, CountingStorage; `backup` | `lab7/storage.py` | `tests/test_7_3_storage.py` |
| 7.4 Vehicle (абстрактна властивість) → Car, Bicycle, Plane | `lab7/vehicles.py` | `tests/test_7_4_vehicles.py` |
| 7.5 Protocol Drawable; Circle, Label; `render_all` | `lab7/drawing.py` | `tests/test_7_5_drawing.py` |
| 7.6 Repository → InMemoryRepository, Student | `lab7/repository.py` | `tests/test_7_6_repository.py` |
| 7.7 Logger → List/Stream/Null; OrderService | `lab7/loggers.py` | `tests/test_7_7_loggers.py` |
| 7.8 Countdown (Sequence) | `lab7/countdown.py` | `tests/test_7_8_countdown.py` |
| 7.9 Plugin, PluginManager | `lab7/plugins.py` | `tests/test_7_9_plugins.py` |
| 7.10 Readable, Writable, MemoryFile, ReadOnlyFile, `copy` | `lab7/streams.py` | `tests/test_7_10_streams.py` |

## Запуск

```
pip install -r requirements.txt
python -m pytest -v
python demo.py
```

## Рішення, варті уваги

- У кожній задачі з ABC тест перевіряє, що абстракція не створюється (`TypeError`), а нащадок без усіх абстрактних членів теж не створюється.
- 7.2: `build()` — шаблонний метод; `header()` і `rows()` абстрактні, `footer()` має значення за замовчуванням, яке перевизначає лише `SalesReport`.
- 7.3: `CountingStorage` — обгортка (композиція), що сама є `Storage`; рахує кожен виклик, навіть невдалий. `load` і `delete` неіснуючого ключа дають `KeyError`.
- 7.4: `max_speed` — абстрактна `property`; нащадок може задати її й звичайним атрибутом класу. Швидкість ≤ 0 дає `ValueError`.
- 7.5: `Drawable` — `Protocol` з `@runtime_checkable`; `Drawable()` теж кидає `TypeError`. Перевірка `isinstance` дивиться лише на наявність методу `draw`, а не на його підпис.
- 7.6: `Student` — незмінний `dataclass` із валідацією; `id >= 1`. Додати можна лише `Student`.
- 7.7: `OrderService` залежить лише від `Logger`. Відхилене замовлення спочатку логується як `ERROR`, потім кидається `OrderError` (нащадок `ValueError`).
- 7.8: у `Countdown` визначені лише `__len__` і `__getitem__`; `in`, `index`, `count`, `reversed` надає `Sequence`. Додатково підтримано зрізи.
- 7.9: `register` приймає клас (не екземпляр), лише нащадка `Plugin` і не абстрактного; повертає клас, тож працює як декоратор. Дублікат імені — `ValueError`.
- 7.10: `copy` спершу перевіряє обидва типи й лише потім читає/пише, тому при `TypeError` нічого не змінюється.
