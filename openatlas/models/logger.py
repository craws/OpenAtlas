# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g, request, session
from flask_login import current_user

from openatlas import app
from openatlas.models.user import UserMapper


class DBHandler:

    @staticmethod
    def log(priority, type_, message, info=None):
        log_levels = app.config['LOG_LEVELS']
        priority = list(log_levels.keys())[list(log_levels.values()).index(priority)]
        if int(session['settings']['log_level']) < priority:
            return
        info = 'path: {path}, method: {method}, agent: {agent}{info}'.format(
            path=request.path,
            method=request.method,
            agent=request.headers.get('User-Agent'),
            info='\n' + str(info) if info else '')
        sql = """
            INSERT INTO web.system_log (priority, type, message, user_id, ip, info)
            VALUES(%(priority)s, %(type)s, %(message)s, %(user_id)s, %(ip)s, %(info)s)
            RETURNING id;"""
        params = {
            'priority': priority,
            'type': type_,
            'message': message,
            'user_id': current_user.id if hasattr(current_user, 'id') else None,
            'ip': request.remote_addr,
            'info': info}
        g.cursor.execute(sql, params)

    @staticmethod
    def get_system_logs(limit, priority, user_id):
        sql = """
            SELECT id, priority, type, message, user_id, ip, info, created
            FROM web.system_log
            WHERE priority <= %(priority)s"""
        sql += ' AND user_id = %(user_id)s' if int(user_id) > 0 else ''
        sql += ' ORDER BY created DESC'
        sql += ' LIMIT %(limit)s' if int(limit) > 0 else ''
        g.cursor.execute(sql, {'limit': limit, 'priority': priority, 'user_id': user_id})
        return g.cursor.fetchall()

    @staticmethod
    def delete_all_system_logs():
        g.cursor.execute('TRUNCATE TABLE web.system_log RESTART IDENTITY;')

    @staticmethod
    def log_user(entity_id, action):
        sql = """
            INSERT INTO web.user_log (user_id, entity_id, action)
            VALUES (%(user_id)s, %(entity_id)s, %(action)s);"""
        g.cursor.execute(
            sql, {'user_id': current_user.id, 'entity_id': entity_id, 'action': action})

    @staticmethod
    def get_log_for_advanced_view(entity_id):
        sql = """
            SELECT ul.created, ul.user_id, ul.entity_id, u.username
            FROM web.user_log ul
            JOIN web.user u ON ul.user_id = u.id
            WHERE ul.entity_id = %(entity_id)s AND ul.action = %(action)s
            ORDER BY ul.created DESC LIMIT 1;"""
        g.cursor.execute(sql, {'entity_id': entity_id, 'action': 'insert'})
        row_insert = g.cursor.fetchone()
        g.cursor.execute(sql, {'entity_id': entity_id, 'action': 'update'})
        row_update = g.cursor.fetchone()
        log = {
            'creator': UserMapper.get_by_id(row_insert.user_id) if row_insert else None,
            'created': row_insert.created if row_insert else None,
            'modifier': UserMapper.get_by_id(row_update.user_id) if row_update else None,
            'modified': row_update.created if row_update else None}
        return log
