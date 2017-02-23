import os
import sys
from word_utils import *


if __name__ == "__main__":

    os.system('cls')

    # разбор параметров командной строки
    input_book = sys.argv[1]
    output_book = sys.argv[2]

    # извлечение списка слов из переданной книги
    words_counts, total_words = words_of_book(input_book)
    print('общее число слов в книге: ' + str(total_words))
    print('уникальных слов: ' + str(len(words_counts)))

    # загрузка словарей
    known, unknown = load_dicts()

    # подготовка слов для Яндекс.переводчика

    words_coverage = initial_coverage(known, unknown, words_counts)
    counter = 0

    for word in words_counts:

        counter += 1

        # обработаные ранее слова нужно пропустить
        if word[0] in known or word[0] in unknown:
            continue
  
        ans = input('do you know: %s [%d] ' % (word[0], int(word[1])))

        if ans == 'y':
            write_to_known(word[0])
        elif ans == 'n':
            write_to_unknown(word[0])
        else:
            break

        # вывод процента покрытия книги известными словами
        words_coverage += int(word[1])
        print('progress %.2f, coverage %.2f' % (100.0 * counter / len(words_counts), 100.0 * words_coverage / total_words))
