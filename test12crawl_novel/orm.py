# -*- coding:utf-8 -*-

import sqlite3
from sqlite3 import Error as SqlError
import os.path
import datetime
from crwal_novel import crwal, URL
import logging

DB_DIR = r'E:\Git\novel_web\mysite\db.sqlite3'  # 修改这里


def connect_to_db(db_dir=None, default_name='NEW'):
    if db_dir is None:
        db_dir = DB_DIR
    if os.path.isfile(db_dir):
        _conn = sqlite3.connect(db_dir)
    else:
        print('create new db: {}.sqlite3'.format(default_name))
        _conn = sqlite3.connect(os.path.join(db_dir, default_name + '.sqlite3'))
    return _conn


def select(sql, *args, size=None):
    with connect_to_db(DB_DIR) as conn:
        cur = conn.cursor()
        cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = cur.fetchmany(size)
        else:
            rs = cur.fetchall()
        cur.close()
        return rs


def execute(sql, *args):
    with connect_to_db(DB_DIR) as conn:
        try:
            cur = conn.cursor()
            cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            cur.close()
        except BaseException as e:
            raise e
        return affected


def insert(pk_id, chapter, need_confirm, content):
    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.today())
    with connect_to_db(DB_DIR) as conn:
        cur = conn.cursor()
        cur.execute(r'select `id` from novel_site_noveltable where `id` = ?', (pk_id,))
        try:
            if cur.fetchone() is None:  # 若查不到则会返回none
                cur.execute(r'INSERT INTO novel_site_noveltable (`id`, chapter, modified_time, need_confirm, content) '
                            'VALUES (?, ?, ?, ?, ?)', (pk_id, chapter, time, need_confirm, content))
                if cur.rowcount:
                    print('insert: {}'.format(chapter))
            else:
                cur.execute(r'UPDATE novel_site_noveltable SET chapter=?, modified_time=?, need_confirm=?, content=? '
                            'WHERE `id` = ?', (chapter, time, need_confirm, content, pk_id))
                if cur.rowcount:
                    print('update: {}'.format(chapter))

        except SqlError as e:
            print(e)
            conn.rollback()
        finally:
            cur.close()
        conn.commit()


def crete_args_string(num):
    ll = []
    for n in range(num):
        ll.append('?')
    return ', '.join(ll)


class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class ModelMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return type.__new__(mcs, name, bases, attrs)

        table_name = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, table_name))

        mapping = dict()
        fields = []
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                mapping[k] = v
                if v.primary_key:
                    if primary_key:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise RuntimeError('Primary key not found.')
        for k in mapping.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))  # ?????????
        attrs['__mappings__'] = mapping
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key
        attrs['__fields__'] = fields

        attrs['__select__'] = 'select `%s`, `%s` from `%s`  ' % (primary_key, ','.join(escaped_fields), table_name)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (table_name, ','.join(escaped_fields),
                                                                           primary_key, crete_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s` =?' % (table_name, ', '.join(map(lambda f: '`%s`=?'
                                                                                              % (mapping.get(f).name or f),
                                                                                              fields)), primary_key)
        attrs['__deleter__'] = 'delete from `%s` where `%s`=?' % (table_name, primary_key)

        return type.__new__(mcs, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % item)

    def __setattr__(self, key, value):
        self[key] = value

    def get_value(self, key):
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mapping__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value


if __name__ == '__main__':
    # chapter, content = crwal(URL)
    print(tuple is None)
