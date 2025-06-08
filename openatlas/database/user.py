from typing import Any

from flask import g

SQL = """
    SELECT
        u.id,
        u.username,
        u.password,
        u.active,
        u.real_name,
        u.info,
        u.email, u.unsubscribe_code,        
        u.created, u.modified,        
        u.password_reset_code, u.password_reset_date ,
        u.login_last_success, u.login_last_failure, u.login_failed_count,
        r.name AS group_name
    FROM web.user u
    LEFT JOIN web.group r ON u.group_id = r.id """


def update(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE web.user
        SET (
            username, password, real_name, info, email, active,
            login_last_success, login_last_failure, login_failed_count,
            group_id, password_reset_code, password_reset_date,
            unsubscribe_code
        ) = (
            %(username)s, %(password)s, %(real_name)s, %(info)s, %(email)s,
            %(active)s, %(login_last_success)s, %(login_last_failure)s,
            %(login_failed_count)s,
            (SELECT id FROM web.group WHERE name LIKE %(group_name)s),
            %(password_reset_code)s, %(password_reset_date)s,
            %(unsubscribe_code)s
        ) WHERE id = %(id)s;
        """,
        data)


def update_settings(user_id: int, name: str, value: int | str) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.user_settings (user_id, "name", "value")
        VALUES (%(user_id)s, %(name)s, %(value)s)
        ON CONFLICT (user_id, name) DO UPDATE SET "value" = %(value)s;
        """,
        {'user_id': user_id, 'name': name, 'value': value})


def remove_newsletter(user_id: int) -> None:
    g.cursor.execute(
        """
        DELETE FROM web.user_settings
        WHERE name = 'newsletter' AND user_id = %(user_id)s;
        """,
        {'user_id': user_id})


def update_language(user_id: int, value: str) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.user_settings (user_id, "name", "value")
        VALUES (%(user_id)s, 'language', %(value)s)
        ON CONFLICT (user_id, name) DO UPDATE SET "value" = %(value)s;
        """,
        {'user_id': user_id, 'value': value})


def get_all() -> list[dict[str, Any]]:
    g.cursor.execute(f'{SQL} ORDER BY username;')
    return list(g.cursor)


def get_bookmarks(user_id: int) -> list[int]:
    g.cursor.execute(
        """
        SELECT entity_id
        FROM web.user_bookmarks
        WHERE user_id = %(user_id)s;
        """,
        {'user_id': user_id})
    return [row[0] for row in list(g.cursor)]


def get_by_id(user_id: int) -> dict[str, Any]:
    g.cursor.execute(f'{SQL} WHERE u.id = %(id)s;', {'id': user_id})
    return g.cursor.fetchone()


def get_by_reset_code(code: str) -> dict[str, Any]:
    g.cursor.execute(
        f'{SQL} WHERE u.password_reset_code = %(code)s;',
        {'code': code})
    return g.cursor.fetchone()


def get_by_email(email: str) -> dict[str, Any]:
    g.cursor.execute(
        f'{SQL} WHERE LOWER(u.email) = LOWER(%(email)s);',
        {'email': email})
    return g.cursor.fetchone()


def get_by_username(username: str) -> dict[str, Any]:
    g.cursor.execute(
        f'{SQL} WHERE LOWER(u.username) = LOWER(%(username)s);',
        {'username': username})
    return g.cursor.fetchone()


def get_by_unsubscribe_code(code: str) -> dict[str, Any]:
    g.cursor.execute(
        f'{SQL} WHERE u.unsubscribe_code = %(code)s;',
        {'code': code})
    return g.cursor.fetchone()


def get_activities(
        limit: int,
        user_id: int,
        action: str,
        entity_id: int | None) -> list[dict[str, Any]]:
    g.cursor.execute(
        f"""
        SELECT
            id, user_id,
            entity_id,
            created,
            action,
            'ignore' AS ignore
        FROM web.user_log
        WHERE TRUE
            {'AND user_id = %(id)s' if int(user_id) else ''}
            {'AND action = %(action)s' if action != 'all' else ''}
            {'AND entity_id = %(entity_id)s' if entity_id else ''}
        ORDER BY created DESC
        {'LIMIT %(limit)s' if int(limit) else ''};
        """, {
            'limit': limit,
            'id': user_id,
            'action': action,
            'entity_id': entity_id})
    return list(g.cursor)


def get_created_entities_count(user_id: int) -> int:
    g.cursor.execute(
        """
        SELECT COUNT(*)
        FROM web.user_log l
        JOIN model.entity e ON l.entity_id = e.id
            AND l.user_id = %(user_id)s
            AND l.action = 'insert';
        """,
        {'user_id': user_id})
    return g.cursor.fetchone()['count']


def insert(data: dict[str, Any]) -> int:
    g.cursor.execute(
        """
        INSERT INTO web.user (
            username,
            real_name,
            info,
            email,
            active,
            password,
            group_id)
        VALUES (
            %(username)s,
            %(real_name)s,
            %(info)s,
            %(email)s,
            %(active)s,
            %(password)s,
            (SELECT id FROM web.group WHERE name LIKE %(group_name)s))
        RETURNING id;
        """,
        data)
    return g.cursor.fetchone()['id']


def delete(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM web.user WHERE id = %(user_id)s;',
        {'user_id': id_})


def get_users_for_form() -> list[tuple[int, str]]:
    g.cursor.execute('SELECT id, username FROM web.user ORDER BY username;')
    return [(row['id'], row['username']) for row in list(g.cursor)]


def insert_bookmark(user_id: int, entity_id: int) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.user_bookmarks (user_id, entity_id)
        VALUES (%(user_id)s, %(entity_id)s);
        """,
        {'user_id': user_id, 'entity_id': entity_id})


def delete_bookmark(user_id: int, entity_id: int) -> None:
    g.cursor.execute(
        """
        DELETE FROM web.user_bookmarks
        WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s;
        """,
        {'user_id': user_id, 'entity_id': entity_id})


def get_settings(user_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT "name", value
        FROM web.user_settings
        WHERE user_id = %(user_id)s;
        """,
        {'user_id': user_id})
    return list(g.cursor)


def get_notes_by_entity_id(
        user_id: int,
        entity_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id, created, public, text, user_id
        FROM web.user_notes
        WHERE entity_id = %(entity_id)s
            AND (public IS TRUE or user_id = %(user_id)s);
        """,
        {'entity_id': entity_id, 'user_id': user_id})
    return list(g.cursor)


def get_notes_by_user_id(user_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id, created, public, text, user_id, entity_id
        FROM web.user_notes
        WHERE user_id = %(user_id)s;
        """,
        {'user_id': user_id})
    return list(g.cursor)


def get_note_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(
        """
        SELECT id, created, public, text, user_id, entity_id
        FROM web.user_notes
        WHERE id = %(id)s;
        """,
        {'id': id_})
    return g.cursor.fetchone()


def insert_note(
        user_id: int,
        entity_id: int,
        note: str | None,
        public: bool) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.user_notes (user_id, entity_id, text, public)
        VALUES (%(user_id)s, %(entity_id)s, %(text)s, %(public)s);
        """, {
            'user_id': user_id,
            'entity_id': entity_id,
            'text': note,
            'public': public})


def update_note(id_: int, note: str | None, public: bool) -> None:
    g.cursor.execute(
        """
        UPDATE web.user_notes
        SET text = %(text)s, public = %(public)s
        WHERE id = %(id)s;
        """,
        {'id': id_, 'text': note, 'public': public})


def delete_note(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM web.user_notes WHERE id = %(id)s;',
        {'id': id_})


def get_user_entities(id_: int) -> list[int]:
    g.cursor.execute(
        """
        SELECT e.id
        FROM web.user_log l
        JOIN model.entity e ON l.entity_id = e.id
            AND l.user_id = %(user_id)s
            AND l.action = 'insert';
        """,
        {'user_id': id_})
    return [row[0] for row in list(g.cursor)]


def admins_available() -> bool:
    g.cursor.execute(
        """
        SELECT u.id
        FROM web.user u
        LEFT JOIN web.group g ON u.group_id = g.id AND g.name = 'admin'
        WHERE u.active = true;
        """)
    return bool(g.cursor.rowcount)
