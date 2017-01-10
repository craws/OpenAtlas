# -*- coding: utf-8 -*-
from collections import OrderedDict
from flask import session

import openatlas


class ContentMapper(object):

    @staticmethod
    def get_content():
        content = OrderedDict()
        for name in ['intro', 'faq', 'contact']:
            content[name] = OrderedDict()
            for language in openatlas.app.config['LANGUAGES'].keys():
                content[name][language] = ''
        cursor = openatlas.get_cursor()
        cursor.execute("SELECT name, language, text FROM web.i18n;")
        for row in cursor.fetchall():
            content[row.name][row.language] = row.text
        return content

    @staticmethod
    def get_translation(name):
        translations = ContentMapper.get_content()[name]
        content = translations[session['language']] if translations[session['language']] else translations['en']
        return content

    @staticmethod
    def update_content(name, form):
        cursor = openatlas.get_cursor()
        cursor.execute('BEGIN')
        for language in openatlas.app.config['LANGUAGES'].keys():
            sql = 'DELETE FROM web.i18n WHERE name = %(name)s AND language = %(language)s'
            cursor.execute(sql, {'name': name, 'language': language})
            sql = 'INSERT INTO web.i18n (name, language, text) VALUES (%(name)s, %(language)s, %(text)s);'
            cursor.execute(sql, {
                'name': name,
                'language': language,
                'text': form.__getattribute__(language).data.strip()
            })
        cursor.execute('COMMIT')
