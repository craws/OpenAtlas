# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import session
import openatlas


class SettingsMapper(object):

    fields = ['site_name', 'default_language', 'default_table_rows', 'log_level', 'maintenance', 'offline', 'mail',
              'mail_transport_username', 'mail_transport_host', 'mail_transport_port', 'mail_transport_type',
              'mail_transport_ssl', 'mail_transport_auth', 'mail_from_email', 'mail_from_name', 'mail_recipients_login',
              'mail_recipients_feedback', 'random_password_length', 'reset_confirm_hours', 'failed_login_tries',
              'failed_login_forget_minutes']

    @staticmethod
    def get_settings():
        settings = {}
        cursor = openatlas.get_cursor()
        cursor.execute("SELECT name, value FROM web.settings;")
        for row in cursor.fetchall():
            settings[row.name] = row.value
        return settings

    @staticmethod
    def update(form):
        sql = 'UPDATE web.settings SET "value" = %(value)s WHERE "name" = %(name)s;'
        for field in SettingsMapper.fields:
            session['settings'][field] = getattr(form, field).data
        for name, value in session['settings'].items():
            cursor = openatlas.get_cursor()
            cursor.execute(sql, {'value': value, 'name': name})
