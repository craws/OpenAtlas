from datetime import datetime, timedelta
from typing import Any

from flask_jwt_extended import create_access_token, decode_token
from flask_login import current_user

from openatlas.database import token as db
from openatlas.models.user import User


class Token:

    @staticmethod
    def generate_token(expiration: int, token_name: str, user_: User) -> str:
        access_token = create_access_token(
            identity=user_.username,
            additional_claims={'role': user_.group},
            expires_delta=timedelta(days=expiration) if expiration else False)
        decoded_token = decode_token(access_token, allow_expired=True)
        valid_until = datetime.max
        if expire := decoded_token.get('exp'):
            valid_until = datetime.fromtimestamp(expire)
        db.generate_token({
            'jti': decoded_token['jti'],
            'user_id': user_.id,
            'creator_id': current_user.id,
            'name': token_name,
            'valid_until': valid_until,
            'valid_from': datetime.fromtimestamp(decoded_token['iat'])})
        return access_token

    @staticmethod
    def get_tokens(
            user_id: int,
            revoked: str,
            valid: str) -> list[dict[str, Any]]:
        return db.get_tokens(user_id, revoked, valid)

    @staticmethod
    def revoke_jwt_token(id_: int) -> None:
        return db.revoke_jwt_token(id_)

    @staticmethod
    def authorize_jwt_token(id_: int) -> None:
        return db.authorize_jwt_token(id_)

    @staticmethod
    def delete_token(id_: int) -> None:
        return db.delete_token(id_)

    @staticmethod
    def delete_all_revoked_tokens() -> None:
        return db.delete_all_revoked_tokens()

    @staticmethod
    def revoke_all_tokens() -> None:
        return db.revoke_all_tokens()

    @staticmethod
    def authorize_all_tokens() -> None:
        return db.authorize_all_tokens()

    @staticmethod
    def delete_invalid_tokens() -> None:
        return db.delete_invalid_tokens([user.id for user in User.get_all() if not user.active])

    @staticmethod
    def is_valid(token: dict[str, Any], user: User) -> bool:
        if token['revoked'] or token['valid_until'] < datetime.now():
            return False
        if not user.get_by_id(token['user_id']).active:
            return False
        return True
