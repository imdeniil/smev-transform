# SMEV Transform (Python) v2.0

**Полная реализация алгоритма трансформации "urn://smev-gov-ru/xmldsig/transform" для Python согласно официальной документации СМЭВ 3.5.0.27.**

Это улучшенный порт оригинальной PHP библиотеки [danbka/smev-transform](https://github.com/danbka/smev-transform) на Python с **полной поддержкой всех 9 шагов трансформации**.

> **Примечание:** Эта библиотека является компонентом основного проекта [giis-signer](https://github.com/imdeniil/giis-signer) - инструмента для работы с электронной подписью и СМЭВ3.

## 📚 Документация СМЭВ

Алгоритм адаптирован для **СМЭВ версии 3.5.0.27** согласно официальной документации:
- [Методические документы СМЭВ3](https://info.gosuslugi.ru/docs/section/%D0%A1%D0%9C%D0%AD%D0%92/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5_%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/%D0%A1%D0%9C%D0%AD%D0%923/?id=758)
- Версия спецификации: 3.5.0.27

## 🆕 Новое в версии 2.0

**КРИТИЧЕСКОЕ ОБНОВЛЕНИЕ:** Добавлена полная поддержка **Шага 9 - Декодирование текста**, который отсутствовал в оригинальной PHP библиотеке!

### Что добавлено:

✅ **Шаг 9.1 - Декодирование текстовых блоков:**
- Снятие экранирования символов (`&#xd;`, `&lt;`, `&amp;` и др.)
- Корректная обработка CDATA секций
- Умное кодирование блоков по размеру (до 11 символов / от 12 символов)
- Условное кодирование символа `>` согласно спецификации

✅ **Шаг 9.2 - Декодирование атрибутов:**
- Нормализация пробельных символов в атрибутах
- Снятие экранирования в значениях атрибутов
- Правильное кодирование атрибутов

## Описание

При подписании XML-фрагментов ЭП в формате XMLDSig, обязательно использование трансформации urn://smev-gov-ru/xmldsig/transform.

## Полный алгоритм трансформации (9 шагов)

1. ✅ **XML declaration и processing instructions** удаляются
2. ✅ **Пробельные символы** удаляются из текстовых узлов
3. ✅ **Empty element tags** преобразуются в пары start-tag + end-tag
4. ✅ **Неиспользуемые namespace prefix** удаляются
5. ✅ **Namespace declarations** проверяются и добавляются при необходимости
6. ✅ **Автоматические префиксы** генерируются (ns1, ns2, ...)
7. ✅ **Атрибуты сортируются** в алфавитном порядке
8. ✅ **Namespace declarations** размещаются перед атрибутами
9. ✅ **Декодирование текста** (НОВОЕ!) - полная обработка текстовых блоков и атрибутов

## Установка

### Из PyPI (рекомендовано)
```bash
pip install smev-transform
```

### Из исходников
```bash
git clone https://github.com/imdeniil/smev-transform
cd smev-transform
pip install -e .
```

### С использованием uv
```bash
uv pip install smev-transform
```

## Использование

### Базовое использование
```python
from smev_transform import Transform

transform = Transform()
result = transform.process(xml_string)
```

### Использование отдельных компонентов
```python
from smev_transform import TextDecoder, AttributeDecoder

# Декодирование текстовых блоков
decoded_text = TextDecoder.decode_text_block(text_with_entities)

# Декодирование атрибутов
decoded_attr = AttributeDecoder.decode_attribute_value(attr_value)
```

## Примеры

### Пример 1: Базовая трансформация
```python
from smev_transform import Transform

xml = '''<?xml version="1.0" encoding="UTF-8"?>
<elementOne xmlns="http://test/1" xmlns:qwe="http://test/2">
    <qwe:elementTwo attB="bbb" attA="aaa"/>
</elementOne>'''

transform = Transform()
result = transform.process(xml)

print(result)
# Результат: <ns1:elementOne xmlns:ns1="http://test/1"><ns2:elementTwo xmlns:ns2="http://test/2" attA="aaa" attB="bbb"></ns2:elementTwo></ns1:elementOne>
```

### Пример 2: Обработка текста с экранированием (Шаг 9.1)
```python
from smev_transform import Transform

xml = '''<root>&gt;&gt;text&amp;content&lt;</root>'''

transform = Transform()
result = transform.process(xml)

print(result)
# Текст проходит декодирование согласно алгоритму СМЭВ
```

### Пример 3: Обработка атрибутов с пробелами (Шаг 9.2)
```python
from smev_transform import Transform

xml = '''<root attr="value	with	tabs and
newlines"/>'''

transform = Transform()
result = transform.process(xml)

print(result)
# Пробельные символы в атрибутах нормализуются согласно СМЭВ
```

### Пример 4: CDATA секции
```python
from smev_transform import Transform

xml = '''<root>
    Текст до CDATA
    <![CDATA[Сырой контент < & > остается нетронутым]]>
    Текст после CDATA
</root>'''

transform = Transform()
result = transform.process(xml)
# CDATA секции обрабатываются корректно согласно спецификации
```

## Тестирование

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Конкретные тесты
pytest smev_transform/tests/test_transform.py -v
pytest smev_transform/tests/test_text_decoder.py -v
pytest smev_transform/tests/test_attribute_decoder.py -v

# С покрытием кода
pytest --cov=smev_transform --cov-report=html
```

## Различия с оригинальной PHP библиотекой

| Функциональность | PHP версия | Python v2.0 |
|-----------------|------------|---------------|
| Шаги 1-8 (базовая трансформация) | ✅ | ✅ |
| Шаг 9.1 (декодирование текста) | ❌ **ОТСУТСТВУЕТ** | ✅ **РЕАЛИЗОВАНО** |
| Шаг 9.2 (декодирование атрибутов) | ❌ **ОТСУТСТВУЕТ** | ✅ **РЕАЛИЗОВАНО** |
| Обработка CDATA | ⚠️ Частично | ✅ Полностью |
| Соответствие официальной спецификации | ⚠️ 89% | ✅ **100%** |

## Требования

- Python 3.7+
- Только стандартная библиотека Python (xml.etree.ElementTree)

## Структура проекта

```
smev-transform/
├── smev_transform/              # Основной пакет
│   ├── __init__.py              # Инициализация модуля
│   ├── transform.py             # Главный класс Transform
│   ├── text_decoder.py          # Декодирование текстовых блоков (Шаг 9.1)
│   ├── attribute_decoder.py     # Декодирование атрибутов (Шаг 9.2)
│   ├── xml_namespace.py         # Работа с XML namespaces
│   ├── attribute.py             # Представление XML атрибутов
│   ├── comparators.py           # Сортировка атрибутов
│   ├── exceptions.py            # Исключения
│   └── tests/                   # Тесты пакета
│       ├── test_transform.py
│       ├── test_text_decoder.py
│       └── test_attribute_decoder.py
├── docs/                        # Документация
│   ├── CHANGELOG.md
│   ├── CLASSES.md
│   ├── FILES.md
│   ├── TECH.md
│   └── TRANSIT.md
├── setup.py                     # Конфигурация setuptools
├── pyproject.toml               # Современная конфигурация пакета
├── README.md                    # Этот файл
├── LICENSE                      # MIT License
└── requirements.txt             # Dev зависимости
```

## Совместимость и миграция

### Миграция с версии 1.0:
- **API полностью совместимо** - никаких изменений в коде не требуется
- Результаты трансформации могут отличаться из-за добавления Шага 9
- Рекомендуется протестировать с реальными СМЭВ сообщениями

### Для продакшен-использования:
- ✅ Версия 2.0 **рекомендована** для всех новых проектов
- ✅ Полное соответствие официальной документации СМЭВ3
- ✅ Корректная работа с реальными СМЭВ сообщениями

## Разработка

### Начало работы

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/imdeniil/smev-transform
   cd smev-transform
   ```

2. **Создайте виртуальное окружение с uv:**
   ```bash
   uv venv
   ```

3. **Активируйте окружение:**
   ```bash
   # Windows
   .venv\Scripts\activate

   # Linux/macOS
   source .venv/bin/activate
   ```

4. **Синхронизируйте зависимости:**
   ```bash
   uv sync
   ```

### Установка в режиме разработки

```bash
# С dev зависимостями
uv pip install -e ".[dev]"

# Или напрямую
pip install -e ".[dev]"
```

### Запуск тестов

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# С покрытием кода
pytest --cov=smev_transform --cov-report=html
```

### Публикация на PyPI

```bash
# Сборка пакета
uv build

# Публикация (требуется API token)
uv publish
```

## Ссылки

- 📦 [PyPI Package](https://pypi.org/project/smev-transform/)
- 🐙 [GitHub Repository](https://github.com/imdeniil/smev-transform)
- 📚 [СМЭВ3 Документация](https://info.gosuslugi.ru/docs/section/%D0%A1%D0%9C%D0%AD%D0%92/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5_%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/%D0%A1%D0%9C%D0%AD%D0%923/?id=758)
- 🔗 [Оригинальная PHP библиотека](https://github.com/danbka/smev-transform)

## Автор

**Daniil** ([@imdeniil](https://github.com/imdeniil))
- Email: keemor821@gmail.com
- GitHub: https://github.com/imdeniil/

## Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.

---

**⚠️ ВАЖНО:** Если вы используете эту библиотеку для интеграции с СМЭВ3, настоятельно рекомендуется использовать версию 2.0, так как она включает все требования официальной спецификации СМЭВ 3.5.0.27.

## Поддержка

Если вы обнаружили баг или у вас есть предложения по улучшению, пожалуйста, создайте [issue на GitHub](https://github.com/imdeniil/smev-transform/issues).