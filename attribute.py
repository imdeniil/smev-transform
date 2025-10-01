"""
Класс для описания XML атрибута.
"""

from typing import Optional


class Attribute:
    """Класс, описывающий атрибут XML."""

    def __init__(self, name: str, value: str, uri: Optional[str] = None, prefix: Optional[str] = None):
        """
        Инициализация XML атрибута.

        Args:
            name: Имя атрибута
            value: Значение атрибута
            uri: URI namespace атрибута (может быть None)
            prefix: Префикс namespace атрибута (может быть None)
        """
        self.name = name
        self.value = value
        self.uri = uri
        self.prefix = prefix

    def get_name(self) -> str:
        """Возвращает имя атрибута."""
        return self.name

    def get_value(self) -> str:
        """Возвращает значение атрибута."""
        return self.value

    def get_uri(self) -> str:
        """Возвращает URI namespace атрибута (пустую строку если None)."""
        return self.uri or ""

    def get_prefix(self) -> str:
        """Возвращает префикс namespace атрибута."""
        return self.prefix