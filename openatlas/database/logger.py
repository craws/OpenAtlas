from typing import Any

from flask import g


def log(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.system_log (priority, type, message, user_id, info)
        VALUES (%(priority)s, %(type)s, %(message)s, %(user_id)s, %(info)s)
        """,
        data)


def get_system_logs(
        limit: str,
        priority: str,
        user_id: str) -> list[dict[str, Any]]:
    g.cursor.execute(
        f"""
        SELECT id, priority, type, message, user_id, info, created
        FROM web.system_log
        WHERE priority <= %(priority)s
            {' AND user_id = %(user_id)s' if int(user_id) > 0 else ''}
        ORDER BY created DESC
        {' LIMIT %(limit)s' if int(limit) > 0 else ''};
        """,
        {'limit': limit, 'priority': priority, 'user_id': user_id})
    return list(g.cursor)


def delete_all_system_logs() -> None:
    g.cursor.execute('TRUNCATE TABLE web.system_log RESTART IDENTITY;')


def log_user(entity_id: int, user_id: int, action: str) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.user_log (user_id, entity_id, action)
        VALUES (%(user_id)s, %(entity_id)s, %(action)s);
        """,
        {'user_id': user_id, 'entity_id': entity_id, 'action': action})


def get_log_for_advanced_view(entity_id: int) -> dict[str, Any]:
    sql = """
        SELECT ul.created, ul.user_id, ul.entity_id, u.username
        FROM web.user_log ul
        JOIN web.user u ON ul.user_id = u.id
        WHERE ul.entity_id = %(entity_id)s AND ul.action = %(action)s
        ORDER BY ul.created
        DESC LIMIT 1;
        """
    g.cursor.execute(sql, {'entity_id': entity_id, 'action': 'insert'})
    row_insert = g.cursor.fetchone()
    g.cursor.execute(sql, {'entity_id': entity_id, 'action': 'update'})
    row_update = g.cursor.fetchone()
    g.cursor.execute(
        """
        SELECT project_id, origin_id, user_id
        FROM import.entity
        WHERE entity_id = %(id)s;
        """,
        {'id': entity_id})
    row_import = g.cursor.fetchone()
    return {
        'creator_id': row_insert['user_id'] if row_insert else None,
        'created': row_insert['created'] if row_insert else None,
        'modifier_id': row_update['user_id'] if row_update else None,
        'modified': row_update['created'] if row_update else None,
        'project_id': row_import['project_id'] if row_import else None,
        'importer_id': row_import['user_id'] if row_import else None,
        'origin_id': row_import['origin_id'] if row_import else None}
