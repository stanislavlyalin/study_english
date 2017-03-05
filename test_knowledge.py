# скрипт опрашивает пользователя по словарю незнакомых слов
# если пользователь знает слово из незнакомого словаря, оно переносится в словарь знакомых слов
import os
import sys
from db import DB
from word_utils import *


if __name__ == "__main__":

    os.system('cls')

    start = 0
    if len(sys.argv) > 1:
        start = int(sys.argv[1])

    db = DB()
    known, unknown = db.load_dicts()

    for word in unknown[start:, :]:

        if word[0] in known:
            continue
  
        ans = input('do you know: %s ' % word[0])

        if ans == 'y':
            db.write_to_known(word[0])
        elif ans == 'n':
            pass
        else:
            break
