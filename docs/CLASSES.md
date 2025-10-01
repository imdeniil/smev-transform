# Структура классов проекта

## Обзор архитектуры

Проект построен на модульной архитектуре с четким разделением ответственности между классами.

```
┌─────────────────────────────────────────────────────────────┐
│                         Transform                            │
│  (Главный класс - координатор всех шагов трансформации)     │
└──────────────┬──────────────────────────────────────────────┘
               │
               ├──► TextDecoder (Шаг 9.1)
               ├──► AttributeDecoder (Шаг 9.2)
               ├──► XmlNamespace (Работа с namespaces)
               ├──► Attribute (Представление атрибутов)
               ├──► AttributeSortingComparator (Сортировка)
               └──► TransformationException (Исключения)
```

## Основные классы

### 1. Transform (transform.py)

**Назначение:** Главный класс, реализующий полный алгоритм трансформации СМЭВ.

**Атрибуты:**
- `ALGORITHM_URN: str` - URN алгоритма трансформации
- `XML_ENCODING: str` - Кодировка XML (UTF-8)
- `prefix_stack: Optional[Deque[Deque[XmlNamespace]]]` - Стек префиксов namespaces
- `prefix_counter: int` - Счетчик для генерации автоматических префиксов

**Методы:**
```python
def process(self, xml: str) -> str:
    """
    Главный метод - выполняет полную трансформацию XML.

    Args:
        xml: Исходный XML строка

    Returns:
        str: Трансформированный XML

    Raises:
        TransformationException: При ошибках парсинга или трансформации
    """

def _remove_xml_declarations(self, xml: str) -> str:
    """Шаг 1: Удаление XML declaration и processing instructions"""

def _transform_element(self, element: ET.Element) -> str:
    """Шаги 2-9: Трансформация элемента"""

def _collect_namespaces(self, element: ET.Element) -> List[XmlNamespace]:
    """Шаг 4: Сбор используемых namespaces"""

def _generate_prefix(self) -> str:
    """Шаг 6: Генерация автоматических префиксов (ns1, ns2, ...)"""

def _sort_attributes(self, attributes: List[Attribute]) -> List[Attribute]:
    """Шаг 7: Сортировка атрибутов"""
```

**Алгоритм работы:**
1. Удаление XML declarations (Шаг 1)
2. Парсинг XML
3. Рекурсивная трансформация элементов (Шаги 2-9)

---

### 2. TextDecoder (text_decoder.py)

**Назначение:** Реализация Шага 9.1 - декодирование и корректное кодирование текстовых блоков.

**Методы:**
```python
@staticmethod
def decode_text_block(text: str, is_cdata: bool = False) -> str:
    """
    Декодирует и корректно кодирует текстовый блок.

    Args:
        text: Исходный текст
        is_cdata: Флаг CDATA секции

    Returns:
        str: Корректно закодированный текст
    """

@staticmethod
def _decode_entities(text: str) -> str:
    """Декодирует HTML/XML entity references"""

@staticmethod
def _encode_text(text: str) -> str:
    """
    Кодирует текст согласно правилам СМЭВ:
    - < → &lt;
    - & → &amp;
    - > → &gt; (только если длина >= 12 или есть "]]")
    """

@staticmethod
def _should_encode_gt(text: str) -> bool:
    """Определяет, нужно ли кодировать символ '>'"""
```

**Особенности:**
- Декодирование всех стандартных entity references (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;`, `&#xXX;`)
- Условное кодирование символа `>` (только для длинных блоков >= 12 символов или содержащих `]]`)
- Корректная обработка CDATA секций

---

### 3. AttributeDecoder (attribute_decoder.py)

**Назначение:** Реализация Шага 9.2 - декодирование и нормализация атрибутов.

**Методы:**
```python
@staticmethod
def decode_attribute_value(value: str) -> str:
    """
    Декодирует и нормализует значение атрибута.

    Args:
        value: Исходное значение атрибута

    Returns:
        str: Нормализованное и закодированное значение
    """

@staticmethod
def _normalize_whitespace(value: str) -> str:
    """
    Нормализует пробельные символы:
    - \t, \n, \r → пробел
    - Множественные пробелы → один пробел
    """

@staticmethod
def _decode_entities(value: str) -> str:
    """Декодирует entity references в атрибутах"""

@staticmethod
def _encode_attribute(value: str) -> str:
    """
    Кодирует атрибут:
    - & → &amp;
    - < → &lt;
    - " → &quot;
    """
```

**Особенности:**
- Нормализация всех whitespace символов в один пробел
- Декодирование entity references
- Обязательное кодирование кавычек (`"`)

---

### 4. XmlNamespace (xml_namespace.py)

**Назначение:** Представление XML namespace.

**Атрибуты:**
```python
prefix: Optional[str]  # Префикс namespace (может быть None для default namespace)
uri: str               # URI namespace
```

**Методы:**
```python
def __init__(self, prefix: Optional[str], uri: str):
    """Создание namespace"""

def __eq__(self, other) -> bool:
    """Сравнение namespaces (по URI и prefix)"""

def __hash__(self) -> int:
    """Хеш для использования в множествах"""
```

**Использование:**
```python
ns = XmlNamespace("ns1", "http://example.com/ns")
```

---

### 5. Attribute (attribute.py)

**Назначение:** Представление XML атрибута с поддержкой namespaces.

**Атрибуты:**
```python
local_name: str                    # Локальное имя атрибута
value: str                         # Значение атрибута
namespace: Optional[XmlNamespace]  # Namespace атрибута (если есть)
```

**Методы:**
```python
def __init__(self, local_name: str, value: str, namespace: Optional[XmlNamespace] = None):
    """Создание атрибута"""

def get_full_name(self) -> str:
    """
    Получение полного имени атрибута.

    Returns:
        "prefix:local_name" или "local_name"
    """
```

**Использование:**
```python
attr = Attribute("id", "123")  # Простой атрибут
attr_ns = Attribute("type", "data", XmlNamespace("ns1", "http://..."))  # С namespace
```

---

### 6. AttributeSortingComparator (comparators.py)

**Назначение:** Компаратор для сортировки атрибутов (Шаг 7).

**Методы:**
```python
@staticmethod
def compare(attr1: Attribute, attr2: Attribute) -> int:
    """
    Сравнивает два атрибута для сортировки.

    Правила сортировки:
    1. Атрибуты с namespace идут перед атрибутами без namespace
    2. Среди namespace атрибутов - сортировка по полному имени
    3. Среди обычных атрибутов - сортировка по локальному имени

    Returns:
        -1, 0, или 1
    """
```

**Использование:**
```python
from functools import cmp_to_key

sorted_attrs = sorted(attributes, key=cmp_to_key(AttributeSortingComparator.compare))
```

---

### 7. TransformationException (exceptions.py)

**Назначение:** Пользовательское исключение для ошибок трансформации.

**Наследование:** `Exception`

**Использование:**
```python
try:
    result = transform.process(xml)
except TransformationException as e:
    print(f"Ошибка трансформации: {e}")
```

## Взаимодействие классов

### Процесс трансформации

```
1. Transform.process(xml)
   │
   ├─► Transform._remove_xml_declarations(xml)  [Шаг 1]
   │
   ├─► ET.fromstring(xml_clean)  [Парсинг]
   │
   └─► Transform._transform_element(root)  [Шаги 2-9]
       │
       ├─► Сбор namespaces → XmlNamespace
       │
       ├─► Генерация префиксов → Transform._generate_prefix()
       │
       ├─► Сбор атрибутов → Attribute
       │
       ├─► Сортировка → AttributeSortingComparator.compare()
       │
       ├─► Декодирование текста → TextDecoder.decode_text_block()
       │
       └─► Декодирование атрибутов → AttributeDecoder.decode_attribute_value()
```

### Пример потока данных

```python
# Входные данные
xml = '<root xmlns="http://test" attr="value">Text</root>'

# 1. Transform обрабатывает XML
transform = Transform()

# 2. Создаются XmlNamespace объекты
ns = XmlNamespace("ns1", "http://test")

# 3. Создаются Attribute объекты
attr = Attribute("attr", "value")

# 4. AttributeDecoder обрабатывает значение атрибута
decoded_value = AttributeDecoder.decode_attribute_value(attr.value)

# 5. TextDecoder обрабатывает текст элемента
decoded_text = TextDecoder.decode_text_block("Text")

# 6. Transform собирает всё вместе
result = '<ns1:root xmlns:ns1="http://test" attr="value">Text</ns1:root>'
```

## Диаграмма зависимостей

```
Transform
├── depends on → XmlNamespace
├── depends on → Attribute
├── depends on → AttributeSortingComparator
├── depends on → TextDecoder
├── depends on → AttributeDecoder
└── raises → TransformationException

Attribute
└── depends on → XmlNamespace

AttributeSortingComparator
└── depends on → Attribute

TextDecoder
└── standalone (static methods)

AttributeDecoder
└── standalone (static methods)

XmlNamespace
└── standalone (data class)

TransformationException
└── extends → Exception
```

## Паттерны проектирования

1. **Strategy Pattern** - TextDecoder и AttributeDecoder реализуют стратегии обработки
2. **Composite Pattern** - Рекурсивная обработка XML элементов
3. **Factory Pattern** - Генерация автоматических префиксов
4. **Data Transfer Object** - XmlNamespace, Attribute

## Расширяемость

Проект легко расширяется:

1. **Добавление новых шагов трансформации:**
   - Создать новый класс-декодер (по аналогии с TextDecoder)
   - Вызвать его в Transform._transform_element()

2. **Добавление новых типов атрибутов:**
   - Расширить класс Attribute
   - Обновить AttributeSortingComparator

3. **Добавление валидации:**
   - Создать класс Validator
   - Вызвать в Transform.process()

## Тестируемость

Все классы хорошо тестируются:

- **Unit тесты:** Каждый класс имеет свои тесты
- **Integration тесты:** test_transform.py проверяет взаимодействие
- **Мокирование:** Не требуется благодаря четким границам между классами
