"""
Основной класс для трансформации XML согласно алгоритму СМЭВ.
"""

import re
from collections import deque
from typing import List, Optional, Deque
from xml.etree import ElementTree as ET

from .attribute import Attribute
from .xml_namespace import XmlNamespace
from .comparators import AttributeSortingComparator
from .exceptions import TransformationException


class Transform:
    """Класс для выполнения трансформации XML согласно алгоритму СМЭВ."""

    ALGORITHM_URN = "urn://smev-gov-ru/xmldsig/transform"
    XML_ENCODING = "UTF-8"

    def __init__(self):
        self.prefix_stack: Optional[Deque[Deque[XmlNamespace]]] = None
        self.prefix_counter = 1

    def process(self, xml: str) -> str:
        """
        Выполняет трансформацию XML согласно алгоритму СМЭВ.

        Args:
            xml: Исходный XML для трансформации

        Returns:
            str: Трансформированный XML

        Raises:
            TransformationException: При ошибках трансформации
        """
        try:
            self.prefix_stack = deque()
            self.prefix_counter = 1

            # Удаляем XML declaration и processing instructions
            xml_clean = self._remove_xml_declarations(xml)

            # Парсим XML
            root = ET.fromstring(xml_clean)

            # Выполняем трансформацию
            result_xml = self._transform_element(root)

            return result_xml

        except Exception as e:
            raise TransformationException(
                f"Can not perform transformation {self.ALGORITHM_URN}"
            ) from e

    def _remove_xml_declarations(self, xml: str) -> str:
        """Удаляет XML declaration и processing instructions."""
        # Удаляем XML declaration
        xml = re.sub(r'<\?xml[^>]*\?>', '', xml)
        # Удаляем processing instructions
        xml = re.sub(r'<\?[^>]*\?>', '', xml)
        return xml.strip()

    def _transform_element(self, element: ET.Element) -> str:
        """Трансформирует XML элемент согласно алгоритму СМЭВ."""
        result = []
        current_prefix_stack = deque()
        self.prefix_stack.append(current_prefix_stack)

        try:
            # Получаем namespace URI и local name элемента (строка 119-129 Java)
            ns_uri, local_name = self._parse_element_name(element.tag)
            prefix = self._find_prefix(ns_uri) if ns_uri else None

            if ns_uri and not prefix:
                prefix = f"ns{self.prefix_counter}"
                self.prefix_counter += 1
                current_prefix_stack.append(XmlNamespace(ns_uri, prefix))

            # Формируем имя элемента с префиксом
            if prefix and ns_uri:
                element_name = f"{prefix}:{local_name}"
            else:
                element_name = local_name

            # Обрабатываем атрибуты
            src_attributes = self._collect_attributes(element)
            sorted_attributes = sorted(src_attributes, key=AttributeSortingComparator.get_sort_key())

            # Генерируем префиксы для атрибутов (строка 142-161 Java)
            dst_attributes = []
            for attr in sorted_attributes:
                if attr.get_uri():
                    attr_prefix = self._find_prefix(attr.get_uri())
                    if not attr_prefix:
                        attr_prefix = f"ns{self.prefix_counter}"
                        self.prefix_counter += 1
                        current_prefix_stack.append(XmlNamespace(attr.get_uri(), attr_prefix))

                    dst_attributes.append(Attribute(
                        attr.get_name(),
                        attr.get_value(),
                        attr.get_uri(),
                        attr_prefix
                    ))
                else:
                    dst_attributes.append(attr)

            # Формируем открывающий тег
            result.append(f"<{element_name}")

            # Добавляем объявления namespace
            for namespace in current_prefix_stack:
                result.append(f' xmlns:{namespace.get_prefix()}="{namespace.get_uri()}"')

            # Добавляем атрибуты
            for attr in dst_attributes:
                if attr.get_uri():
                    attr_name = f"{attr.get_prefix()}:{attr.get_name()}"
                else:
                    attr_name = attr.get_name()
                result.append(f' {attr_name}="{attr.get_value()}"')

            result.append(">")

            # Обрабатываем содержимое элемента
            # Согласно C# XmlDsigSmevTransform (строка 254): удаляем \n и отсекаем whitespace
            if element.text and element.text.strip():
                # Удаляем переносы строк как в C# версии: .Replace("\n", "")
                text_without_newlines = element.text.replace('\n', '')
                if text_without_newlines.strip():
                    result.append(text_without_newlines)

            # Обрабатываем дочерние элементы
            for child in element:
                child_result = self._transform_element(child)
                result.append(child_result)

                # Добавляем tail текст если он не пустой (отсекаем whitespace и удаляем \n)
                if child.tail and child.tail.strip():
                    tail_without_newlines = child.tail.replace('\n', '')
                    if tail_without_newlines.strip():
                        result.append(tail_without_newlines)

            # Гарантируем, что empty tags запишутся в форме <a></a>, а не <a/>
            # Согласно строке 180 Java: dst.add(eventFactory.get().createSpace(""));
            # Добавляем пустую строку перед закрывающим тегом
            if not element.text and len(element) == 0:
                result.append("")

            # Формируем закрывающий тег (всегда полный, не self-closing)
            result.append(f"</{element_name}>")

            return ''.join(result)

        finally:
            self.prefix_stack.pop()

    def _parse_element_name(self, tag: str) -> tuple:
        """Разбирает тег элемента на namespace URI и local name."""
        if '}' in tag:
            uri, local_name = tag.split('}', 1)
            return uri[1:], local_name  # убираем открывающую фигурную скобку
        return "", tag

    def _collect_attributes(self, element: ET.Element) -> List[Attribute]:
        """
        Собирает атрибуты элемента.
        Java-реализация не делает декодирование - парсер XML уже обрабатывает entities.
        """
        attributes = []
        for name, value in element.attrib.items():
            # Значение атрибута используется как есть - парсер XML уже декодировал entities
            if '}' in name:
                # Qualified атрибут
                uri, local_name = name.split('}', 1)
                uri = uri[1:]  # убираем открывающую фигурную скобку
                attributes.append(Attribute(local_name, value, uri))
            else:
                # Unqualified атрибут
                attributes.append(Attribute(name, value))
        return attributes

    def _find_prefix(self, uri: str) -> Optional[str]:
        """
        Ищет существующий префикс для заданного URI namespace.
        Аналог метода findPrefix в Java (строка 232-244).
        """
        if not uri:
            return None

        # Ищем в стеке (как в Java)
        for current_prefix_stack in self.prefix_stack:
            for namespace in current_prefix_stack:
                if uri == namespace.get_uri():
                    return namespace.get_prefix()
        return None