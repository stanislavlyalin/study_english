import os
import re
import sys
from db import DB
from word_utils import *


if __name__ == "__main__":

    os.system('cls')

    # разбор параметров командной строки
    input_book = sys.argv[1]
    output_book = sys.argv[2]

    # извлечение списка слов из переданной книги
    words, total_words = words_of_book(input_book)
    print('общее число слов в книге: ' + str(total_words))
    print('уникальных слов: ' + str(len(words)))

    # TODO: переводить нужно только те слова, которых нет в словарях знакомых/незнакомых слов

    # подготовка слов для Яндекс.переводчика
    key = 'trnsl.1.1.20170221T194012Z.9440c67d9bb5681d.b51b9261979862c60b232cd040264c5af034b018'
    translate = yandex_translate(words[:,0], key)
    # translate = yandex_translate(words[:100,0], key)

    # пополнение словарей извлечёнными словами
    db = DB()
    db.fill_unknown_dict(words, translate)

    # подготовка книги (замена английских слов переводом)
    known, unknown = db.load_dicts()
    p1 = re.compile('[\W_]+')   # буквенно-цифровые символы
    p2 = re.compile('[^\W_]+')  # пробелы, переносы строк и т.п.

    with open(input_book) as file:
        text = file.read()

    words = p1.split(text)
    spaces = p2.split(text)
    full_text = []

    i = 0
    for word in words:

        lower = word.lower()

        if lower in unknown:
            idx = np.where(lower == unknown[:, 0])[0]
            if len(idx) > 0:
                t = unknown[idx[0], 1]
                full_text.append('%s%s /%s/' % (spaces[i], word, t))
        else:
            full_text.append('%s%s' % (spaces[i], word))

        i += 1

    text = ''.join(full_text)
    text = re.sub(r'\n(?!\n)', ' ', text)
    text = re.sub(r'\n', '\n\n', text)

    write_to_file(output_book, ''.join(full_text))
