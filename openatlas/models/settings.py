# Created 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g


class SettingsMapper:

    fields = [
        'debug_mode',
        'default_language',
        'default_table_rows',
        'failed_login_forget_minutes',
        'failed_login_tries',
        'log_level',
        'mail',
        'mail_transport_username',
        'mail_transport_port',
        'mail_transport_host',
        'mail_from_email',
        'mail_from_name',
        'mail_recipients_login',
        'mail_recipients_feedback',
        'minimum_password_length',
        'random_password_length',
        'reset_confirm_hours',
        'site_name']

    @staticmethod
    def get_settings():
        settings = {}
        g.cursor.execute("SELECT name, value FROM web.settings;")
        for row in g.cursor.fetchall():
            settings[row.name] = row.value
            if row.name in [
                'default_table_rows',
                'failed_login_forget_minutes',
                'failed_login_tries',
                'minimum_password_length',
                'random_password_length',
                'reset_confirm_hours'
            ]:
                settings[row.name] = int(row.value)
            elif row.name in ['mail_recipients_login', 'mail_recipients_feedback']:
                settings[row.name] = row.value.split(';')
        return settings

    @staticmethod
    def update(form):
        sql = 'UPDATE web.settings SET "value" = %(value)s WHERE "name" = %(name)s;'
        for field in SettingsMapper.fields:
            value = getattr(form, field).data
            if field in ['debug_mode', 'mail']:
                value = 'True' if getattr(form, field).data else ''
            g.cursor.execute(sql, {'name': field, 'value': value})
