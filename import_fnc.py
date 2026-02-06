from main import logger
import json


@logger
def read_json(file_path, word_min_len=7, top_words_amt=10):
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            words = []
            for item in data['rss']['channel']['items']:
                words.extend(item['description'].split())

            counts = {}
            for word in words:
                if len(word) >= word_min_len:
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1

            sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            top_words = [word for word, count in sorted_words[:top_words_amt]]
    return top_words

read_json('newsafr.json')