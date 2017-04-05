# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import session

import openatlas


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
        # remove hardcoded language code
        cursor.execute(sql, {'language_code': 'en', 'language_default_code': 'en'})
        for row in cursor.fetchall():
            # to do: created class class_ and a populate method in mapper
            pass
        return classes
