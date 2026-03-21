from main import logger
import json


@logger
def read_json(file_path: str, word_min_len: int = 7, top_words_amt: int = 10) -> list[str]:
    """
    Читает JSON-файл с RSS-лентой и возвращает список наиболее частых слов.

    Функция оборачивается декоратором @logger для логирования вызовов.

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


if __name__ == '__main__':
    read_json('newsafr.json')