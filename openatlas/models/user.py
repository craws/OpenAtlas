# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import bcrypt
import datetime
from flask import session
from flask_login import UserMixin
import openatlas


class User(UserMixin):
    def __init__(self, row=None, bookmarks=None):
        self.id = None
        self.username = None
        self.email = None
        if not row:
            return
        self.id = row.id
        self.active = True if row.active == 1 else False
        self.username = row.username
        self.password = row.password
        self.login_last_success = row.login_last_success
        self.login_last_failure = row.login_last_failure
        self.login_failed_count = row.login_failed_count
        self.real_name = row.real_name
        self.email = row.email
        self.description = row.info
        self.settings = UserMapper.get_settings(row.id)
        self.bookmarks = bookmarks
        self.password_reset_code = row.password_reset_code
        self.password_reset_date = row.password_reset_date
        self.group = row.group_name
        self.created = row.created
        self.modified = row.modified

    def update(self):
        UserMapper.update(self)
        return

    def login_attempts_exceeded(self):
        if not self.login_last_failure or self.login_failed_count <= int(session['settings']['failed_login_tries']):
            return False
        last_failure_date = self.login_last_failure
        last_failure_date += datetime.timedelta(minutes=int(session['settings']['failed_login_forget_minutes']))
        if last_failure_date > datetime.datetime.now():
            return True
        return False

    def get_setting(self, name, needed_for='system'):
        if name in self.settings:
            return self.settings[name]
        else:
            if needed_for == 'display':
                return ''
        return False


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

    @staticmethod
    def get_by_id(user_id):
        cursor = openatlas.get_cursor()
        sql = 'SELECT entity_id FROM web.user_bookmarks WHERE user_id = %(user_id)s;'
        cursor.execute(sql, {'user_id': user_id})
        bookmarks = []
        for row in cursor.fetchall():
            bookmarks.append(row.entity_id)
        cursor.execute(UserMapper.sql + ' WHERE u.id = %(id)s;', {'id': user_id})
        return User(cursor.fetchone(), bookmarks)

    @staticmethod
    def get_by_email(email):
        cursor = openatlas.get_cursor()
        cursor.execute(UserMapper.sql + ' WHERE u.email = %(email)s;', {'email': email})
        if cursor.rowcount == 1:
            return User(cursor.fetchone())
        return False

    @staticmethod
    def get_by_username(username):
        cursor = openatlas.get_cursor()
        cursor.execute(UserMapper.sql + ' WHERE u.username = %(username)s;', {'username': username})
        if cursor.rowcount == 1:
            return User(cursor.fetchone())
        return False

    @staticmethod
    def insert(form):
        cursor = openatlas.get_cursor()
        sql = '''
            INSERT INTO web.user (username, real_name, info, email, active, password, group_id) VALUES
                (%(username)s, %(real_name)s, %(info)s, %(email)s, %(active)s, %(password)s,
                (SELECT id FROM web.group WHERE name LIKE %(group_name)s))
            RETURNING id;'''
        cursor.execute(sql, {
            'username': form.username.data,
            'real_name': form.real_name.data,
            'info': form.description.data,
            'email': form.email.data,
            'active': form.active.data,
            'group_name': form.group.data,
            'password': bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        })
        return cursor.fetchone()[0]

    @staticmethod
    def update(user):
        cursor = openatlas.get_cursor()
        sql = '''
            UPDATE web.user SET (username, real_name, info, email, active,
                login_last_success, login_last_failure, login_failed_count, group_id) =
                (%(username)s, %(real_name)s, %(info)s, %(email)s, %(active)s,
                %(login_last_success)s, %(login_last_failure)s, %(login_failed_count)s,
                (SELECT id FROM web.group WHERE name LIKE %(group_name)s))
            WHERE id = %(id)s;'''
        cursor.execute(sql, {
            'id': user.id,
            'username': user.username,
            'real_name': user.real_name,
            'info': user.description,
            'email': user.email,
            'active': user.active,
            'group_name': user.group,
            'login_last_success': user.login_last_success,
            'login_last_failure': user.login_last_failure,
            'login_failed_count': user.login_failed_count})
        return

    @staticmethod
    def delete(user_id):
        sql = 'DELETE FROM web."user" WHERE id = %(user_id)s;'
        openatlas.get_cursor().execute(sql, {'user_id': user_id})

    @staticmethod
    def get_groups():
        cursor = openatlas.get_cursor()
        sql = 'SELECT name FROM web.group ORDER BY name;'
        cursor.execute(sql)
        groups = []
        for row in cursor.fetchall():
            groups.append((row.name, row.name))
        return groups

    @staticmethod
    def toggle_bookmark(entity_id, user):
        cursor = openatlas.get_cursor()
        sql = 'INSERT INTO web.user_bookmarks (user_id, entity_id) VALUES (%(user_id)s, %(entity_id)s);'
        label = 'bookmark remove'
        if int(entity_id) in user.bookmarks:
            sql = 'DELETE FROM web.user_bookmarks WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s;'
            label = 'bookmark'
        cursor.execute(sql, {'user_id': user.id, 'entity_id': entity_id})
        return label

    @staticmethod
    def get_settings(user_id):
        cursor = openatlas.get_cursor()
        sql = 'SELECT "name", value FROM web.user_settings WHERE user_id = %(user_id)s;'
        cursor.execute(sql, {'user_id': user_id})
        settings = {}
        for row in cursor.fetchall():
            settings[row.name] = row.value
        return settings
