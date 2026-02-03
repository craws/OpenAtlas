from flask import g
from psycopg2 import connect
from psycopg2.extensions import connection


def open_connection(config: dict[str, object]) -> connection:
    return connect(
        database=config['DATABASE_NAME'],
        user=config['DATABASE_USER'],
        password=config['DATABASE_PASS'],
        port=config['DATABASE_PORT'],
        host=config['DATABASE_HOST'])


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
