# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import openatlas


class SettingsMapper(object):

    @staticmethod
    def get_settings():
        settings = {}
        cursor = openatlas.get_cursor()
        cursor.execute("SELECT name, value FROM web.settings;")
        for row in cursor.fetchall():
            settings[row.name] = row.value
        return settings
