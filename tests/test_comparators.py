"""
Тесты для компараторов сортировки атрибутов.
"""

import unittest
from smev_transform.attribute import Attribute
from smev_transform.comparators import AttributeSortingComparator


class TestAttributeSortingComparator(unittest.TestCase):
    """Тесты для сортировки атрибутов XML."""

    def test_compare_unqualified_attributes(self):
        """Тестирует сравнение неквалифицированных атрибутов."""
        attr1 = Attribute("attA", "aaa")
        attr2 = Attribute("attB", "bbb")

        result = AttributeSortingComparator.compare(attr1, attr2)
        self.assertEqual(-1, result)  # attA < attB

        result = AttributeSortingComparator.compare(attr2, attr1)
        self.assertEqual(1, result)  # attB > attA

    def test_compare_qualified_attributes(self):
        """Тестирует сравнение квалифицированных атрибутов."""
        attr1 = Attribute("attA", "aaa", "http://test/1")
        attr2 = Attribute("attB", "bbb", "http://test/2")

        result = AttributeSortingComparator.compare(attr1, attr2)
        self.assertEqual(-1, result)  # по namespace URI

    def test_compare_same_namespace_attributes(self):
        """Тестирует сравнение атрибутов с одинаковым namespace."""
        attr1 = Attribute("attA", "aaa", "http://test/1")
        attr2 = Attribute("attB", "bbb", "http://test/1")

        result = AttributeSortingComparator.compare(attr1, attr2)
        self.assertEqual(-1, result)  # по local name

    def test_compare_qualified_vs_unqualified(self):
        """Тестирует сравнение квалифицированного и неквалифицированного атрибутов."""
        qualified_attr = Attribute("attA", "aaa", "http://test/1")
        unqualified_attr = Attribute("attB", "bbb")

        # Квалифицированный должен быть перед неквалифицированным
        result = AttributeSortingComparator.compare(qualified_attr, unqualified_attr)
        self.assertEqual(-1, result)

        result = AttributeSortingComparator.compare(unqualified_attr, qualified_attr)
        self.assertEqual(1, result)

    def test_sort_attributes(self):
        """Тестирует полную сортировку списка атрибутов."""
        attributes = [
            Attribute("attB", "bbb"),  # unqualified
            Attribute("attA", "aaa"),  # unqualified
            Attribute("attZ", "zzz", "http://test/a"),  # qualified
            Attribute("attC", "ccc", "http://test/0"),  # qualified
            Attribute("attD", "ddd", "http://test/3"),  # qualified
            Attribute("attE", "eee", "http://test/3"),  # qualified
            Attribute("attF", "fff", "http://test/2"),  # qualified
        ]

        sorted_attributes = sorted(attributes, key=AttributeSortingComparator.get_sort_key())

        # Проверяем порядок: сначала qualified (по URI, затем по name), потом unqualified (по name)
        expected_order = [
            ("attC", "http://test/0"),  # http://test/0
            ("attF", "http://test/2"),  # http://test/2
            ("attD", "http://test/3"),  # http://test/3
            ("attE", "http://test/3"),  # http://test/3
            ("attZ", "http://test/a"),  # http://test/a
            ("attA", ""),  # unqualified
            ("attB", ""),  # unqualified
        ]

        for i, (expected_name, expected_uri) in enumerate(expected_order):
            self.assertEqual(expected_name, sorted_attributes[i].get_name())
            self.assertEqual(expected_uri, sorted_attributes[i].get_uri())


if __name__ == '__main__':
    unittest.main()