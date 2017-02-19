# замена слов в книге на соответствующий перевод
import re
from word_utils import *


if __name__ == "__main__":

    with open('harry_potter.txt', 'r') as file:
        text = file.read()
    # text = text.split()

    known, unknown = load_dicts()
    translation = load_translation()
    trans = combine_dicts(unknown, translation)

    p1 = re.compile('[\W_]+')   # буквенно-цифровые символы
    p2 = re.compile('[^\W_]+')  # пробелы, переносы строк и т.п.
    full_text = []

    words = p1.split(text)
    spaces = p2.split(text)

    i = 0
    for word in words:

        lower = word.lower()
        # lower = pattern.sub('', lower)

        if lower in unknown:
            idx = np.where(lower == trans[:,0])[0]
            if len(idx) > 0:
                t = trans[idx[0],1]
                full_text.append('%s%s /%s/' % (spaces[i], word, t))
        else:
            full_text.append('%s%s' % (spaces[i], word))

        i += 1
    
    text = ''.join(full_text)
    text = re.sub(r'\n(?!\n)', ' ', text)
    text = re.sub(r'\n', '\n\n', text)
    write_to_file('ready.txt', ''.join(text))
    # write_to_file('ready.txt', ''.join(full_text))
