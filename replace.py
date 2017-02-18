# замена слов в книге на соответствующий перевод
import re
from word_utils import *


if __name__ == "__main__":

    with open('harry_potter.txt', 'r') as file:
        text = file.read()
    text = text.split()

    known, unknown = load_dicts()
    translation = load_translation()
    trans = combine_dicts(unknown, translation)

    pattern = re.compile('[\W_]+')
    full_text = []

    for word in text:

        lower = word.lower()
        lower = pattern.sub('', lower)

        if lower in unknown:
            idx = np.where(lower == trans[:,0])[0]
            if len(idx) > 0:
                t = trans[idx[0],1]
                full_text.append('%s /%s/' % (word, t))
        else:
            full_text.append(word)
    
    write_to_file('ready.txt', ' '.join(full_text))
