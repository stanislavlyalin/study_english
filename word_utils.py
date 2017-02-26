import re
import numpy as np
import os
import urllib.request
import json
from collections import Counter


# перевод массива английских слов на русский с помощью переводчика Яндекс
def yandex_translate(words, key):

    words_to_translate = 100
    translate = []

    for i in range(0, len(words), words_to_translate):
        sub_words = words[i:i+words_to_translate]
        text_en = '. '.join(sub_words)
        request = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&text=%s&lang=en-ru' % (key, text_en)
        ans = urllib.request.urlopen(request).read().decode('utf-8')
        translate.append(json.loads(ans)['text'][0].lower().split('. '))

    return np.array(translate).ravel()


# определение встречания слов в книге
def words_of_book(book_filename):
    # загрузка текста книги
    with open(book_filename, 'r') as file:
        text = file.read()

    # разделение на отдельные слова
    words = text.lower().split()

    # удаление не буквенно-цифровых символов каждого слова
    pattern = re.compile('[\W_]+')
    words = [pattern.sub('', item) for item in words]

    total_words = len(words)

    # вычисление частоты встречания каждого слова
    words_counts = Counter(words)

    # сортировка по частоте встречания слов
    words_counts = sorted(words_counts.items(), key=lambda item: item[1], reverse=True)

    # преобразование к массиву NumPy
    return np.array([[key, val] for key, val in words_counts]), total_words

