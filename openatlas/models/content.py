from flask import g, session

from openatlas import app
from openatlas.database import content as db


def get_content() -> dict[str, dict[str, str]]:
    content: dict[str, dict[str, str]] = {}
    for name in ['intro', 'legal_notice', 'contact', 'citation_example']:
        content[name] = {lang: '' for lang in app.config['LANGUAGES']}
    for row in db.get_content():
        content[row['name']][row['language']] = row['text']
    return content


def get_translation(name: str) -> str:
    translations = get_content()[name]
    if translations[session['language']]:
        return translations[session['language']]
    return translations[g.settings['default_language']]


def update_content(data: list[dict[str, str]]) -> None:
    for item in data:
        db.update(item['name'], item['language'], item['text'])
