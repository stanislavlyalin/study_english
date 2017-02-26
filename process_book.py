import os
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

    # подготовка слов для Яндекс.переводчика
    key = 'trnsl.1.1.20170221T194012Z.9440c67d9bb5681d.b51b9261979862c60b232cd040264c5af034b018'
    # translate = yandex_translate(words[:,0], key)
    translate = yandex_translate(words[:100,0], key)

    # пополнение словарей извлечёнными словами
    db = DB()
    db.fill_unknown_dict(words[:100], translate)
