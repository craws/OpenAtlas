from flask import g


def get_content() -> list[dict[str, str]]:
    g.cursor.execute('SELECT name, language, text FROM web.i18n;')
    return list(g.cursor)


def update(name: str, language: str, text: str) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.i18n (name, language, text)
        VALUES (%(name)s, %(language)s, %(text)s)
        ON CONFLICT (name, language) DO UPDATE SET text = %(text)s;
        """,
        {'name': name, 'language': language, 'text': text})
