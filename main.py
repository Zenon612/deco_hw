import os
from functools import wraps
import datetime
from typing import Callable
import json


def read_json(file_path: str, word_min_len: int = 7, top_words_amt: int = 10) -> list[str]:
    """
    Читает JSON-файл с RSS-лентой и возвращает список наиболее частых слов.

    :param file_path: Путь к JSON-файлу с RSS-данными
    :param word_min_len: Минимальная длина слова для учёта
    :param top_words_amt: Количество топ-слов для возврата
    :return: Список наиболее часто встречающихся слов длиной >= word_min_len
    :raises ValueError: Если файл не имеет расширения .json
    :raises KeyError: Если структура JSON не соответствует ожидаемой
    """
    if not file_path.endswith('.json'):
        raise ValueError("Файл должен иметь расширение .json")

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        words = []
        for item in data['rss']['channel']['items']:
            words.extend(item['description'].split())

        counts = {}
        for word in words:
            if len(word) >= word_min_len:
                counts[word] = counts.get(word, 0) + 1

        sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        top_words = [word for word, count in sorted_words[:top_words_amt]]

    return top_words


def logger(old_function: Callable):
    """
    Декоратор для логирования вызовов функций.

    Записывает в файл main.log дату и время вызова, имя функции, аргументы,
    время выполнения и результат (или информацию об ошибке).

    :param old_function: Функция для обёртывания
    :return: Обёрнутая функция с логированием
    """
    path = '.'

    if not os.path.exists(path):
        os.makedirs(path)
    log_file_path = os.path.join(path, 'main.log')

    @wraps(old_function) # без него не сохранит данные функции, например докстринг
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        try:
            res = old_function(*args, **kwargs)
            exception_info = None
        except Exception as e:
            res = None
            exception_info = str(e)

        end_time = datetime.datetime.now()
        execute_time = end_time - start_time

        log_entry = f"""
Дата и время: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
Имя функции: {old_function.__name__}
Аргументы: {args}, {kwargs}
Время выполнения: {execute_time}"""

        if exception_info:
            log_entry += f"\nОшибка: {exception_info}\n"
        else:
            log_entry += f"\nФункция возвращает: {repr(res)}\n"

        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        return res

    return wrapper


def test_1():
    """Тест для декоратора logger из main.py"""
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)


    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)
    read_json('newsafr.json')

    with open(path, "r", encoding="utf-8") as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
    