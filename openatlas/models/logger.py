# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import request
from flask_login import current_user
import openatlas


class DBHandler:

    @staticmethod
    def log(priority, type_, message, info=None):
        # Todo: log only if priority is high enough
        log_levels = {
            0: 'emergency',
            1: 'alert',
            2: 'critical',
            3: 'error',
            4: 'warn',
            5: 'notice',
            6: 'info',
            7: 'debug'}
        info = 'path: {path}, method: {method}, agent: {agent}, info: {info}'.format(
            path=request.path,
            method=request.method,
            agent=request.headers.get('User-Agent'),
            info=info)
        sql = '''INSERT INTO log.log (priority, type, message, user_id, ip, info)
        VALUES(%(priority)s, %(type)s, %(message)s, %(user_id)s, %(ip)s, %(info)s) RETURNING id;'''
        params = {
            'priority': list(log_levels.keys())[list(log_levels.values()).index(priority)],
            'type': type_,
            'message': message,
            'user_id': current_user.id if hasattr(current_user, 'id') else None,
            'ip': request.remote_addr,
            'info': info}
        cursor = openatlas.get_cursor()
        cursor.execute(sql, params)
