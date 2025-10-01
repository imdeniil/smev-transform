"""
Тесты для декодирования атрибутов.
"""

import unittest
from smev_transform.attribute_decoder import AttributeDecoder


class TestAttributeDecoder(unittest.TestCase):
    """Тесты для декодирования атрибутов согласно СМЭВ Шаг 9.2."""

    def test_unescape_and_normalize_whitespace(self):
        """Тестирует снятие экранирования и нормализацию пробельных символов."""
        # Тестируем финальный результат после всех преобразований
        test_cases = [
            ('&#xd;', ' '),  # &#xd; -> \r -> ' ' (пробел)
            ('&#13;', ' '),  # &#13; -> \r -> ' ' (пробел)
            ('&#10;', ' '),  # &#10; -> \n -> ' ' (пробел)
            ('&#xa;', ' '),  # &#xa; -> \n -> ' ' (пробел)
            ('&#x9;', ' '),  # &#x9; -> \t -> ' ' (пробел)
            ('&#9;', ' '),   # &#9; -> \t -> ' ' (пробел)
            ('\r', ' '),     # заменяется на пробел
            ('\r\n', ' '),   # заменяется на пробел
            ('\n', ' '),     # заменяется на пробел
            ('\t', ' '),     # заменяется на пробел
            ('&gt;', '>'),
            ('&lt;', '<'),
            ('&amp;', '&'),
            ('&apos;', "'"),
            ('&quot;', '"')
        ]

        for escaped, expected in test_cases:
            with self.subTest(escaped=escaped):
                result = AttributeDecoder._unescape_and_normalize_whitespace(escaped)
                self.assertEqual(expected, result)

    def test_encode_attribute(self):
        """Тестирует кодирование атрибутов."""
        # Таблица 9 - Правила кодирования атрибутов
        test_cases = [
            ('<', '&lt;'),
            ('&', '&amp;'),
            ('"', '&quot;'),
            ('\r', '&#xd;'),
            ('\n', '&#xa;'),
            ('\t', '&#x9;')
        ]

        for char, expected in test_cases:
            with self.subTest(char=char):
                result = AttributeDecoder._encode_attribute(char)
                self.assertEqual(expected, result)

    def test_decode_attribute_value_full_process(self):
        """Тестирует полный процесс декодирования атрибута."""
        # Тест с пробельными символами
        value = 'text\twith\r\nvarious\nwhitespace'
        result = AttributeDecoder.decode_attribute_value(value)
        # Все пробельные символы должны быть нормализованы к пробелам, а затем закодированы
        expected = 'text with various whitespace'
        self.assertEqual(expected, result)

        # Тест с экранированными символами
        value = '&lt;test&gt;&amp;&quot;'
        result = AttributeDecoder.decode_attribute_value(value)
        # Сначала снимаем экранирование, затем кодируем обратно
        expected = '&lt;test>&amp;&quot;'  # < кодируется, > НЕ кодируется, & и " кодируются
        self.assertEqual(expected, result)

        # Тест со сложным случаем
        value = 'value\twith\r"quotes"\nand<symbols>&amp;'
        result = AttributeDecoder.decode_attribute_value(value)
        # Ожидаем нормализацию пробелов и кодирование специальных символов
        expected = 'value with &quot;quotes&quot; and&lt;symbols>&amp;'  # > не кодируется в атрибутах
        self.assertEqual(expected, result)

    def test_whitespace_normalization(self):
        """Тестирует нормализацию пробельных символов."""
        # Различные комбинации пробельных символов
        test_cases = [
            ('\r\n', ' '),
            ('\r', ' '),
            ('\n', ' '),
            ('\t', ' '),
            ('\r\n\t \n\r', '     '),  # \r\n->space, \t->space, space, \n->space, \r->space
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=repr(input_text)):
                result = AttributeDecoder._unescape_and_normalize_whitespace(input_text)
                self.assertEqual(expected, result)

    def test_decode_empty_and_none(self):
        """Тестирует декодирование пустых и None значений."""
        self.assertEqual('', AttributeDecoder.decode_attribute_value(''))
        self.assertEqual(None, AttributeDecoder.decode_attribute_value(None))

    def test_complex_attribute_example(self):
        """Тестирует сложный пример из документации СМЭВ."""
        # Пример из документации: атрибут с различными символами
        value = '&gt;&gt; 2&gt;\r\n2&lt;&gt; 1&amp;8&gt;&gt;5&apos;0\n&quot; a'
        result = AttributeDecoder.decode_attribute_value(value)

        # После обработки все пробельные символы нормализуются,
        # экранирование снимается и символы кодируются заново
        expected = '>> 2> 2&lt;> 1&amp;8>>5\'0 &quot; a'
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()