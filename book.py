import re
import goslate
from collections import Counter
import numpy as np

gs = goslate.Goslate()

# загрузка текста книги
with open('harry_potter.txt', 'r') as file:
  text = file.read()

# разделение на отдельные слова
words = text.lower().split()

# удаление не буквенно-цифровых символов каждого слова
pattern = re.compile('[\W_]+')
words = [pattern.sub('', item) for item in words]

total_words = len(words)
print('общее число слов в книге: ' + str(total_words))

# вычисление частоты встречания каждого слова
words_counts = Counter(words)

# сортировка по частоте встречания слов
words_counts = sorted(words_counts.items(), key=lambda item: item[1], reverse=True)

# преобразование к массиву NumPy
words_counts = np.array([[key, val] for key, val in words_counts])

known_words = 0
unknown_words = 0
words_coverage = 0



for word in words_counts:
  ans = input('do you know ' + word[0] + ' ')
  if ans == 'y':
    known_words += 1
    words_coverage += int(word[1])
  elif ans == 'n':
    unknown_words += 1
    words_coverage += int(word[1])
    # trans = gs.translate(word[0], 'ru')

    # print('%s;%s' % (word[0], trans))

    dict_file = open('dict.txt', 'a+')
    dict_file.write('%s\n' % word[0])
    dict_file.close()
  else:
    break
  print('coverage = %.2f' % (100.0 * words_coverage / total_words))
