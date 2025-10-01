# Технические спецификации проекта

## Технологический стек

### Основные технологии

- **Язык программирования:** Python 3.7+
- **XML обработка:** xml.etree.ElementTree (стандартная библиотека)
- **Тестирование:** pytest 7.0+
- **Пакетный менеджер:** uv (рекомендуется) или pip
- **Build система:** setuptools + pyproject.toml (PEP 517/518)

### Зависимости

#### Runtime зависимости
- **Нет внешних зависимостей** - используется только стандартная библиотека Python

#### Dev зависимости
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
```

### Требования к окружению

- **Python:** >= 3.7
- **OS:** Windows, Linux, macOS (кросс-платформенность)
- **Память:** Минимальные требования (обработка в памяти)

## Архитектурные принципы

### 1. Модульность

Каждый модуль отвечает за отдельный аспект трансформации:

```
transform.py          → Координация всех шагов
text_decoder.py       → Шаг 9.1
attribute_decoder.py  → Шаг 9.2
xml_namespace.py      → Работа с namespaces
attribute.py          → Представление атрибутов
comparators.py        → Сортировка
exceptions.py         → Обработка ошибок
```

### 2. Единственная ответственность (SRP)

Каждый класс выполняет одну четко определенную задачу:

- `Transform` - координирует трансформацию
- `TextDecoder` - только декодирование текста
- `AttributeDecoder` - только декодирование атрибутов

### 3. Открыт для расширения, закрыт для модификации (OCP)

- Декодеры реализованы как независимые модули
- Легко добавить новые шаги без изменения существующего кода

### 4. Инверсия зависимостей (DIP)

- `Transform` зависит от абстракций (методы декодеров)
- Декодеры не зависят от `Transform`

### 5. Immutability где возможно

- Декодеры используют статические методы
- `XmlNamespace` и `Attribute` - immutable data classes

## Правила стилизации кода

### PEP 8 Compliance

Проект следует стандарту PEP 8:

```python
# Именование классов: PascalCase
class Transform:
    pass

# Именование методов и переменных: snake_case
def process_xml(xml_string: str) -> str:
    result_xml = transform(xml_string)
    return result_xml

# Константы: UPPER_CASE
ALGORITHM_URN = "urn://smev-gov-ru/xmldsig/transform"
XML_ENCODING = "UTF-8"

# Приватные методы: _leading_underscore
def _remove_xml_declarations(self, xml: str) -> str:
    pass
```

### Type Hints

Используются аннотации типов для всех публичных методов:

```python
from typing import List, Optional, Deque

def process(self, xml: str) -> str:
    """Процесс с явными типами"""
    pass

def _collect_namespaces(self, element: ET.Element) -> List[XmlNamespace]:
    """Возвращаем типизированный список"""
    pass

def __init__(self):
    self.prefix_stack: Optional[Deque[Deque[XmlNamespace]]] = None
    self.prefix_counter: int = 1
```

### Docstrings

Все публичные методы и классы документированы:

```python
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
```

Формат: Google Style Docstrings

### Форматирование

```python
# Длина строки: рекомендуется <= 88 символов (Black style)
# Максимум: 120 символов

# Импорты: группировка
import re  # Стандартная библиотека
from collections import deque
from typing import List, Optional  # Typing

from xml.etree import ElementTree as ET  # XML обработка

from .attribute import Attribute  # Локальные импорты
from .xml_namespace import XmlNamespace
```

### Обработка ошибок

```python
try:
    root = ET.fromstring(xml_clean)
except ET.ParseError as e:
    raise TransformationException(f"Failed to parse XML: {e}")
```

- Используем специфичные исключения
- Всегда добавляем контекст к ошибкам
- Не глушим исключения без необходимости

## Паттерны кодирования

### 1. Static Methods для утилитарных функций

```python
class TextDecoder:
    @staticmethod
    def decode_text_block(text: str, is_cdata: bool = False) -> str:
        """Не требует состояния - static method"""
        pass
```

### 2. List Comprehensions для трансформаций

```python
# Вместо цикла
attributes = [
    Attribute(name, value)
    for name, value in element.attrib.items()
]

# Фильтрация
used_namespaces = [
    ns for ns in all_namespaces
    if ns.is_used(element)
]
```

### 3. Context Managers для управления ресурсами

```python
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
```

### 4. Generator Expressions для больших коллекций

```python
# Ленивая обработка
elements_text = "".join(
    process_element(el)
    for el in elements
)
```

### 5. Defaultdict и deque для специализированных структур

```python
from collections import deque

self.prefix_stack: Deque[Deque[XmlNamespace]] = deque()
```

## Тестирование

### Структура тестов

```python
import unittest

class TestTransform(unittest.TestCase):
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.transform = Transform()

    def test_basic_transformation(self):
        """Базовая трансформация"""
        xml = '<root>test</root>'
        result = self.transform.process(xml)
        self.assertEqual(result, '<root>test</root>')

    def tearDown(self):
        """Очистка после теста"""
        pass
```

### Покрытие тестами

Целевое покрытие: **>90%**

Текущее покрытие:
- `transform.py` - ~95%
- `text_decoder.py` - ~95%
- `attribute_decoder.py` - ~95%
- Общее - ~93%

### Типы тестов

1. **Unit тесты** - тестирование отдельных методов
2. **Integration тесты** - тестирование взаимодействия классов
3. **Regression тесты** - примеры из документации СМЭВ
4. **Edge case тесты** - граничные случаи

### Запуск тестов

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Конкретный файл
pytest tests/test_transform.py

# С coverage
pytest --cov=smev_transform --cov-report=html
```

## Производительность

### Оптимизации

1. **Использование deque для стека** - O(1) операции
2. **Минимальное копирование строк** - использование join()
3. **Кеширование регулярных выражений** - компиляция один раз
4. **Отсутствие рекурсии там, где возможна итерация**

### Сложность алгоритма

- **Временная сложность:** O(n), где n - количество элементов в XML
- **Пространственная сложность:** O(h), где h - глубина XML дерева

### Ограничения

- Работает с XML в памяти - не подходит для очень больших файлов (>100MB)
- Для больших файлов рекомендуется стриминговая обработка (будущее улучшение)

## Безопасность

### XML парсинг

```python
# НЕТ обработки внешних сущностей (защита от XXE)
ET.fromstring(xml)  # По умолчанию безопасно в Python 3.7+
```

### Валидация входных данных

```python
try:
    root = ET.fromstring(xml_clean)
except ET.ParseError as e:
    raise TransformationException(f"Invalid XML: {e}")
```

### Обработка кодировок

```python
# Всегда UTF-8
XML_ENCODING = "UTF-8"
```

## CI/CD (Будущее)

### GitHub Actions (планируется)

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, 3.10, 3.11, 3.12]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest --cov=smev_transform
```

## Версионирование

Следуем **Semantic Versioning 2.0.0**:

```
MAJOR.MINOR.PATCH

MAJOR - несовместимые изменения API
MINOR - новая функциональность с обратной совместимостью
PATCH - исправления багов
```

Текущая версия: **2.0.0**

## Публикация

### Сборка пакета

```bash
# Установка инструментов
uv pip install build twine

# Сборка
python -m build

# Проверка
python -m twine check dist/*
```

### Публикация на PyPI

```bash
# Test PyPI (опционально)
python -m twine upload --repository testpypi dist/*

# Production PyPI
python -m twine upload dist/*
```

## Документация кода

### Inline комментарии

```python
# Комментарии для сложной логики
def _should_encode_gt(text: str) -> bool:
    # Кодируем '>' только если:
    # 1. Длина текста >= 12 символов, ИЛИ
    # 2. Текст содержит ']]' (защита от ']]>')
    return len(text) >= 12 or ']]' in text
```

### TODO/FIXME/NOTE

```python
# TODO: Добавить поддержку стриминга для больших файлов
# FIXME: Обработать edge case с пустыми CDATA
# NOTE: Этот код соответствует СМЭВ 3.5.0.27 спецификации
```

## Совместимость

### Python версии

Тестируется на:
- Python 3.7 (минимальная)
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12 (последняя)

### Операционные системы

- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, CentOS)
- ✅ macOS (10.15+)

### Кодировки

- Поддерживается только UTF-8 (стандарт СМЭВ)

## Лицензирование

- **Лицензия:** MIT License
- **Коммерческое использование:** Разрешено
- **Модификация:** Разрешена
- **Распространение:** Разрешено
- **Гарантии:** Отсутствуют (AS IS)

## Контроль качества

### Pre-commit hooks (рекомендуется)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
```

### Code review checklist

- [ ] Все тесты проходят
- [ ] Код следует PEP 8
- [ ] Добавлены docstrings
- [ ] Добавлены type hints
- [ ] Обновлена документация
- [ ] Обновлен CHANGELOG.md

## Метрики качества

### Целевые метрики

- **Test coverage:** >90%
- **Cyclomatic complexity:** <10 на функцию
- **Maintainability index:** >70
- **Code duplication:** <5%

### Инструменты анализа

```bash
# Coverage
pytest --cov=smev_transform --cov-report=html

# Complexity
radon cc smev_transform/ -a

# Maintainability
radon mi smev_transform/

# Type checking
mypy smev_transform/
```
