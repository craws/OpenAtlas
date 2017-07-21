# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import bcrypt

import openatlas


class User(object):
    def __init__(self, row):
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
        self.settings = []
        self.bookmarks = []
        self.password_reset_code = row.password_reset_code
        self.password_reset_date = row.password_reset_date
        self.group = row.group_name
        self.created = row.created
        self.modified = row.modified

    def update(self):
        UserMapper.update(self)
        return


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
        cursor.execute(UserMapper.sql + ' WHERE u.id = %(id)s;', {'id': user_id})
        return User(cursor.fetchone())

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
        sql = '''INSERT INTO web.user (username, real_name, info, email, active, password, group_id) VALUES
            (%(username)s, %(real_name)s, %(info)s, %(email)s, %(active)s, %(password)s, %(group_id)s) RETURNING id;'''
        cursor.execute(sql, {
            'username': form.username.data,
            'real_name': form.real_name.data,
            'info': form.description.data,
            'email': form.email.data,
            'active': form.active.data,
            'group_id': 1,
            'password': bcrypt.hashpw(form.password.data, bcrypt.gensalt(12))})
        return cursor.fetchone()[0]

    @staticmethod
    def update(user):
        cursor = openatlas.get_cursor()
        sql = '''UPDATE web.user SET (username, real_name, info, email, active, group_id) =
            (%(username)s, %(real_name)s, %(info)s, %(email)s, %(active)s, %(group_id)s) WHERE id = %(id)s;'''
        cursor.execute(sql, {
            'id': user.id,
            'username': user.username,
            'real_name': user.real_name,
            'info': user.description,
            'email': user.email,
            'active': user.active,
            'group_id': 1})
        return

    @staticmethod
    def delete(user_id):
        sql = 'DELETE FROM web."user" WHERE id = %(user_id)s;'
        openatlas.get_cursor().execute(sql, {'user_id': user_id})
