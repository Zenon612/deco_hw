import os
import datetime
from functools import wraps
from typing import Callable



def logger(path=None):
    """Параметризованный декоратор для логирования"""

    def __logger(old_function: Callable):
        @wraps(old_function)
        def wrapper(*args, **kwargs):
            if path is None:
                default_dir = "log"
                if not os.path.exists(default_dir):
                    os.makedirs(default_dir)
                actual_log_path = os.path.join(default_dir, "main_p.log")
            else:
                actual_log_path = path
                directory = os.path.dirname(actual_log_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)

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

            with open(actual_log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)

            return res

        return wrapper

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path, "r", encoding="utf-8") as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()