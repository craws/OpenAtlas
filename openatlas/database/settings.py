from typing import Any, Optional

from flask import g
from psycopg2.extras import DictCursor


def get_settings(cursor: Optional[DictCursor] = None) -> dict[str, str]:
    cursor = cursor or g.cursor
    cursor.execute('SELECT name, value FROM web.settings;')
    return {row['name']: row['value'] for row in list(cursor)}


def update(field_name: str, value: Any) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.settings (name, value)
        VALUES (%(name)s, %(value)s)
        ON CONFLICT (name) DO UPDATE SET "value" = %(value)s;
        """,
        {'name': field_name, 'value': value})


def set_logo(file_id: int | str) -> None:
    g.cursor.execute(
        """
        UPDATE web.settings
        SET value = %(file_id)s
        WHERE name = 'logo_file_id';
        """,
        {'file_id': file_id})
