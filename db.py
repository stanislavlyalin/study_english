import os
import re
import sqlite3
import numpy as np


# класс работы с БД
class DB:

    def __init__(self):

        # абсолютный путь к БД
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(base_dir, 'dict.db')

        # создание БД, если не существует
        if not os.path.isfile(self.db_name):
            self.create_db()

        # подключение к БД
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_db(self):

        try:
            conn = sqlite3.connect(self.db_name)
        finally:
            conn.close()
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # создание таблицы знакомых слов
            create_known_table_sql = '''
                create table if not exists known (
                    word text not null
                );'''
            cursor.execute(create_known_table_sql)

            # создание таблицы незнакомых слов
            create_unknown_table_sql = '''
                create table if not exists unknown
                (
                    word text not null,
                    translate text not null,
                    count integer not null
                );'''
            cursor.execute(create_unknown_table_sql)

            conn.commit()
        finally:
            conn.close()

    def load_dicts(self):

        self.cursor.execute('select word from known')
        known = np.array(self.cursor.fetchall()).ravel()

        self.cursor.execute('select * from unknown order by count desc')
        unknown_full = np.array([list(item) for item in self.cursor.fetchall()])
        unknown = unknown_full

        return known, unknown

    def fill_unknown_dict(self, en_word, trans):

        known, unknown = self.load_dicts()

        word = en_word[0]
        count = int(en_word[1])

        # перевод, состоящий из латинских символов, отбрасывается
        if re.match('^[a-z]+$', trans):
            return
        # короткие слова и переводы (0 или 1 символ) отбрасываются
        if len(word) < 2 or len(trans) < 2:
            return

        # слова, для которых переводчик выдал то же слово, отбрасываются
        if word == trans:
            return

        # нужно проверять, что и в знакомых словах слова нет
        if word not in known and word not in unknown:
            insert_sql = '''
                insert into unknown(word, translate, count)
                values('%s', '%s', %d);''' % (word, trans, count)
            self.cursor.execute(insert_sql)
        else:
            update_sql = '''
                update unknown set count=%d where word='%s';''' % (count, word)
            self.cursor.execute(update_sql)

        self.conn.commit()

    def write_to_known(self, word):

        known, unknown = self.load_dicts()

        if word not in known:
            insert_sql = '''insert into known (word) values('%s');''' % word
            self.cursor.execute(insert_sql)

            delete_sql = '''delete from unknown where word='%s'; ''' % word
            self.cursor.execute(delete_sql)

            self.conn.commit()
