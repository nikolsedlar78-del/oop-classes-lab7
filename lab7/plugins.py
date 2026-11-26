"""Задача 7.9: Plugin (ABC) і PluginManager."""
import inspect
from abc import ABC, abstractmethod


class Plugin(ABC):
    """Абстрактний плагін: ім'я та обробка даних."""

    @property
    @abstractmethod
    def name(self):
        """Унікальне ім'я плагіна."""

    @abstractmethod
    def run(self, data):
        """Обробляє дані й повертає результат."""


class UpperPlugin(Plugin):
    """Верхній регістр."""

    @property
    def name(self):
        return "upper"

    def run(self, data):
        return data.upper()


class StripPlugin(Plugin):
    """Прибирає крайні пробіли."""

    @property
    def name(self):
        return "strip"

    def run(self, data):
        return data.strip()


class ExclaimPlugin(Plugin):
    """Додає знак оклику."""

    @property
    def name(self):
        return "exclaim"

    def run(self, data):
        return data + "!"


class PluginManager:
    """Реєструє класи плагінів і застосовує їх по черзі."""

    def __init__(self):
        self._plugins = {}

    def register(self, plugin_cls):
        """Реєструє клас-нащадок Plugin (TypeError для іншого); повертає клас."""
        if not (isinstance(plugin_cls, type) and issubclass(plugin_cls, Plugin)):
            raise TypeError("only Plugin subclasses can be registered")
        if inspect.isabstract(plugin_cls):
            raise TypeError("abstract plugin class cannot be registered")
        instance = plugin_cls()
        if instance.name in self._plugins:
            raise ValueError(f"plugin '{instance.name}' is already registered")
        self._plugins[instance.name] = instance
        return plugin_cls

    def names(self):
        """Імена плагінів у порядку реєстрації."""
        return list(self._plugins)

    def run_all(self, data):
        """Пропускає дані через усі плагіни за порядком реєстрації."""
        for plugin in self._plugins.values():
            data = plugin.run(data)
        return data
