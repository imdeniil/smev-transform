"""
Декодирование атрибутов согласно алгоритму СМЭВ Шаг 9.2.
"""

import re


class AttributeDecoder:
    """Класс для декодирования атрибутов согласно СМЭВ алгоритму."""

    # Таблица 8 - Правила снятия экранирования в атрибутах
    UNESCAPE_RULES = {
        '&#xd;': '\r',
        '&#13;': '\r',
        '&#10;': '\n',
        '&#xa;': '\n',
        '&#x9;': '\t',
        '&#9;': '\t',
        '\r': ' ',  # заменяем на пробел
        '\r\n': ' ',  # заменяем на пробел
        '\n': ' ',  # заменяем на пробел
        '\t': ' ',  # заменяем на пробел
        '&gt;': '>',
        '&lt;': '<',
        '&amp;': '&',
        '&apos;': "'",
        '&quot;': '"'
    }

    # Таблица 9 - Правила кодирования атрибутов
    ENCODE_RULES = {
        '<': '&lt;',
        '&': '&amp;',
        '"': '&quot;',
        '\r': '&#xd;',
        '\n': '&#xa;',
        '\t': '&#x9;'
    }

    @classmethod
    def decode_attribute_value(cls, value: str) -> str:
        """
        Декодирует значение атрибута согласно Шагу 9.2 алгоритма СМЭВ.

        Args:
            value: Исходное значение атрибута

        Returns:
            str: Декодированное значение атрибута
        """
        if not value:
            return value

        # Шаг 1: Снятие экранирования и замена пробельных символов
        unescaped = cls._unescape_and_normalize_whitespace(value)

        # Шаг 2: Кодирование атрибутов
        encoded = cls._encode_attribute(unescaped)

        return encoded

    @classmethod
    def _unescape_and_normalize_whitespace(cls, value: str) -> str:
        """
        Шаг 1: Снятие экранирования и замена пробельных символов.

        В атрибутах XML сообщения выполняется замена пробельных символов
        (перевод строки, пробел, символ перевода каретки, табуляция) на пробел.
        """
        result = value

        # Сначала заменяем пробельные символы на пробелы
        result = result.replace('\r\n', ' ')
        result = result.replace('\r', ' ')
        result = result.replace('\n', ' ')
        result = result.replace('\t', ' ')

        # Затем применяем правила снятия экранирования
        for escaped, unescaped in cls.UNESCAPE_RULES.items():
            result = result.replace(escaped, unescaped)

        return result

    @classmethod
    def _encode_attribute(cls, value: str) -> str:
        """
        Шаг 2: Кодирование атрибутов согласно Таблице 9.

        Кодирование выполняется в соответствии с правилами, где все символы
        кодируются "всегда" без дополнительных условий.
        """
        result = value

        # Кодируем & в первую очередь, чтобы не затронуть уже закодированные символы
        result = result.replace('&', '&amp;')
        result = result.replace('<', '&lt;')
        result = result.replace('"', '&quot;')
        result = result.replace('\r', '&#xd;')
        result = result.replace('\n', '&#xa;')
        result = result.replace('\t', '&#x9;')

        return result