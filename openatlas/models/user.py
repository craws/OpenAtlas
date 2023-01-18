from __future__ import annotations

import datetime
import secrets
import string
from typing import Any, Optional

from flask import g, session
from flask_login import UserMixin, current_user

from openatlas.database.user import User as Db
from openatlas.models.entity import Entity
from openatlas.display.util import sanitize


class User(UserMixin):

    def __init__(
            self,
            row: dict[str, Any],
            bookmarks: Optional[list[int]] = None) -> None:
        self.id = row['id']
        self.active = row['active'] == 1
        self.username = row['username']
        self.password = row['password']
        self.login_last_success = row['login_last_success']
        self.login_last_failure = row['login_last_failure']
        self.login_failed_count = row['login_failed_count']
        self.real_name = row['real_name']
        self.email = row['email']
        self.description = row['info']
        self.settings = User.get_settings(row['id'])
        self.bookmarks = bookmarks
        self.password_reset_code = row['password_reset_code']
        self.password_reset_date = row['password_reset_date']
        self.unsubscribe_code = row['unsubscribe_code']
        self.group = row['group_name']
        self.created = row['created']
        self.modified = row['modified']

    def update(self) -> None:
        Db.update({
            'id': self.id,
            'username': self.username.strip(),
            'real_name': self.real_name.strip(),
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

    def update_settings(self, settings: dict[str, Any]) -> None:
        for name, value in settings.items():
            Db.update_settings(self.id, name, value)

    def remove_newsletter(self) -> None:
        Db.remove_newsletter(self.id)

    def update_language(self) -> None:
        Db.update_language(self.id, current_user.settings['language'])

    def login_attempts_exceeded(self) -> bool:
        if not self.login_last_failure \
                or self.login_failed_count < \
                int(g.settings['failed_login_tries']):
            return False
        unlocked = self.login_last_failure + datetime.timedelta(
            minutes=int(g.settings['failed_login_forget_minutes']))
        return bool(unlocked > datetime.datetime.now())

    def get_notes_by_entity_id(self, entity_id: int) -> list[dict[str, Any]]:
        return Db.get_notes_by_entity_id(self.id, entity_id)

    def get_entities(self) -> list[Entity]:
        return Entity.get_by_ids(Db.get_user_entities(self.id), types=True)

    @staticmethod
    def get_all() -> list[User]:
        return [User(row) for row in Db.get_all()]

    @staticmethod
    def get_by_id(user_id: int, bookmarks: bool = False) -> Optional[User]:
        if user_data := Db.get_by_id(user_id):
            return User(
                user_data,
                Db.get_bookmarks(user_id) if bookmarks else None)
        return None  # e.g. obsolete session values

    @staticmethod
    def get_by_reset_code(code: str) -> Optional[User]:
        user_data = Db.get_by_reset_code(code)
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        user_data = Db.get_by_email(email)
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        user_data = Db.get_by_username(username)
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_unsubscribe_code(code: str) -> Optional[User]:
        user_data = Db.get_by_unsubscribe_code(code)
        return User(user_data) if user_data else None

    @staticmethod
    def get_activities(
            limit: int,
            user_id: int,
            action: str) -> list[dict[str, Any]]:
        return Db.get_activities(limit, user_id, action)

    @staticmethod
    def get_created_entities_count(user_id: int) -> int:
        return Db.get_created_entities_count(user_id)

    @staticmethod
    def insert(data: dict[str, Any]) -> int:
        return Db.insert(data)

    @staticmethod
    def delete(id_: int) -> None:
        Db.delete(id_)

    @staticmethod
    def get_users_for_form() -> list[tuple[int, str]]:
        return Db.get_users_for_form()

    @staticmethod
    def toggle_bookmark(entity_id: int) -> str:
        if int(entity_id) in current_user.bookmarks:
            Db.delete_bookmark(current_user.id, entity_id)
            return 'bookmark'
        Db.insert_bookmark(current_user.id, entity_id)
        return 'bookmark remove'

    @staticmethod
    def get_settings(user_id: int) -> dict[str, Any]:
        settings = {
            'layout': 'default',
            'language': session['language'],
            'newsletter': False,
            'table_show_aliases': True,
            'table_show_icons': False,
            'show_email': False}
        for setting in g.settings:
            if setting in \
                    ['map_zoom_max', 'map_zoom_default', 'table_rows'] \
                    or setting.startswith('module_'):
                settings[setting] = g.settings[setting]
        for row in Db.get_settings(user_id):
            settings[row['name']] = row['value']
            if row['name'] in ['table_rows']:
                settings[row['name']] = int(row['value'])
        return settings

    @staticmethod
    def generate_password(
            length: Optional[int] = None) -> str:
        length = length or g.settings['random_password_length']
        return ''.join(
            secrets.choice(
                string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def insert_note(
            entity_id: int,
            user_id: int,
            note: str,
            public: bool) -> id:
        return Db.insert_note(
            user_id,
            entity_id,
            sanitize(note, 'text'),
            public)

    @staticmethod
    def update_note(id_: int, note: str, public: bool) -> None:
        Db.update_note(id_, sanitize(note, 'text'), public)

    @staticmethod
    def get_note_by_id(id_: int) -> dict[str, Any]:
        return Db.get_note_by_id(id_)

    @staticmethod
    def get_notes_by_user_id(user_id: int) -> list[dict[str, Any]]:
        return Db.get_notes_by_user_id(user_id)

    @staticmethod
    def delete_note(id_: int) -> None:
        Db.delete_note(id_)
