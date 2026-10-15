from collections.abc import Callable
from functools import wraps
from typing import Any

from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_login import current_user

from openatlas.api.api_v1.error_handlers import (
    abort_forbidden, abort_unauthorized)

ROLE_HIERARCHY = ['admin', 'manager', 'editor', 'contributor', 'readonly']


def is_authenticated() -> bool:
    if current_user.is_authenticated:
        return True
    try:
        return bool(verify_jwt_in_request(optional=True, locations='headers'))
    except Exception:
        return False


def get_authenticated_role() -> str | None:
    if current_user.is_authenticated and hasattr(current_user, 'group'):
        return str(current_user.group)
    try:
        jwt_claims = get_jwt()
        if jwt_claims and 'role' in jwt_claims:
            return str(jwt_claims['role'])
    except Exception:
        return None
    return None


def is_authorized_role(required_role: str) -> bool:
    user_role = get_authenticated_role()
    if not user_role:
        return False
    if user_role == 'admin':
        return True
    if required_role not in ROLE_HIERARCHY or user_role not in ROLE_HIERARCHY:
        return user_role == required_role
    return (ROLE_HIERARCHY.index(user_role)
            <= ROLE_HIERARCHY.index(required_role))


def require_auth(message: str = 'Authentication required.') -> None:
    if not is_authenticated():
        abort_unauthorized(message)


def require_group(
        group: str,
        message: str = 'Insufficient permissions.') -> None:
    require_auth()
    if not is_authorized_role(group):
        abort_forbidden(message)


def api_auth_required(fn: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        require_auth()
        return fn(*args, **kwargs)
    return wrapper


def api_group_required(
        group: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            require_group(group)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
