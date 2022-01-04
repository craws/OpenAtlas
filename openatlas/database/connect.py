from typing import Any

from flask import g
from psycopg2 import connect, extras


def open_connection(config: dict[str, Any]) -> None:
    g.db = connect(
        database=config['DATABASE_NAME'],
        user=config['DATABASE_USER'],
        password=config['DATABASE_PASS'],
        port=config['DATABASE_PORT'],
        host=config['DATABASE_HOST'])
    g.db.autocommit = True
    g.cursor = g.db.cursor(cursor_factory=extras.DictCursor)


def close_connection() -> None:
    if hasattr(g, 'db'):
        g.db.close()


class Transaction:

    @staticmethod
    def begin() -> None:
        g.cursor.execute('BEGIN')

    @staticmethod
    def commit() -> None:
        g.cursor.execute('COMMIT')

    @staticmethod
    def rollback() -> None:
        g.cursor.execute('ROLLBACK')
