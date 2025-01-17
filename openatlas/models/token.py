from datetime import datetime, timedelta
from typing import Any

from flask_jwt_extended import create_access_token, decode_token
from flask_login import current_user

from openatlas.database import token as db
from openatlas.models.user import User


class Token:

    @staticmethod
    def generate_token(expiration: str, token_name: str, user_id: int) -> None:
        expires_delta = None
        match expiration:
            case '0':
                expires_delta = timedelta(days=1)
            case '1':
                expires_delta = timedelta(days=90)
        user_ = User.get_by_id(user_id)
        access_token = create_access_token(
            identity=user_.username,
            additional_claims={'role': user_.group},
            expires_delta=expires_delta)  # type: ignore
        decoded_token = decode_token(access_token, allow_expired=True)
        valid_until = datetime.max
        if expire := decoded_token.get('exp'):
            valid_until = datetime.fromtimestamp(expire)
        db.generate_token({
            'jti': decoded_token['jti'],
            'user_id': user_id,
            'creator_id': current_user,
            'name': token_name,
            'valid_until': valid_until,
            'valid_from': datetime.fromtimestamp(decoded_token['iat'])})
        return access_token

    @staticmethod
    def get_tokens(user_id: int) -> list[dict[str, Any]]:
        return db.get_tokens(user_id)

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
