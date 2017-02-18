import re
from collections import Counter
import numpy as np

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

words_coverage = 0

for word in words_counts:
  
  ans = input('do you know: %s ' % word[0])

  known_dict = open('known_dict.txt', 'a+')
  unknown_dict = open('unknown_dict.txt', 'a+')

  if ans == 'y':
    known_dict.write('%s\n' % word[0])
  elif ans == 'n':
    unknown_dict.write('%s\n' % word[0])
  else:
    break

  words_coverage += int(word[1])

  known_dict.close()
  unknown_dict.close()

  print('coverage = %.2f' % (100.0 * words_coverage / total_words))
