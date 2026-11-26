import pytest
from lab7.plugins import Plugin, PluginManager, UpperPlugin, StripPlugin, ExclaimPlugin


def test_plugin_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Plugin()


def test_subclass_without_name_cannot_be_instantiated():
    class NoName(Plugin):
        def run(self, data):
            return data
    with pytest.raises(TypeError):
        NoName()


def test_register_and_names():
    m = PluginManager()
    m.register(UpperPlugin)
    m.register(StripPlugin)
    assert m.names() == ["upper", "strip"]


def test_run_all_in_registration_order():
    m = PluginManager()
    for cls in (StripPlugin, UpperPlugin, ExclaimPlugin):
        m.register(cls)
    assert m.run_all("  hi ") == "HI!"


def test_order_changes_result():
    a, b = PluginManager(), PluginManager()
    for cls in (UpperPlugin, ExclaimPlugin):
        a.register(cls)
    for cls in (ExclaimPlugin, UpperPlugin):
        b.register(cls)
    assert a.run_all("x") == b.run_all("x") == "X!"
    class Twice(Plugin):
        name = "twice"
        def run(self, data):
            return data * 2
    a.register(Twice)
    assert a.run_all("x") == "X!X!"


def test_run_all_without_plugins_returns_data():
    assert PluginManager().run_all("same") == "same"


@pytest.mark.parametrize("bad", [str, int, object, "UpperPlugin", None, 5])
def test_register_rejects_non_plugin_classes(bad):
    with pytest.raises(TypeError):
        PluginManager().register(bad)


def test_register_rejects_instance():
    with pytest.raises(TypeError):
        PluginManager().register(UpperPlugin())


def test_register_rejects_abstract_plugin():
    with pytest.raises(TypeError):
        PluginManager().register(Plugin)


def test_duplicate_name_rejected():
    m = PluginManager()
    m.register(UpperPlugin)
    with pytest.raises(ValueError):
        m.register(UpperPlugin)


def test_register_works_as_decorator():
    m = PluginManager()

    @m.register
    class Reverse(Plugin):
        name = "reverse"

        def run(self, data):
            return data[::-1]

    assert issubclass(Reverse, Plugin) and m.run_all("abc") == "cba"


@pytest.mark.parametrize("cls", [UpperPlugin, StripPlugin, ExclaimPlugin])
def test_isinstance_plugin(cls):
    assert isinstance(cls(), Plugin)
