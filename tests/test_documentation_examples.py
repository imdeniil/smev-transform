"""
Тесты примеров из документации СМЭВ Transform v2.0.

Этот файл содержит тесты, которые проверяют соответствие реализации
примерам, приведенным в документации README.md.
"""

import unittest
from smev_transform import Transform


class TestDocumentationExamples(unittest.TestCase):
    """Тесты примеров из документации."""

    def test_example_1_basic_transformation(self):
        """
        Тест примера 1: Базовая трансформация.

        Проверяет базовую функциональность трансформации XML с пространствами имен,
        включая сортировку атрибутов и генерацию префиксов.
        """
        # Исходный XML из документации
        src_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<elementOne xmlns="http://test/1" xmlns:qwe="http://test/2">
    <qwe:elementTwo attB="bbb" attA="aaa"/>
</elementOne>'''

        # Ожидаемый результат из документации
        expected_result = '<ns1:elementOne xmlns:ns1="http://test/1"><ns2:elementTwo xmlns:ns2="http://test/2" attA="aaa" attB="bbb"></ns2:elementTwo></ns1:elementOne>'

        # Выполняем трансформацию
        transform = Transform()
        result = transform.process(src_xml)

        # Проверяем соответствие документации
        self.assertEqual(expected_result, result)

    def test_example_2_text_escaping_step_91(self):
        """
        Тест примера 2: Обработка текста с экранированием (Шаг 9.1).

        Проверяет декодирование текстовых блоков согласно алгоритму СМЭВ.
        Исходный текст содержит экранированные символы, которые должны быть
        обработаны согласно шагу 9.1.
        """
        # Исходный XML из документации
        src_xml = '''<root>&gt;&gt;text&amp;content&lt;</root>'''

        # Выполняем трансформацию
        transform = Transform()
        result = transform.process(src_xml)

        # Анализируем что происходит:
        # 1. XML парсер: &gt;&gt;text&amp;content&lt; → >>text&content<
        # 2. Длина текста: 15 символов (больше 11) → применяются правила больших блоков
        # 3. Кодирование больших блоков:
        #    - > в начале → &gt;
        #    - > в середине → остается >
        #    - & → &amp;
        #    - < → &lt;
        expected_result = '<root>&gt;>text&amp;content&lt;</root>'

        self.assertEqual(expected_result, result)

    def test_example_3_attribute_whitespace_step_92(self):
        """
        Тест примера 3: Обработка атрибутов с пробелами (Шаг 9.2).

        Проверяет нормализацию пробельных символов в атрибутах согласно
        алгоритму СМЭВ шаг 9.2.
        """
        # Исходный XML из документации (с табуляцией и переводом строки)
        src_xml = '''<root attr="value\twith\ttabs and\nnewlines"/>'''

        # Выполняем трансформацию
        transform = Transform()
        result = transform.process(src_xml)

        # Анализируем обработку атрибута:
        # 1. Исходное значение: "value\twith\ttabs and\nnewlines"
        # 2. Нормализация: \t → пробел, \n → пробел
        # 3. Результат: "value with tabs and newlines"
        # 4. Кодирование: специальных символов нет, остается как есть
        expected_result = '<root attr="value with tabs and newlines"></root>'

        self.assertEqual(expected_result, result)

    def test_example_4_cdata_handling(self):
        """
        Тест примера 4: CDATA секции.

        Проверяет обработку CDATA секций. Следует отметить, что ElementTree
        автоматически обрабатывает CDATA и объединяет содержимое с текстом элемента.
        """
        # Исходный XML из документации
        src_xml = '''<root>
    Текст до CDATA
    <![CDATA[Сырой контент < & > остается нетронутым]]>
    Текст после CDATA
</root>'''

        # Выполняем трансформацию
        transform = Transform()
        result = transform.process(src_xml)

        # ElementTree автоматически обрабатывает CDATA, объединяя с текстом
        # Объединенный текст проходит через декодер текста (шаг 9.1)
        # Символы < и & кодируются, > остается как есть (не в начале и не после ])
        self.assertIn('Текст до CDATA', result)
        self.assertIn('Сырой контент', result)
        self.assertIn('Текст после CDATA', result)
        self.assertIn('&lt;', result)  # < кодируется
        self.assertIn('&amp;', result)  # & кодируется
        # > может остаться как есть в зависимости от позиции

    def test_complex_smev_scenario(self):
        """
        Тест комплексного сценария СМЭВ.

        Проверяет сложный случай, включающий все основные функции:
        - Множественные пространства имен
        - Сортировку атрибутов
        - Декодирование текста и атрибутов
        - Генерацию префиксов
        """
        src_xml = '''<?xml version="1.0"?>
<root xmlns="urn:test:main" xmlns:sec="urn:test:secondary">
    <sec:element attr2="value&amp;2" attr1="value\t1">
        Text with &lt;special&gt; chars &amp; more
    </sec:element>
</root>'''

        transform = Transform()
        result = transform.process(src_xml)

        # Проверяем основные ожидания
        self.assertIn('ns1:', result)  # Префиксы генерируются
        self.assertIn('ns2:', result)
        self.assertIn('attr1="value 1"', result)  # Табуляция нормализована в пробел
        self.assertIn('attr2="value&amp;2"', result)  # & остается закодированным в атрибутах
        self.assertIn('xmlns:ns1=', result)  # Декларации пространств имен
        self.assertIn('xmlns:ns2=', result)

        # Проверяем сортировку атрибутов (attr1 должен идти перед attr2)
        attr1_pos = result.find('attr1=')
        attr2_pos = result.find('attr2=')
        self.assertTrue(attr1_pos < attr2_pos, "Атрибуты должны быть отсортированы")


if __name__ == '__main__':
    unittest.main()