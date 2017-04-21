# -*- coding:utf-8 -*-

import sqlite3
from sqlite3 import OperationalError
import os.path
import datetime
from crwal_novel import crwal, URL

DB_DIR = r'F:\Git\novel_web\mysite\db.sqlite3'


def connect_to_db(db_dir, default_name='NEW'):
    if os.path.isfile(db_dir):
        _conn = sqlite3.connect(db_dir)
    else:
        print('create new db: {}.sqlite3'.format(default_name))
        _conn = sqlite3.connect(os.path.join(db_dir, default_name + '.sqlite3'))
    return _conn


def select(sql, *args, size=None):
    pass


# def execute(sql, *args):
#     pass

def insert(chapter, content):
    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.today())
    with connect_to_db(DB_DIR) as conn:
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO novel_site_noveltable (chapter, modified_time, content) '
                        'VALUES (?, ?, ?)', (chapter, time, content))
            if cur.rowcount:
                print('success')
        except OperationalError:
            conn.rollback()
        finally:
            cur.close()
        conn.commit()


if __name__ == '__main__':
    # chapter, content = crwal(URL)
    pass