"""
Класс для описания XML namespace.
"""

from typing import Optional


class XmlNamespace:
    """Класс, описывающий namespace XML."""

    def __init__(self, uri: str, prefix: Optional[str] = None):
        """
        Инициализация XML namespace.

        Args:
            uri: URI namespace (не может быть пустым)
            prefix: Префикс namespace (может быть None)

        Raises:
            ValueError: Если передан пустой URI
        """
        if not uri:
            raise ValueError("Passed empty URI")

        self.prefix = prefix
        self.uri = uri

    def get_prefix(self) -> str:
        """Возвращает префикс namespace."""
        return self.prefix

    def get_uri(self) -> str:
        """Возвращает URI namespace."""
        return self.uri