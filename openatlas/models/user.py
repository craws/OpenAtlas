from __future__ import annotations

import secrets
import string
from datetime import datetime, timedelta
from typing import Any, Optional

from flask import g, session
from flask_login import UserMixin, current_user

from openatlas.database import user as db
from openatlas.display.util2 import sanitize
from openatlas.models.entity import Entity


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
        db.update({
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

    def delete(self) -> None:
        db.delete(self.id)

    def update_settings(self, settings: dict[str, Any]) -> None:
        for name, value in settings.items():
            db.update_settings(self.id, name, value)

    def remove_newsletter(self) -> None:
        db.remove_newsletter(self.id)

    def update_language(self) -> None:
        db.update_language(self.id, current_user.settings['language'])

    def login_attempts_exceeded(self) -> bool:
        if not self.login_last_failure \
                or self.login_failed_count < \
                int(g.settings['failed_login_tries']):
            return False
        unlocked = self.login_last_failure + timedelta(
            minutes=int(g.settings['failed_login_forget_minutes']))
        return bool(unlocked > datetime.now())

    def get_notes_by_entity_id(self, entity_id: int) -> list[dict[str, Any]]:
        return db.get_notes_by_entity_id(self.id, entity_id)

    def get_entities(self) -> list[Entity]:
        return Entity.get_by_ids(db.get_user_entities(self.id), types=True)

    @staticmethod
    def get_all() -> list[User]:
        return [User(row) for row in db.get_all()]

    @staticmethod
    def get_by_id(user_id: int, bookmarks: bool = False) -> Optional[User]:
        if user_data := db.get_by_id(user_id):
            return User(
                user_data,
                db.get_bookmarks(user_id) if bookmarks else None)
        return None  # e.g. obsolete session values

    @staticmethod
    def get_by_id_without_bookmarks(user_id: int) -> User:
        return User(db.get_by_id(user_id))

    @staticmethod
    def get_by_reset_code(code: str) -> Optional[User]:
        user_data = db.get_by_reset_code(code)
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        user_data = db.get_by_email(email)
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        user_data = db.get_by_username(username)
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_unsubscribe_code(code: str) -> Optional[User]:
        user_data = db.get_by_unsubscribe_code(code)
        return User(user_data) if user_data else None

    @staticmethod
    def get_activities(
            limit: int,
            user_id: int,
            action: str,
            entity_id: int | None) -> list[dict[str, Any]]:
        return db.get_activities(limit, user_id, action, entity_id)

    @staticmethod
    def get_created_entities_count(user_id: int) -> int:
        return db.get_created_entities_count(user_id)

    @staticmethod
    def insert(data: dict[str, Any]) -> int:
        return db.insert(data)

    @staticmethod
    def get_users_for_form() -> list[tuple[int, str]]:
        return db.get_users_for_form()

    @staticmethod
    def toggle_bookmark(entity_id: int) -> str:
        if entity_id in current_user.bookmarks:
            db.delete_bookmark(current_user.id, entity_id)
            return 'bookmark'
        db.insert_bookmark(current_user.id, entity_id)
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
            if setting in [
                    'frontend_website_url',
                    'frontend_resolver_url',
                    'map_zoom_max',
                    'map_zoom_default',
                    'table_rows'] \
                    or setting.startswith('module_'):
                settings[setting] = g.settings[setting]
        for row in db.get_settings(user_id):
            settings[row['name']] = row['value']
            if row['name'] in ['table_rows']:
                settings[row['name']] = int(row['value'])
        return settings

    @staticmethod
    def generate_password(length: Optional[int] = None) -> str:
        length = length or g.settings['random_password_length']
        return ''.join(
            secrets.choice(
                string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def insert_note(
            entity_id: int,
            user_id: int,
            note: str,
            public: bool) -> None:
        db.insert_note(user_id, entity_id, sanitize(note, 'text'), public)

    @staticmethod
    def update_note(id_: int, note: str, public: bool) -> None:
        db.update_note(id_, sanitize(note, 'text'), public)

    @staticmethod
    def get_note_by_id(id_: int) -> dict[str, Any]:
        return db.get_note_by_id(id_)

    @staticmethod
    def get_notes_by_user_id(user_id: int) -> list[dict[str, Any]]:
        return db.get_notes_by_user_id(user_id)

    @staticmethod
    def delete_note(id_: int) -> None:
        db.delete_note(id_)
