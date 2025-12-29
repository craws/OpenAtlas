from datetime import datetime
from typing import Any

from flask import g


def get_tokens(
        user_id: int,
        revoked: str,
        valid: str) -> list[dict[str, Any]]:
    g.cursor.execute(
        f"""
        SELECT 
            id, user_id, jti, valid_from, valid_until, name, created, revoked,
            creator_id
        FROM web.user_tokens 
        WHERE TRUE
            {'AND user_id = %(user_id)s' if int(user_id) else ''}
            {'AND revoked = %(revoked)s' if revoked != 'all' else ''}
            {'AND valid_until ' + valid + ' timestamp %(timestamp)s'
            if valid != 'all' else ''};
        """, {
            'user_id': user_id,
            'revoked': revoked,
            'timestamp': str(datetime.now())})
    return [dict(row) for row in g.cursor.fetchall()]


def generate_token(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.user_tokens(user_id, jti, valid_from, valid_until, 
        name, creator_id)
            VALUES (%(user_id)s, %(jti)s, %(valid_from)s, %(valid_until)s, 
            %(name)s, %(creator_id)s);
        """, data)


def revoke_jwt_token(id_: int) -> None:
    g.cursor.execute(
        "UPDATE web.user_tokens SET revoked=true WHERE id = %(id)s;",
        {'id': id_})


def authorize_jwt_token(id_: int) -> None:
    g.cursor.execute(
        "UPDATE web.user_tokens SET revoked=false WHERE id = %(id)s;",
        {'id': id_})


def delete_token(id_: int) -> None:
    g.cursor.execute(
        "DELETE FROM web.user_tokens WHERE id = %(id)s;",
        {'id': id_})


def delete_all_revoked_tokens() -> None:
    g.cursor.execute("DELETE FROM web.user_tokens WHERE revoked = true;")


def authorize_all_tokens() -> None:
    g.cursor.execute("UPDATE web.user_tokens SET revoked=false;")


def revoke_all_tokens() -> None:
    g.cursor.execute("UPDATE web.user_tokens SET revoked=true;")


def delete_invalid_tokens(inactive_user_ids: list[int]) -> None:
    g.cursor.execute(
        """
        DELETE FROM web.user_tokens
        WHERE revoked = true
            OR valid_until < %(now)s
            OR user_id IN %(user_ids)s;
        """,
        {'now': str(datetime.now()), 'user_ids': tuple(inactive_user_ids)})


def check_token_revoked(jti: str) -> dict[str, Any]:
    g.cursor.execute(
        """
        SELECT t.revoked, t.valid_until, u.active
        FROM web.user_tokens t 
        LEFT JOIN web.user u ON t.user_id = u.id
        WHERE jti = %(jti)s;
        """,
        {'jti': jti})
    token = {'revoked': True, 'valid_until': True, 'active': True}
    if row := g.cursor.fetchone():
        token = {'revoked': row[0], 'valid_until': row[1], 'active': row[2]}
    return token
