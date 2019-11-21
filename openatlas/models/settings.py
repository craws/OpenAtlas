# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Dict

from flask import g


class SettingsMapper:
    fields = {'debug_mode',
              'default_language',
              'default_table_rows',
              'failed_login_forget_minutes',
              'failed_login_tries',
              'file_upload_max_size',
              'file_upload_allowed_extension',
              'log_level',
              'mail',
              'mail_transport_username',
              'mail_transport_port',
              'mail_transport_host',
              'mail_from_email',
              'mail_from_name',
              'map_cluster_enabled',
              'map_cluster_max_radius',
              'map_cluster_disable_at_zoom',
              'mail_recipients_feedback',
              'minimum_password_length',
              'minimum_jstree_search',
              'minimum_tablesorter_search',
              'profile_image_width',
              'random_password_length',
              'reset_confirm_hours',
              'site_name',
              'site_header'}

    @staticmethod
    def get_settings() -> Dict:
        g.execute("SELECT name, value FROM web.settings;")
        settings = {}
        for row in g.cursor.fetchall():
            settings[row.name] = row.value
            if row.name in ['default_table_rows',
                            'failed_login_forget_minutes',
                            'failed_login_tries',
                            'file_upload_max_size',
                            'minimum_password_length',
                            'random_password_length',
                            'reset_confirm_hours']:
                settings[row.name] = int(row.value)
            elif row.name in ['mail_recipients_feedback']:
                settings[row.name] = row.value.split(';')
        return settings

    @staticmethod
    def update(form) -> None:
        sql = 'UPDATE web.settings SET "value" = %(value)s WHERE "name" = %(name)s;'
        for field in SettingsMapper.fields:
            if field in form:
                value = getattr(form, field).data
                if field in ['debug_mode', 'mail']:
                    value = 'True' if getattr(form, field).data else ''
                g.execute(sql, {'name': field, 'value': value})

    @staticmethod
    def update_file_settings(form) -> None:
        sql = 'UPDATE web.settings SET "value" = %(value)s WHERE "name" = %(name)s;'
        for field in SettingsMapper.fields:
            if field.startswith('file_') or field == 'profile_image_width':
                value = getattr(form, field).data
                g.execute(sql, {'name': field, 'value': value})

    @staticmethod
    def update_map_settings(form) -> None:
        sql = 'UPDATE web.settings SET "value" = %(value)s WHERE "name" = %(name)s;'
        for field in SettingsMapper.fields:
            if not field.startswith('map_'):
                continue
            value = getattr(form, field).data
            if field == 'map_cluster_enabled':
                value = 'True' if getattr(form, field).data else ''
            g.execute(sql, {'name': field, 'value': value})

    @staticmethod
    def set_logo(file_id: int = None) -> None:
        sql = "UPDATE web.settings SET value = %(file_id)s WHERE name = 'logo_file_id';"
        g.execute(sql, {'file_id': file_id if file_id else ''})
