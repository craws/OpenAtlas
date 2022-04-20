from typing import Any, Union

from flask import g, request
from flask_login import current_user

from openatlas import app
from openatlas.database.logger import Logger as Db


class Logger:

    @staticmethod
    def log(
            priority_: str,
            type_: str,
            message: str,
            info: Union[str, Exception, None] = None) -> None:
        log_levels = app.config['LOG_LEVELS']
        priority = list(log_levels)[list(log_levels.values()).index(priority_)]
        if int(g.settings['log_level']) < priority:
            return  # pragma: no cover
        Db.log({
            'priority': priority,
            'type': type_,
            'message': message,
            'user_id': current_user.id if hasattr(current_user, 'id') else None,
            'info': '{method} {path}{info}'.format(
                path=request.path,
                method=request.method,
                info=f'\n{info}' if info else '')})

    @staticmethod
    def get_system_logs(
            limit: str,
            priority: str,
            user_id: str) -> list[dict[str, Any]]:
        return Db.get_system_logs(limit, priority, user_id)

    @staticmethod
    def delete_all_system_logs() -> None:
        Db.delete_all_system_logs()

    @staticmethod
    def log_user(entity_id: int, action: str) -> None:
        Db.log_user(entity_id, current_user.id, action)

    @staticmethod
    def get_log_info(entity_id: str) -> dict[str, Any]:
        from openatlas.models.user import User
        from openatlas.models.imports import Import
        data = Db.get_log_for_advanced_view(entity_id)
        return {
            'creator': User.get_by_id(data['creator_id'])
            if data['creator_id'] else None,
            'created': data['created'],
            'modifier': User.get_by_id(data['modifier_id'])
            if data['modifier_id'] else None,
            'modified': data['modified'],
            'project': Import.get_project_by_id(data['project_id'])
            if data['project_id'] else None,
            'importer': User.get_by_id(data['importer_id'])
            if data['importer_id'] else None,
            'origin_id': data['origin_id']}
