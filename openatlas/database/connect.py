from typing import Any, Dict

import psycopg2
import psycopg2.extras
from flask import g


def initialize_database(config: Dict[str, Any]) -> None:
    try:
        g.db = psycopg2.connect(
            database=config['DATABASE_NAME'],
            user=config['DATABASE_USER'],
            password=config['DATABASE_PASS'],
            port=config['DATABASE_PORT'],
            host=config['DATABASE_HOST'])
        g.db.autocommit = True
    except Exception as e:  # pragma: no cover
        print("Database connection failed")
        raise Exception(e)
    g.cursor = g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def close_connection() -> None:
    if hasattr(g, 'db'):
        g.db.close()
