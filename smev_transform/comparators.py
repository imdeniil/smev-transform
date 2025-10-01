"""
Компараторы для сортировки атрибутов XML.
"""

from functools import cmp_to_key
from .attribute import Attribute


class AttributeSortingComparator:
    """Компаратор для сортировки атрибутов XML."""

    @staticmethod
    def compare(attr1: Attribute, attr2: Attribute) -> int:
        """
        Сортировка атрибутов.

        Атрибуты должны быть отсортированы в алфавитном порядке:
        сначала по namespace URI (если атрибут - в qualified form),
        затем – по local name.
        Атрибуты в unqualified form после сортировки идут после атрибутов в qualified form.

        Args:
            attr1: Первый атрибут для сравнения
            attr2: Второй атрибут для сравнения

        Returns:
            int: -1 если attr1 < attr2, 0 если равны, 1 если attr1 > attr2
        """
        uri1 = attr1.get_uri()
        uri2 = attr2.get_uri()

        # оба атрибута - unqualified
        if not uri1 and not uri2:
            # сравнить имена атрибутов
            if attr1.get_name() < attr2.get_name():
                return -1
            elif attr1.get_name() > attr2.get_name():
                return 1
            else:
                return 0

        # оба атрибута qualified
        if uri1 and uri2:
            # сравнить namespace
            if uri1 < uri2:
                return -1
            elif uri1 > uri2:
                return 1
            else:
                # если namespace атрибутов одинаковые, то сравнить имена атрибутов
                if attr1.get_name() < attr2.get_name():
                    return -1
                elif attr1.get_name() > attr2.get_name():
                    return 1
                else:
                    return 0

        # один атрибут - qualified, другой - unqualified
        if not uri1:
            return 1
        else:
            return -1

    @staticmethod
    def get_sort_key():
        """Возвращает ключ для сортировки атрибутов."""
        return cmp_to_key(AttributeSortingComparator.compare)