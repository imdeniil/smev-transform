"""
Декодирование текстовых блоков согласно алгоритму СМЭВ Шаг 9.1.
"""

import re
from typing import List


class TextDecoder:
    """Класс для декодирования текстовых блоков согласно СМЭВ алгоритму."""

    # Таблица 5 - Правила снятия экранирования
    UNESCAPE_RULES = {
        '&#xd;': '\r',
        '&#13;': '\r',
        '&#10;': '\n',
        '&#xa;': '\n',
        '&#x9;': '\t',
        '&#9;': '\t',
        '\r': '\n',
        '\r\n': '\n',
        '&gt;': '>',
        '&lt;': '<',
        '&amp;': '&',
        '&apos;': "'",
        '&quot;': '"'
    }

    # Таблица 6 - Кодирование блоков размером до 11 символов
    ENCODE_SMALL_RULES = {
        '<': '&lt;',
        '&': '&amp;',
        '\r': '&#xd;'
    }

    # Таблица 7 - Кодирование блоков размером от 12 символов
    ENCODE_LARGE_RULES = {
        '<': '&lt;',
        '&': '&amp;',
        '\r': '&#xd;'
    }

    @classmethod
    def decode_text_block(cls, text: str) -> str:
        """
        Декодирует текстовый блок согласно Шагу 9.1 алгоритма СМЭВ.

        Args:
            text: Исходный текст для декодирования

        Returns:
            str: Декодированный текст
        """
        if not text:
            return text

        # Шаг 2: Разделение блоков с CDATA
        blocks = cls._split_cdata_blocks(text)

        processed_blocks = []
        for block in blocks:
            if block['type'] == 'cdata':
                # CDATA блоки не обрабатываются
                processed_blocks.append(block['content'])
            else:
                # Шаг 1: Снятие экранирования
                unescaped = cls._unescape_text(block['content'])

                # Шаги 3-4: Кодирование по размеру блока
                if len(unescaped) <= 11:
                    encoded = cls._encode_small_block(unescaped)
                else:
                    encoded = cls._encode_large_block(unescaped)

                processed_blocks.append(encoded)

        return ''.join(processed_blocks)

    @classmethod
    def _split_cdata_blocks(cls, text: str) -> List[dict]:
        """
        Шаг 2: Разделяет текстовый блок на части с учетом CDATA секций.

        Returns:
            List[dict]: Список блоков с типом ('text' или 'cdata') и содержимым
        """
        blocks = []
        cdata_pattern = r'<!\[CDATA\[(.*?)\]\]>'

        last_end = 0
        for match in re.finditer(cdata_pattern, text, re.DOTALL):
            # Текст до CDATA
            if match.start() > last_end:
                blocks.append({
                    'type': 'text',
                    'content': text[last_end:match.start()]
                })

            # CDATA блок
            blocks.append({
                'type': 'cdata',
                'content': match.group(0)  # Включаем полную CDATA секцию
            })

            last_end = match.end()

        # Остаток текста после последнего CDATA
        if last_end < len(text):
            blocks.append({
                'type': 'text',
                'content': text[last_end:]
            })

        # Если CDATA не найдено, возвращаем весь текст как один блок
        if not blocks:
            blocks.append({
                'type': 'text',
                'content': text
            })

        return blocks

    @classmethod
    def _unescape_text(cls, text: str) -> str:
        """
        Шаг 1: Снятие экранирования символов согласно Таблице 5.
        """
        result = text

        # Применяем правила в определенном порядке
        # Сначала более специфичные правила, потом общие
        result = result.replace('&#xd;', '\r')
        result = result.replace('&#13;', '\r')
        result = result.replace('&#10;', '\n')
        result = result.replace('&#xa;', '\n')
        result = result.replace('&#x9;', '\t')
        result = result.replace('&#9;', '\t')
        result = result.replace('\r\n', '\n')  # Сначала \r\n
        result = result.replace('\r', '\n')    # Потом \r
        result = result.replace('&gt;', '>')
        result = result.replace('&lt;', '<')
        result = result.replace('&amp;', '&')
        result = result.replace('&apos;', "'")
        result = result.replace('&quot;', '"')

        return result

    @classmethod
    def _encode_small_block(cls, text: str) -> str:
        """
        Шаг 3: Кодирование блоков размером до 11 символов (включительно).
        """
        result = text

        # Кодируем в правильном порядке: & ПЕРВЫМ, чтобы не затронуть уже закодированные символы
        result = result.replace('&', '&amp;')  # & кодируем первым
        result = result.replace('<', '&lt;')
        result = result.replace('\r', '&#xd;')

        # Кодируем > с учетом условий
        result = cls._encode_gt_small(result)

        return result

    @classmethod
    def _encode_gt_small(cls, text: str) -> str:
        """
        Кодирование символа '>' для блоков до 11 символов с учетом условий.
        Условие: если символ идет первым в блоке или стоит сразу после символа ']'
        """
        result = ""
        for i, char in enumerate(text):
            if char == '>':
                # Первый символ в блоке (включая пробелы и переводы строк)
                if i == 0:
                    result += '&gt;'
                # Или стоит сразу после ']'
                elif text[i-1] == ']':
                    result += '&gt;'
                else:
                    result += char
            else:
                result += char

        return result

    @classmethod
    def _encode_large_block(cls, text: str) -> str:
        """
        Шаг 4: Кодирование блоков размером от 12 символов (включительно).
        Блоки разделяются на части по 512 символов.
        """
        if len(text) <= 512:
            return cls._encode_large_chunk(text)

        # Разделяем на части по 512 символов
        chunks = [text[i:i+512] for i in range(0, len(text), 512)]
        encoded_chunks = [cls._encode_large_chunk(chunk) for chunk in chunks]

        return ''.join(encoded_chunks)

    @classmethod
    def _encode_large_chunk(cls, text: str) -> str:
        """Кодирование одного фрагмента для больших блоков."""
        result = text

        # Кодируем в правильном порядке: & ПЕРВЫМ, чтобы не затронуть уже закодированные символы
        result = result.replace('&', '&amp;')  # & кодируем первым
        result = result.replace('<', '&lt;')
        result = result.replace('\r', '&#xd;')

        # Кодируем > с учетом расширенных условий для больших блоков
        result = cls._encode_gt_large(result)

        return result

    @classmethod
    def _encode_gt_large(cls, text: str) -> str:
        """
        Кодирование символа '>' для блоков от 12 символов с учетом условий.
        Условие: если символ идет первым в блоке или стоит сразу после символов '<', '&gt;', '&', ']'
        ВАЖНО: этот метод применяется ПОСЛЕ кодирования &, < и \r
        """
        result = ""
        for i, char in enumerate(text):
            if char == '>':
                if i == 0:
                    # Первый символ в блоке
                    result += '&gt;'
                else:
                    # Проверяем что стоит перед >
                    # Учитываем что & уже закодирован как &amp;
                    if i >= 5 and text[i-5:i] == '&amp;':
                        # Стоит после &amp; (что было &)
                        result += '&gt;'
                    elif i >= 4 and text[i-4:i] == '&lt;':
                        # Стоит после &lt; (что было <)
                        result += '&gt;'
                    elif i >= 4 and text[i-4:i] == '&gt;':
                        # Стоит после &gt;
                        result += '&gt;'
                    elif i >= 1 and text[i-1] == ']':
                        # Стоит после ]
                        result += '&gt;'
                    else:
                        result += char
            else:
                result += char

        return result