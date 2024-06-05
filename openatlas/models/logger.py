from typing import Any

from flask import g, request
from flask_login import current_user

from openatlas import app
from openatlas.database import logger as db
from openatlas.models.imports import get_project_by_id
from openatlas.models.user import User

app.config['LOG_LEVELS'] = {
    0: 'emergency',
    1: 'alert',
    2: 'critical',
    3: 'error',
    4: 'warn',
    5: 'notice',
    6: 'info',
    7: 'debug'}


class Logger:
    @staticmethod
    def log(
            priority_: str,
            type_: str,
            message: str,
            info: str | Exception | None = None) -> None:
        log_levels = app.config['LOG_LEVELS']
        priority = list(log_levels)[list(log_levels.values()).index(priority_)]
        if priority >= int(g.settings['log_level']):
            db.log({
                'priority': priority,
                'type': type_,
                'message': message,
                'user_id': current_user.id
                if hasattr(current_user, 'id') else None,
                'info': f'{request.method} {request.method}\n{info}'})

    @staticmethod
    def get_system_logs(
            limit: str,
            priority: str,
            user_id: str) -> list[dict[str, Any]]:
        return db.get_system_logs(limit, priority, user_id)

    @staticmethod
    def delete_all_system_logs() -> None:
        db.delete_all_system_logs()

    @staticmethod
    def log_user(entity_id: int, action: str) -> None:
        db.log_user(entity_id, current_user.id, action)

    @staticmethod
    def get_log_info(entity_id: int) -> dict[str, Any]:
        data = db.get_log_for_advanced_view(entity_id)
        return {
            'creator': User.get_by_id(data['creator_id'])
            if data['creator_id'] else None,
            'created': data['created'],
            'modifier': User.get_by_id(data['modifier_id'])
            if data['modifier_id'] else None,
            'modified': data['modified'],
            'project': get_project_by_id(data['project_id'])
            if data['project_id'] else None,
            'importer': User.get_by_id(data['importer_id'])
            if data['importer_id'] else None,
            'origin_id': data['origin_id']}
