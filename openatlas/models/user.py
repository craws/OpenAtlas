# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import openatlas


class User(object):
    def __init__(self, row):
        self.active = True if row.active == 1 else False
        self.username = row.username
        self.password = row.password
        self.login_last_success = row.login_last_success
        self.login_last_failure = row.login_last_failure
        self.login_failed_count = row.login_failed_count
        self.real_name = row.real_name
        self.email = row.email
        self.info = row.info
        self.settings = []
        self.bookmarks = []
        self.password_reset_code = row.password_reset_code
        self.password_reset_date = row.password_reset_date
        self.group = row.group_name
        self.created = row.created
        self.modified = row.modified


class UserMapper(object):
    sql = '''
        SELECT u.id, u.username, u.password, u.active, u.real_name, u.info, u.created, u.modified,
            u.login_last_success, u.login_last_failure, u.login_failed_count, u.password_reset_code,
            u.password_reset_date, u.email, r.name as group_name
        FROM web."user" u
        LEFT JOIN web.group r ON u.group_id = r.id'''

    @staticmethod
    def get_all():
        cursor = openatlas.get_cursor()
        cursor.execute(UserMapper.sql)
        users = []
        for row in cursor.fetchall():
            users.append(User(row))
        openatlas.debug_model['user'] += 1
        return users
