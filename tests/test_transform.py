"""
Тесты для класса Transform.
"""

import unittest
from smev_transform import Transform


class TestTransform(unittest.TestCase):
    """Тесты для трансформации XML согласно алгоритму СМЭВ."""

    def test_transform(self):
        """Тестирует основной алгоритм трансформации."""
        src_xml = '''<?xml version="1.0" encoding="UTF-8"?>
            <?xml-stylesheet type="text/xsl" href="style.xsl"?>
            <elementOne xmlns="http://test/1" xmlns:qwe="http://test/2" xmlns:asd="http://test/3">
                <qwe:elementTwo>
                    <asd:elementThree
                        xmlns:wer="http://test/a"
                        xmlns:zxc="http://test/0"
                        wer:attZ="zzz"
                        attB="bbb"
                        attA="aaa"
                        zxc:attC="ccc"
                        asd:attD="ddd"
                        asd:attE="eee"
                        qwe:attF="fff"
                    />
                </qwe:elementTwo>
                <qwe:elementFour>0</qwe:elementFour>
                <qwe:elementFive/>
                <qwe:elementSix>   </qwe:elementSix>
            </elementOne>'''

        expected_xml = ('<ns1:elementOne xmlns:ns1="http://test/1">'
                       '<ns2:elementTwo xmlns:ns2="http://test/2">'
                       '<ns3:elementThree xmlns:ns3="http://test/3" xmlns:ns4="http://test/0" xmlns:ns5="http://test/a" ns4:attC="ccc" ns2:attF="fff" ns3:attD="ddd" ns3:attE="eee" ns5:attZ="zzz" attA="aaa" attB="bbb"></ns3:elementThree>'
                       '</ns2:elementTwo>'
                       '<ns2:elementFour>0</ns2:elementFour>'
                       '<ns2:elementFive></ns2:elementFive>'
                       '<ns2:elementSix></ns2:elementSix>'
                       '</ns1:elementOne>')

        transform = Transform()
        result = transform.process(src_xml)

        # Мы не используем assertXmlStringEqualsXmlString потому что она не видит различий
        # между пустыми парными и самозакрывающимися тегами согласно спецификациям.
        # Но для нас это критично важно из-за правила СМЭВ №3
        self.assertEqual(expected_xml, result)

    def test_simple_element(self):
        """Тестирует трансформацию простого элемента."""
        src_xml = '<root>test</root>'
        expected_xml = '<root>test</root>'

        transform = Transform()
        result = transform.process(src_xml)

        self.assertEqual(expected_xml, result)

    def test_element_with_namespace(self):
        """Тестирует трансформацию элемента с namespace."""
        src_xml = '<root xmlns="http://example.com">test</root>'
        expected_xml = '<ns1:root xmlns:ns1="http://example.com">test</ns1:root>'

        transform = Transform()
        result = transform.process(src_xml)

        self.assertEqual(expected_xml, result)

    def test_empty_element(self):
        """Тестирует трансформацию пустого элемента (должен стать парным тегом)."""
        src_xml = '<empty/>'
        expected_xml = '<empty></empty>'

        transform = Transform()
        result = transform.process(src_xml)

        self.assertEqual(expected_xml, result)

    def test_text_decoding(self):
        """Тестирует декодирование текстовых блоков (Шаг 9.1)."""
        src_xml = '<root>&gt;&gt;text&lt;&amp;</root>'
        expected_xml = '<root>&gt;>text&lt;&amp;</root>'  # Only first > is encoded (at beginning), second > is not

        transform = Transform()
        result = transform.process(src_xml)

        self.assertEqual(expected_xml, result)

    def test_attribute_decoding(self):
        """Тестирует декодирование атрибутов (Шаг 9.2)."""
        src_xml = '<root attr="value\twith\r\nwhitespace"/>'
        expected_xml = '<root attr="value with whitespace"></root>'

        transform = Transform()
        result = transform.process(src_xml)

        self.assertEqual(expected_xml, result)

    def test_cdata_handling(self):
        """Тестирует обработку CDATA блоков."""
        src_xml = '<root>text<![CDATA[raw < & > content]]>more text</root>'

        transform = Transform()
        result = transform.process(src_xml)

        # CDATA content is merged into text by ElementTree parser
        # The content is processed according to Step 9.1 text decoding
        self.assertIn('textraw &lt; &amp; > contentmore text', result)

    def test_complex_smev_example(self):
        """Тестирует сложный пример из документации СМЭВ."""
        src_xml = '''<root xmlns="http://test" attr="&gt;test&lt;">
            <child>&amp;text&gt;</child>
        </root>'''

        transform = Transform()
        result = transform.process(src_xml)

        # Проверяем что результат содержит правильные namespace префиксы
        self.assertIn('ns1:', result)
        self.assertIn('xmlns:ns1="http://test"', result)


if __name__ == '__main__':
    unittest.main()