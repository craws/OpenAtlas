from typing import Dict, Optional

from flask import session
from flask_wtf import FlaskForm

from openatlas import app
from openatlas.database.content import Content as Db


def get_content() -> Dict[str, Dict[str, str]]:
    content: Dict[str, Dict[str, str]] = {}
    for name in [
            'intro',
            'legal_notice',
            'contact',
            'citation_example',
            'intro_for_frontend',
            'legal_notice_for_frontend',
            'contact_for_frontend',
            'site_name_for_frontend']:
        content[name] = {lang: '' for lang in app.config['LANGUAGES'].keys()}
    for row in Db.get_content():
        content[row['name']][row['language']] = row['text']
    return content


def get_translation(name: str, lang: Optional[str] = None) -> str:
    items = get_content()
    if name not in items:  # pragma: no cover
        return ''
    translations = items[name]
    if lang and lang in translations and translations[lang]:
        return translations[lang]  # pragma: no cover, can be used by API
    if translations[session['language']]:
        return translations[session['language']]
    return translations[session['settings']['default_language']]


def update_content(name: str, form: FlaskForm) -> None:
    for language in app.config['LANGUAGES'].keys():
        Db.update(
            name,
            language,
            form.__getattribute__(language).data.strip())
