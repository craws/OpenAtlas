from typing import Any, Dict, Union

from flask import g, request, session
from flask_login import current_user
from psycopg2.extras import NamedTupleCursor

from openatlas import app
from openatlas.models.imports import Import


class Logger:

    @staticmethod
    def log(priority_: str, type_: str, message: str,
            info: Union[str, Exception, None] = None) -> None:
        log_levels = app.config['LOG_LEVELS']
        priority = list(log_levels.keys())[list(log_levels.values()).index(priority_)]
        if int(session['settings']['log_level']) < priority:
            return
        info = '{method} {path}{info}'.format(path=request.path,
                                              method=request.method,
                                              info='\n' + str(info) if info else '')
        sql = """
            INSERT INTO web.system_log (priority, type, message, user_id, info)
            VALUES(%(priority)s, %(type)s, %(message)s, %(user_id)s, %(info)s)
            RETURNING id;"""
        params = {'priority': priority,
                  'type': type_,
                  'message': message,
                  'user_id': current_user.id if hasattr(current_user, 'id') else None,
                  'info': info}
        g.execute(sql, params)

    @staticmethod
    def get_system_logs(limit: str, priority: str, user_id: str) -> NamedTupleCursor.Record:
        sql = """
            SELECT id, priority, type, message, user_id, info, created FROM web.system_log
            WHERE priority <= %(priority)s"""
        sql += ' AND user_id = %(user_id)s' if int(user_id) > 0 else ''
        sql += ' ORDER BY created DESC'
        sql += ' LIMIT %(limit)s' if int(limit) > 0 else ''
        g.execute(sql, {'limit': limit, 'priority': priority, 'user_id': user_id})
        return g.cursor.fetchall()

    @staticmethod
    def delete_all_system_logs() -> None:
        g.execute('TRUNCATE TABLE web.system_log RESTART IDENTITY;')

    @staticmethod
    def log_user(entity_id: int, action: str) -> None:
        sql = """
            INSERT INTO web.user_log (user_id, entity_id, action)
            VALUES (%(user_id)s, %(entity_id)s, %(action)s);"""
        g.execute(sql, {'user_id': current_user.id, 'entity_id': entity_id, 'action': action})

    @staticmethod
    def get_log_for_advanced_view(entity_id: str) -> Dict[str, Any]:
        from openatlas.models.user import User
        sql = """
            SELECT ul.created, ul.user_id, ul.entity_id, u.username
            FROM web.user_log ul
            JOIN web.user u ON ul.user_id = u.id
            WHERE ul.entity_id = %(entity_id)s AND ul.action = %(action)s
            ORDER BY ul.created DESC LIMIT 1;"""
        g.execute(sql, {'entity_id': entity_id, 'action': 'insert'})
        row_insert = g.cursor.fetchone()
        g.execute(sql, {'entity_id': entity_id, 'action': 'update'})
        row_update = g.cursor.fetchone()
        sql = 'SELECT project_id, origin_id, user_id FROM import.entity WHERE entity_id = %(id)s;'
        g.execute(sql, {'id': entity_id})
        row_import = g.cursor.fetchone()
        project = Import.get_project_by_id(row_import.project_id) if row_import else None
        log = {'creator': User.get_by_id(row_insert.user_id) if row_insert else None,
               'created': row_insert.created if row_insert else None,
               'modifier': User.get_by_id(row_update.user_id) if row_update else None,
               'modified': row_update.created if row_update else None,
               'import_project': project,
               'import_user': User.get_by_id(row_import.user_id) if row_import else None,
               'import_origin_id': row_import.origin_id if row_import else None}
        return log
