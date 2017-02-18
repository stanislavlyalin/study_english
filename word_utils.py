import re
import numpy as np
from collections import Counter


# загрузка словарей
def load_dicts():

    with open('known_dict.txt') as f:
        content = f.readlines()
    known_dict = np.array([x.strip() for x in content])

    with open('unknown_dict.txt') as f:
        content = f.readlines()
    unknown_dict = np.array([x.strip() for x in content])

    return known_dict, unknown_dict


# загрузка слов-переводов
def load_translation():
    with open('unknown_dict_translated.txt') as f:
        content = f.readlines()
    translation_dict = np.array([x.strip() for x in content])
    return translation_dict


def combine_dicts(unknown, translation):
    a = unknown.reshape(-1, 1)
    b = translation.reshape(-1, 1)
    return np.hstack((a, b))


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


def initial_coverage(known, unknown, words_counts):
    counts = 0

    for word in known:
        idx = (np.where(words_counts[:,0] == word))[0][0]
        counts += int(words_counts[idx, 1])

    for word in unknown:
        idx = (np.where(words_counts[:,0] == word))[0][0]
        counts += int(words_counts[idx, 1])

    return counts


def write_to_file(fname, word):
    file = open(fname, 'a+')
    file.write('%s\n' % word)
    file.close()


def write_to_known(word):
    write_to_file('known_dict.txt', word)


def write_to_unknown(word):
    write_to_file('unknown_dict.txt', word)
