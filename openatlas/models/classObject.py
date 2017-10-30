# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import session
import openatlas
from openatlas import app


class ClassObject(object):

    def __init__(self, row):
        self._comment = ''
        self._name = row.name
        self.code = row.code
        self.id = row.id
        self.i18n = {}
        self.sub = []
        self.super = []

    @property
    def name(self):
        return self.get_i18n('name')

    @property
    def comment(self):
        return self.get_i18n('comment')

    def get_i18n(self, attribute):
        locale_session = openatlas.get_locale()
        locale_default = session['settings']['default_language']
        if locale_session in self.i18n and attribute in self.i18n[locale_session]:
            return self.i18n[locale_session][attribute]
        elif locale_default in self.i18n and attribute in self.i18n[locale_default]:
            return self.i18n[locale_default][attribute]
        return getattr(self, '_' + attribute)


class ClassMapper(object):

    @staticmethod
    def get_all():
        classes = {}
        cursor = openatlas.get_cursor()
        cursor.execute("SELECT id, code, name FROM model.class;")
        for row in cursor.fetchall():
            classes[row.id] = ClassObject(row)
        cursor.execute("SELECT super_id, sub_id FROM model.class_inheritance;")
        for row in cursor.fetchall():
            classes[row.super_id].sub.append(row.sub_id)
            classes[row.sub_id].super.append(row.super_id)
        sql = """
            SELECT text, language_code, table_field, table_id
            FROM model.i18n
            WHERE table_name = 'class' AND language_code IN %(language_codes)s;"""
        cursor.execute(sql, {'language_codes': tuple(app.config['LANGUAGES'].keys())})
        for row in cursor.fetchall():
            class_ = classes[row.table_id]
            if row.language_code not in class_.i18n:
                class_.i18n[row.language_code] = {}
            class_.i18n[row.language_code][row.table_field] = row.text
        return classes

    @staticmethod
    def get_by_code(code):
        for id_, class_ in openatlas.classes.items():
            if class_.code == code:
                return class_
