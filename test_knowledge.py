# скрипт опрашивает пользователя по словарю незнакомых слов
# если пользователь знает слово из незнакомого словаря, оно переносится в словарь знакомых слов
import os
from db import DB
from word_utils import *


if __name__ == "__main__":

    os.system('cls')

    db = DB()
    known, unknown = db.load_dicts()

    for word in unknown:

        if word in known:
            continue
  
        ans = input('do you know: %s ' % word)

        # TODO: по нажатию на кнопку нужно показать перевод, а только потом спросить пользователя y или n

        if ans == 'y':
            db.write_to_known(word)
        elif ans == 'n':
            pass
        else:
            break
