import pytest
from lab7.repository import Repository, InMemoryRepository, Student


@pytest.fixture
def repo():
    return InMemoryRepository()


def test_repository_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Repository()


def test_add_and_get(repo):
    s = Student(1, "Ann")
    repo.add(s)
    assert repo.get(1) == s


def test_duplicate_id_value_error(repo):
    repo.add(Student(1, "Ann"))
    with pytest.raises(ValueError):
        repo.add(Student(1, "Bob"))
    assert len(repo) == 1


def test_all_in_insertion_order(repo):
    repo.add(Student(2, "Bob"))
    repo.add(Student(1, "Ann"))
    assert [s.name for s in repo.all()] == ["Bob", "Ann"]


def test_all_empty(repo):
    assert repo.all() == []


def test_all_returns_copy(repo):
    repo.add(Student(1, "Ann"))
    repo.all().clear()
    assert len(repo) == 1


def test_remove(repo):
    repo.add(Student(1, "Ann"))
    repo.remove(1)
    assert repo.all() == []


def test_get_and_remove_missing(repo):
    with pytest.raises(KeyError):
        repo.get(99)
    with pytest.raises(KeyError):
        repo.remove(99)


def test_can_reuse_id_after_remove(repo):
    repo.add(Student(1, "Ann"))
    repo.remove(1)
    repo.add(Student(1, "Bob"))
    assert repo.get(1).name == "Bob"


def test_isinstance_repository(repo):
    assert isinstance(repo, Repository)


def test_add_rejects_foreign_entity(repo):
    with pytest.raises(TypeError):
        repo.add({"id": 1})


def test_student_equality_and_immutability():
    assert Student(1, "Ann") == Student(1, "Ann")
    with pytest.raises(AttributeError):
        Student(1, "Ann").id = 5


@pytest.mark.parametrize("bad_id", [0, -1, "1", 1.5, None, True])
def test_student_invalid_id(bad_id):
    with pytest.raises(ValueError):
        Student(bad_id, "Ann")


@pytest.mark.parametrize("bad_name", ["", "  ", None, 5])
def test_student_invalid_name(bad_name):
    with pytest.raises(ValueError):
        Student(1, bad_name)
