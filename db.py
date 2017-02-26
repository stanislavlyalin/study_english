import os
import re
import sqlite3
import numpy as np


# класс работы с БД
class DB:

    def __init__(self):

        # абсолютный путь к БД
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(BASE_DIR, 'dict.db')

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

        self.cursor.execute('select * from unknown')
        unknown_full = np.array([list(item) for item in self.cursor.fetchall()])
        unknown = unknown_full[:,0].ravel() if len(unknown_full) > 0 else np.array([])

        return known, unknown


    def fill_unknown_dict(self, words, translate):

        known, unknown = self.load_dicts()

        for word_item, trans in zip(words, translate):

            word = word_item[0]
            count = int(word_item[1])
            
            # перевод, состоящий из латинских символов, отбрасывается
            if re.match('^[a-z]+$', trans):
                continue
            # короткие слова и переводы (0 или 1 символ) отбрасываются
            if len(word) < 2 or len(trans) < 2:
                continue

            # нужно проверять, что и в знакомых словах слова нет
            if not word in known and not word in unknown:
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

        if not word in known:
            insert_sql = '''insert into known (word) values('%s');''' % word
            self.cursor.execute(insert_sql)

            delete_sql = '''delete from unknown where word='%s'; ''' % word
            self.cursor.execute(delete_sql)

            self.conn.commit()
