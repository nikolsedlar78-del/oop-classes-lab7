import pytest
from lab7.streams import Readable, Writable, MemoryFile, ReadOnlyFile, copy


def test_interfaces_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Readable()
    with pytest.raises(TypeError):
        Writable()


def test_memory_file_read_write_append():
    f = MemoryFile("ab")
    f.write("cd")
    assert f.read() == "abcd"


def test_memory_file_implements_both():
    f = MemoryFile()
    assert isinstance(f, Readable) and isinstance(f, Writable)


def test_read_only_file_implements_only_readable():
    f = ReadOnlyFile("x")
    assert isinstance(f, Readable) and not isinstance(f, Writable)
    assert not hasattr(f, "write")


def test_copy_memory_to_memory():
    src, dst = MemoryFile("hello"), MemoryFile()
    assert copy(src, dst) == 5
    assert dst.read() == "hello"


def test_copy_from_read_only():
    dst = MemoryFile("> ")
    copy(ReadOnlyFile("data"), dst)
    assert dst.read() == "> data"


def test_copy_empty_boundary():
    dst = MemoryFile("keep")
    assert copy(MemoryFile(), dst) == 0
    assert dst.read() == "keep"


def test_copy_into_read_only_is_type_error():
    with pytest.raises(TypeError):
        copy(MemoryFile("x"), ReadOnlyFile())


@pytest.mark.parametrize("bad", ["text", None, 5, ["a"]])
def test_copy_rejects_non_readable_source(bad):
    with pytest.raises(TypeError):
        copy(bad, MemoryFile())


@pytest.mark.parametrize("bad", ["text", None, 5, []])
def test_copy_rejects_non_writable_target(bad):
    with pytest.raises(TypeError):
        copy(MemoryFile("x"), bad)


def test_failed_copy_does_not_modify_source():
    src = MemoryFile("x")
    with pytest.raises(TypeError):
        copy(src, ReadOnlyFile())
    assert src.read() == "x"


def test_invalid_text():
    with pytest.raises(TypeError):
        MemoryFile(5)
    with pytest.raises(TypeError):
        MemoryFile().write(None)
    with pytest.raises(TypeError):
        ReadOnlyFile(["a"])


def test_class_implementing_interface_incompletely_fails():
    class HalfWritable(Writable):
        pass
    with pytest.raises(TypeError):
        HalfWritable()
