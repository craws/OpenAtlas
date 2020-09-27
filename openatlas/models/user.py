from __future__ import annotations  # Needed for Python 4.0 type annotations

import datetime
import secrets
import string
from typing import Any, Dict, List, Optional, Tuple, Union

import bcrypt
from flask import g, session
from flask_babel import lazy_gettext as _
from flask_login import UserMixin, current_user
from flask_wtf import FlaskForm
from psycopg2.extras import NamedTupleCursor
from werkzeug.exceptions import abort

from openatlas.models.entity import Entity
from openatlas.util.util import is_authorized


class User(UserMixin):  # type: ignore

    sql = """
        SELECT u.id, u.username, u.password, u.active, u.real_name, u.info, u.created, u.modified,
            u.login_last_success, u.login_last_failure, u.login_failed_count, u.password_reset_code,
            u.password_reset_date, u.email, r.name as group_name, u.unsubscribe_code
        FROM web."user" u
        LEFT JOIN web.group r ON u.group_id = r.id """

    def __init__(self,
                 row: NamedTupleCursor.Record = None,
                 bookmarks: Optional[List[int]] = None) -> None:
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
        self.settings = User.get_settings(row.id)
        self.bookmarks = bookmarks
        self.password_reset_code = row.password_reset_code
        self.password_reset_date = row.password_reset_date
        self.unsubscribe_code = row.unsubscribe_code
        self.group = row.group_name
        self.created = row.created
        self.modified = row.modified

    def update(self) -> None:
        sql = """
            UPDATE web.user SET (username, password, real_name, info, email, active,
                login_last_success, login_last_failure, login_failed_count, group_id,
                password_reset_code, password_reset_date, unsubscribe_code) =
            (%(username)s, %(password)s, %(real_name)s, %(info)s, %(email)s, %(active)s,
                %(login_last_success)s, %(login_last_failure)s, %(login_failed_count)s,
                (SELECT id FROM web.group WHERE name LIKE %(group_name)s),
                %(password_reset_code)s, %(password_reset_date)s, %(unsubscribe_code)s)
            WHERE id = %(id)s;"""
        g.execute(sql, {'id': self.id,
                        'username': self.username,
                        'real_name': self.real_name,
                        'password': self.password,
                        'info': self.description,
                        'email': self.email,
                        'active': self.active,
                        'group_name': self.group,
                        'login_last_success': self.login_last_success,
                        'login_last_failure': self.login_last_failure,
                        'login_failed_count': self.login_failed_count,
                        'unsubscribe_code': self.unsubscribe_code,
                        'password_reset_code': self.password_reset_code,
                        'password_reset_date': self.password_reset_date})

    def update_settings(self, form: Any) -> None:
        for field in form:
            if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField'] or \
                    field.name in ['name', 'email']:
                continue
            value = field.data
            if field.type == 'BooleanField':
                value = 'True' if value else ''
            elif field.type == 'IntegerField' or field.name == 'table_rows':
                value = int(value)
            sql = """
                INSERT INTO web.user_settings (user_id, "name", "value")
                VALUES (%(user_id)s, %(name)s, %(value)s)
                ON CONFLICT (user_id, name) DO UPDATE SET "value" = excluded.value;"""
            g.execute(sql, {'user_id': self.id, 'name': field.name, 'value': value})

    def remove_newsletter(self) -> None:  # pragma: no cover
        sql = "DELETE FROM web.user_settings WHERE name = 'newsletter' AND user_id = %(user_id)s;"
        g.execute(sql, {'user_id': self.id})

    def update_language(self) -> None:
        sql = """
            INSERT INTO web.user_settings (user_id, "name", "value")
            VALUES (%(user_id)s, 'language', %(value)s)
            ON CONFLICT (user_id, name) DO UPDATE SET "value" = excluded.value;"""
        g.execute(sql, {'user_id': self.id, 'value': current_user.settings['language']})

    def login_attempts_exceeded(self) -> bool:
        failed_login_tries = int(session['settings']['failed_login_tries'])
        if not self.login_last_failure or self.login_failed_count < failed_login_tries:
            return False
        last_failure_date = self.login_last_failure
        forget_minutes = int(session['settings']['failed_login_forget_minutes'])
        last_failure_date += datetime.timedelta(minutes=forget_minutes)
        if last_failure_date > datetime.datetime.now():
            return True
        return False  # pragma no cover - not waiting in tests for forget_minutes to pass

    @staticmethod
    def get_all() -> List[User]:
        g.execute(User.sql + ' ORDER BY username;')
        return [User(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_id(user_id: int, with_bookmarks: bool = False):  # type: ignore
        bookmarks = None
        if with_bookmarks:
            sql = 'SELECT entity_id FROM web.user_bookmarks WHERE user_id = %(user_id)s;'
            g.execute(sql, {'user_id': user_id})
            bookmarks = [row.entity_id for row in g.cursor.fetchall()]
        g.execute(User.sql + ' WHERE u.id = %(id)s;', {'id': user_id})
        if not g.cursor.rowcount:
            return None  # pragma no cover - something went wrong, e.g. obsolete session values
        return User(g.cursor.fetchone(), bookmarks)

    @staticmethod
    def get_by_reset_code(code: str) -> Optional[User]:
        g.execute(User.sql + ' WHERE u.password_reset_code = %(code)s;', {'code': code})
        return User(g.cursor.fetchone()) if g.cursor.rowcount == 1 else None

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        g.execute(User.sql + ' WHERE LOWER(u.email) = LOWER(%(email)s);', {'email': email})
        return User(g.cursor.fetchone()) if g.cursor.rowcount == 1 else None

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        sql = User.sql + ' WHERE LOWER(u.username) = LOWER(%(username)s);'
        g.execute(sql, {'username': username})
        return User(g.cursor.fetchone()) if g.cursor.rowcount == 1 else None

    @staticmethod
    def get_by_unsubscribe_code(code: str) -> Optional[User]:
        g.execute(User.sql + ' WHERE u.unsubscribe_code = %(code)s;', {'code': code})
        return User(g.cursor.fetchone()) if g.cursor.rowcount == 1 else None

    @staticmethod
    def get_activities(limit: Union[int, str], user_id: Union[int, str],
                       action: str) -> List[NamedTupleCursor.Record]:
        sql = """
            SELECT id, user_id, entity_id, created, action, 'ignore' AS ignore
            FROM web.user_log WHERE TRUE"""
        sql += ' AND user_id = %(user_id)s' if int(user_id) else ''
        sql += ' AND action = %(action)s' if action != 'all' else ''
        sql += ' ORDER BY created DESC'  # Order is important because of limit filter
        sql += ' LIMIT %(limit)s' if int(limit) else ''
        g.execute(sql, {'limit': limit, 'user_id': user_id, 'action': action})
        return g.cursor.fetchall()

    @staticmethod
    def get_created_entities_count(user_id: int) -> int:
        sql = "SELECT COUNT(*) FROM web.user_log WHERE user_id = %(user_id)s AND action = 'insert';"
        g.execute(sql, {'user_id': user_id})
        return g.cursor.fetchone()[0]

    @staticmethod
    def insert(form: FlaskForm) -> int:
        sql = """
            INSERT INTO web.user (username, real_name, info, email, active, password, group_id)
            VALUES (%(username)s, %(real_name)s, %(info)s, %(email)s, %(active)s, %(password)s,
                (SELECT id FROM web.group WHERE name LIKE %(group_name)s))
            RETURNING id;"""
        password = bcrypt.hashpw(form.password.data.encode('utf-8'),
                                 bcrypt.gensalt()).decode('utf-8')
        g.execute(sql, {'username': form.username.data,
                        'real_name': form.real_name.data,
                        'info': form.description.data,
                        'email': form.email.data,
                        'active': form.active.data,
                        'group_name': form.group.data,
                        'password': password})
        return g.cursor.fetchone()[0]

    @staticmethod
    def delete(id_: int) -> None:
        user = User.get_by_id(id_)
        if not is_authorized('manager') or user.id == current_user.id or (
                (user.group == 'admin' and not is_authorized('admin'))):
            abort(403)  # pragma: no cover
        sql = 'DELETE FROM web."user" WHERE id = %(user_id)s;'
        g.execute(sql, {'user_id': id_})

    @staticmethod
    def get_users() -> List[Tuple[int, str]]:
        g.execute('SELECT id, username FROM web.user ORDER BY username;')
        return [(row.id, row.username) for row in g.cursor.fetchall()]

    @staticmethod
    def toggle_bookmark(entity_id: int) -> str:
        sql = """
            INSERT INTO web.user_bookmarks (user_id, entity_id)
            VALUES (%(user_id)s, %(entity_id)s);"""
        label = _('bookmark remove')
        if int(entity_id) in current_user.bookmarks:
            sql = """
                DELETE FROM web.user_bookmarks
                WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s;"""
            label = _('bookmark')
        g.execute(sql, {'user_id': current_user.id, 'entity_id': entity_id})
        return label

    @staticmethod
    def get_settings(user_id: int) -> Dict[str, Any]:
        # Set defaults
        settings = {'layout': 'default',
                    'language': session['language'],
                    'newsletter': False,
                    'table_show_aliases': True,
                    'show_email': False}
        for setting in session['settings']:
            if setting in ['map_zoom_max', 'map_zoom_default', 'table_rows'] or \
                    setting.startswith('module_'):
                settings[setting] = session['settings'][setting]

        sql = 'SELECT "name", value FROM web.user_settings WHERE user_id = %(user_id)s;'
        g.execute(sql, {'user_id': user_id})
        for row in g.cursor.fetchall():
            settings[row.name] = row.value
            if row.name in ['table_rows']:
                settings[row.name] = int(row.value)
        return settings

    @staticmethod
    def generate_password(length: Optional[int] = None) -> str:  # pragma no cover - only for mail
        length = length if length else session['settings']['random_password_length']
        return ''.join(
            secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def insert_note(entity: Entity, note: str) -> None:
        from openatlas.util.util import sanitize
        sql = """
            INSERT INTO web.user_notes (user_id, entity_id, text)
            VALUES (%(user_id)s, %(entity_id)s, %(text)s);"""
        g.execute(sql, {'user_id': current_user.id,
                        'entity_id': entity.id,
                        'text': sanitize(note, 'text')})

    @staticmethod
    def update_note(entity: Entity, note: str) -> None:
        from openatlas.util.util import sanitize
        sql = """
            UPDATE web.user_notes SET text = %(text)s
            WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s;"""
        g.execute(sql, {'user_id': current_user.id,
                        'entity_id': entity.id,
                        'text': sanitize(note, 'text')})

    @staticmethod
    def get_note(entity: Entity) -> Optional[str]:
        if not current_user.settings['module_notes']:  # pragma no cover
            return None
        sql = """
            SELECT text FROM web.user_notes
            WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s;"""
        g.execute(sql, {'user_id': current_user.id, 'entity_id': entity.id})
        return g.cursor.fetchone()[0] if g.cursor.rowcount == 1 else None

    @staticmethod
    def get_notes() -> Dict[int, str]:
        if not current_user.settings['module_notes']:  # pragma no cover
            return {}
        sql = "SELECT entity_id, text FROM web.user_notes WHERE user_id = %(user_id)s;"
        g.execute(sql, {'user_id': current_user.id})
        return {row.entity_id: row.text for row in g.cursor.fetchall()}

    @staticmethod
    def delete_note(entity_id: int) -> None:
        sql = "DELETE FROM web.user_notes WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s"
        g.execute(sql, {'user_id': current_user.id, 'entity_id': entity_id})
