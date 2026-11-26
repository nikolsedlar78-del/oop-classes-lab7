import pytest
from lab7.storage import Storage, MemoryStorage, CountingStorage, backup


def test_storage_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Storage()


def test_memory_save_load():
    s = MemoryStorage()
    s.save("a", 1)
    assert s.load("a") == 1


def test_memory_overwrite():
    s = MemoryStorage()
    s.save("a", 1)
    s.save("a", 2)
    assert s.load("a") == 2 and s.keys() == ["a"]


def test_load_missing_key_error():
    with pytest.raises(KeyError):
        MemoryStorage().load("nope")


def test_delete():
    s = MemoryStorage()
    s.save("a", 1)
    s.delete("a")
    assert s.keys() == []
    with pytest.raises(KeyError):
        s.delete("a")


def test_keys_empty_and_order():
    s = MemoryStorage()
    assert s.keys() == []
    s.save("b", 1)
    s.save("a", 2)
    assert s.keys() == ["b", "a"]


@pytest.mark.parametrize("bad", ["", None, 5])
def test_invalid_key(bad):
    s = MemoryStorage()
    with pytest.raises(ValueError):
        s.save(bad, 1)
    with pytest.raises(ValueError):
        s.load(bad)


def test_counting_storage_counts_operations():
    c = CountingStorage(MemoryStorage())
    c.save("a", 1)
    c.save("b", 2)
    c.load("a")
    c.keys()
    c.delete("b")
    assert c.counts == {"save": 2, "load": 1, "delete": 1, "keys": 1}
    assert c.total == 5


def test_counting_storage_delegates():
    inner = MemoryStorage()
    c = CountingStorage(inner)
    c.save("a", 1)
    assert inner.load("a") == 1


def test_counting_counts_failed_calls_too():
    c = CountingStorage(MemoryStorage())
    with pytest.raises(KeyError):
        c.load("x")
    assert c.counts["load"] == 1


def test_counting_requires_storage():
    with pytest.raises(TypeError):
        CountingStorage({})


def test_isinstance_storage():
    assert isinstance(MemoryStorage(), Storage)
    assert isinstance(CountingStorage(MemoryStorage()), Storage)


def test_backup_copies_everything():
    src, dst = MemoryStorage(), MemoryStorage()
    src.save("a", 1)
    src.save("b", [2])
    assert backup(src, dst) == 2
    assert dst.load("a") == 1 and dst.load("b") == [2]


def test_backup_empty_source():
    dst = MemoryStorage()
    assert backup(MemoryStorage(), dst) == 0 and dst.keys() == []


def test_backup_overwrites_destination():
    src, dst = MemoryStorage(), MemoryStorage()
    src.save("a", "new")
    dst.save("a", "old")
    backup(src, dst)
    assert dst.load("a") == "new"


def test_backup_works_with_counting_wrapper():
    src, dst = MemoryStorage(), CountingStorage(MemoryStorage())
    src.save("a", 1)
    src.save("b", 2)
    backup(src, dst)
    assert dst.counts["save"] == 2


def test_backup_rejects_non_storage():
    with pytest.raises(TypeError):
        backup({}, MemoryStorage())
    with pytest.raises(TypeError):
        backup(MemoryStorage(), [])
