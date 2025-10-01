"""
Тесты для декодирования текстовых блоков.
"""

import unittest
from smev_transform.text_decoder import TextDecoder


class TestTextDecoder(unittest.TestCase):
    """Тесты для декодирования текстовых блоков согласно СМЭВ Шаг 9.1."""

    def test_unescape_text(self):
        """Тестирует снятие экранирования символов."""
        # Тестируем финальный результат после всех преобразований
        test_cases = [
            ('&#xd;', '\n'),  # &#xd; -> \r -> \n
            ('&#13;', '\n'),  # &#13; -> \r -> \n
            ('&#10;', '\n'),
            ('&#xa;', '\n'),
            ('&#x9;', '\t'),
            ('&#9;', '\t'),
            ('\r', '\n'),
            ('\r\n', '\n'),
            ('&gt;', '>'),
            ('&lt;', '<'),
            ('&amp;', '&'),
            ('&apos;', "'"),
            ('&quot;', '"')
        ]

        for escaped, expected in test_cases:
            with self.subTest(escaped=escaped):
                result = TextDecoder._unescape_text(escaped)
                self.assertEqual(expected, result)

    def test_split_cdata_blocks(self):
        """Тестирует разделение блоков с CDATA."""
        # Текст без CDATA
        text = "simple text"
        blocks = TextDecoder._split_cdata_blocks(text)
        self.assertEqual(1, len(blocks))
        self.assertEqual('text', blocks[0]['type'])
        self.assertEqual(text, blocks[0]['content'])

        # Текст с одним CDATA
        text = 'before<![CDATA[cdata content]]>after'
        blocks = TextDecoder._split_cdata_blocks(text)
        self.assertEqual(3, len(blocks))
        self.assertEqual('text', blocks[0]['type'])
        self.assertEqual('before', blocks[0]['content'])
        self.assertEqual('cdata', blocks[1]['type'])
        self.assertEqual('<![CDATA[cdata content]]>', blocks[1]['content'])
        self.assertEqual('text', blocks[2]['type'])
        self.assertEqual('after', blocks[2]['content'])

    def test_encode_small_block(self):
        """Тестирует кодирование малых блоков (до 11 символов)."""
        # Символы которые кодируются всегда
        self.assertEqual('&lt;', TextDecoder._encode_small_block('<'))
        self.assertEqual('&amp;', TextDecoder._encode_small_block('&'))
        self.assertEqual('&#xd;', TextDecoder._encode_small_block('\r'))

        # Тест кодирования '>' в начале блока
        self.assertEqual('&gt;', TextDecoder._encode_small_block('>'))

        # Тест кодирования '>' после ']'
        self.assertEqual(']&gt;', TextDecoder._encode_small_block(']>'))

        # Тест '>' в середине (не кодируется)
        self.assertEqual('a>b', TextDecoder._encode_small_block('a>b'))

    def test_encode_large_block_conditions(self):
        """Тестирует условия кодирования '>' для больших блоков."""
        # '>' в начале блока
        result = TextDecoder._encode_gt_large('>test')
        self.assertEqual('&gt;test', result)

        # '>' после '<' (< кодируется как &lt;, затем > кодируется тк стоит после &lt;)
        result = TextDecoder._encode_large_chunk('<>')
        self.assertEqual('&lt;&gt;', result)

        # '>' после '&' (& кодируется как &amp;, затем > кодируется тк стоит после &amp;)
        result = TextDecoder._encode_large_chunk('&>')
        self.assertEqual('&amp;&gt;', result)

        # '>' после ']'
        result = TextDecoder._encode_gt_large(']>')
        self.assertEqual(']&gt;', result)

    def test_decode_text_block_with_cdata(self):
        """Тестирует полный процесс декодирования с CDATA."""
        text = 'before&lt;test&gt;<![CDATA[raw < & > content]]>after&amp;'
        result = TextDecoder.decode_text_block(text)

        # CDATA должен остаться нетронутым
        self.assertIn('<![CDATA[raw < & > content]]>', result)
        # Остальной текст проходит цикл: unescape -> encode
        # &lt; становится < при unescape, затем снова &lt; при encode
        self.assertIn('&lt;', result)
        # &amp; становится & при unescape, затем снова &amp; при encode
        self.assertIn('&amp;', result)

    def test_decode_empty_and_none(self):
        """Тестирует декодирование пустых и None значений."""
        self.assertEqual('', TextDecoder.decode_text_block(''))
        self.assertEqual(None, TextDecoder.decode_text_block(None))

    def test_large_block_chunking(self):
        """Тестирует разбиение больших блоков на части по 512 символов."""
        # Создаем блок больше 512 символов
        large_text = 'a' * 600
        result = TextDecoder._encode_large_block(large_text)

        # Результат должен быть такой же длины (в данном случае 'a' не кодируется)
        self.assertEqual(600, len(result))
        self.assertEqual('a' * 600, result)


if __name__ == '__main__':
    unittest.main()