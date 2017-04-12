# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import session

import openatlas


class ClassObject(object):

    code = None
    comment_translated = None
    created = None
    id = None
    modified = None
    name = None
    name_translated = None
    sub = []
    super = []
    i18n = {}

    def get_name_translated(self):
        locale_session = openatlas.get_locale()
        locale_default = session['settings']['default_language']
        if locale_session in self.i18n and 'name' in self.i18n[locale_session]:
            return self.i18n[locale_session]['name']
        elif locale_default in self.i18n and 'name' in self.i18n[locale_default]:
            return self.i18n[locale_default]['name']
        return self.name


class ClassMapper(object):

    @staticmethod
    def get_all():
        sql = """
            SELECT c.id, c.code, c.name, c.created, c.modified,
              COALESCE (
                (SELECT text FROM model.i18n WHERE table_name LIKE 'class' AND table_field LIKE 'name' AND
                  table_id = c.id AND language_code LIKE %(language_code)s),
                (SELECT text FROM model.i18n WHERE table_name LIKE 'class' AND table_field LIKE 'name' AND
                  table_id = c.id AND language_code LIKE %(language_default_code)s)
              ) as name_i18n,
              COALESCE (
                (SELECT text FROM model.i18n WHERE table_name LIKE 'class' AND table_field LIKE 'comment' AND
                  table_id = c.id AND language_code LIKE %(language_code)s),
                (SELECT text FROM model.i18n WHERE table_name LIKE 'class' AND table_field LIKE 'comment' AND
                  table_id = c.id AND language_code LIKE %(language_default_code)s)
              ) as comment_i18n
            FROM model.class c
        """
        classes = {}
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {
            'language_code': 'en',
            'language_default_code': 'en'
        })
        #cursor.execute(sql, {
        #    'language_code': openatlas.get_locale(),
        #    'language_default_code': session['settings']['default_language']
        #})
        for row in cursor.fetchall():
            classes[row.id] = ClassMapper.populate(row)
            classes[row.id].sub = []
            classes[row.id].super = []
        cursor.execute("SELECT text, language_code, table_field, table_id FROM model.i18n WHERE table_name = 'class';")
        for row in cursor.fetchall():
            if row.language_code not in classes[row.table_id].i18n:
                classes[row.table_id].i18n = {row.language_code: {}}
            classes[row.table_id].i18n[row.language_code][row.table_field] = row.text
        cursor.execute('SELECT super_id, sub_id FROM model.class_inheritance;')
        for row in cursor.fetchall():
            classes[row.super_id].sub.append(row.sub_id)
            classes[row.sub_id].super.append(row.super_id)
        return classes

    @staticmethod
    def populate(row):
        object_ = ClassObject()
        object_.id = row.id
        object_.name = row.name
        object_.created = row.created
        object_.modified = row.modified
        object_.code = row.code
        object_.name_translated = row.name_i18n
        object_.comment_translated = row.comment_i18n
        return object_
