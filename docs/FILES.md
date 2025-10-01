# Файловая структура проекта

## Корневая директория

```
smev_transform/
│
├── smev_transform/              # Основной пакет
│   ├── __init__.py              # Инициализация пакета, экспорт публичного API
│   ├── transform.py             # Главный класс Transform
│   ├── text_decoder.py          # Декодирование текстовых блоков (Шаг 9.1)
│   ├── attribute_decoder.py     # Декодирование атрибутов (Шаг 9.2)
│   ├── xml_namespace.py         # Работа с XML namespaces
│   ├── attribute.py             # Класс представления XML атрибутов
│   ├── comparators.py           # Компараторы для сортировки атрибутов
│   ├── exceptions.py            # Пользовательские исключения
│   │
│   └── tests/                   # Тесты
│       ├── __init__.py
│       ├── test_transform.py             # Тесты основной трансформации
│       ├── test_text_decoder.py          # Тесты декодирования текста (Шаг 9.1)
│       ├── test_attribute_decoder.py     # Тесты декодирования атрибутов (Шаг 9.2)
│       ├── test_comparators.py           # Тесты компараторов
│       └── test_documentation_examples.py # Тесты примеров из документации
│
├── docs/                        # Документация
│   ├── CHANGELOG.md             # История изменений (semver)
│   ├── TRANSIT.md               # Промежуточный контекст для разработки
│   ├── FILES.md                 # Этот файл - структура проекта
│   ├── CLASSES.md               # Описание классов проекта
│   └── TECH.md                  # Архитектура и технологии
│
├── .gitignore                   # Git ignore правила
├── LICENSE                      # MIT License
├── MANIFEST.in                  # Инструкции для включения файлов в дистрибутив
├── README.md                    # Основная документация
├── CLAUDE.md                    # Инструкции для Claude Code
├── pyproject.toml               # Современная конфигурация пакета (PEP 517/518)
├── setup.py                     # Setuptools конфигурация (для обратной совместимости)
└── requirements.txt             # Зависимости для разработки
```

## Описание основных файлов

### Конфигурационные файлы

- **pyproject.toml** - Основной конфигурационный файл для современного Python packaging (PEP 517/518)
  - Метаданные пакета
  - Зависимости
  - Build system конфигурация
  - Настройки инструментов (pytest)

- **setup.py** - Setuptools конфигурация для обратной совместимости
  - Используется для `pip install -e .`
  - Дублирует информацию из pyproject.toml

- **MANIFEST.in** - Определяет дополнительные файлы для включения в source distribution
  - README.md, LICENSE
  - Документация из docs/
  - Тесты

- **.gitignore** - Исключает из git:
  - `__pycache__/`, `*.pyc`
  - `dist/`, `build/`, `*.egg-info/`
  - `.venv/`, виртуальные окружения
  - IDE файлы

### Исходный код

#### Основной модуль (smev_transform/)

- **__init__.py** (16 строк)
  - Экспортирует: Transform, TransformationException, TextDecoder, AttributeDecoder
  - Определяет версию: `__version__ = "2.0.0"`

- **transform.py** (~300 строк)
  - Класс Transform - главный класс трансформации
  - Реализует все 9 шагов алгоритма
  - Методы: process(), _transform_element(), _collect_namespaces() и др.

- **text_decoder.py** (~150 строк)
  - Класс TextDecoder
  - Реализует Шаг 9.1 - декодирование текстовых блоков
  - Обработка entity references
  - Корректное кодирование символа `>`

- **attribute_decoder.py** (~100 строк)
  - Класс AttributeDecoder
  - Реализует Шаг 9.2 - декодирование атрибутов
  - Нормализация whitespace

- **xml_namespace.py** (~50 строк)
  - Класс XmlNamespace
  - Представление XML namespace (prefix, uri)

- **attribute.py** (~60 строк)
  - Класс Attribute
  - Представление XML атрибута с namespace support

- **comparators.py** (~30 строк)
  - AttributeSortingComparator
  - Сортировка атрибутов в алфавитном порядке (Шаг 7)

- **exceptions.py** (~10 строк)
  - TransformationException
  - Пользовательское исключение для ошибок трансформации

#### Тесты (smev_transform/tests/)

- **test_transform.py** (~200 строк)
  - Тесты основной функциональности Transform
  - Проверка всех шагов 1-8

- **test_text_decoder.py** (~150 строк)
  - Тесты TextDecoder (Шаг 9.1)
  - Тестирование entity references
  - Тестирование CDATA
  - Edge cases

- **test_attribute_decoder.py** (~100 строк)
  - Тесты AttributeDecoder (Шаг 9.2)
  - Нормализация пробелов
  - Entity references в атрибутах

- **test_comparators.py** (~50 строк)
  - Тесты сортировки атрибутов

- **test_documentation_examples.py** (~100 строк)
  - Примеры из README.md
  - Проверка корректности документации

### Документация (docs/)

- **CHANGELOG.md** - История изменений в формате Keep a Changelog
- **TRANSIT.md** - Текущее состояние проекта, контекст для новых чатов
- **FILES.md** - Этот файл, структура проекта
- **CLASSES.md** - Описание классов и их взаимодействия
- **TECH.md** - Архитектура, технологический стек, стиль кода

### Корневые файлы

- **README.md** - Основная документация проекта
  - Установка
  - Использование
  - Примеры
  - API reference

- **LICENSE** - MIT License

- **CLAUDE.md** - Инструкции для Claude Code
  - Окружение (Windows, Python, uv)
  - Принципы документирования
  - Файлы документации

- **requirements.txt** - Зависимости для разработки
  - pytest>=7.0.0 (тестирование)

## Размер проекта

- **Всего Python файлов:** ~15
- **Строк кода:** ~1200
- **Строк тестов:** ~600
- **Документация:** ~500 строк

## Зависимости

### Runtime зависимости
- Нет внешних зависимостей
- Используется только стандартная библиотека Python (xml.etree.ElementTree)

### Dev зависимости
- pytest>=7.0.0 - для тестирования
- pytest-cov>=4.0.0 - для coverage отчетов (опционально)

## Поддерживаемые версии Python

- Python 3.7+
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
