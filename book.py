import os
from word_utils import *


if __name__ == "__main__":

    os.system('cls')

    known, unknown = load_dicts()

    words_counts, total_words = words_of_book('harry_potter.txt')
    print('общее число слов в книге: ' + str(total_words))

    words_coverage = initial_coverage(known, unknown, words_counts)

    for word in words_counts:

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
        print('coverage = %.2f' % (100.0 * words_coverage / total_words))
