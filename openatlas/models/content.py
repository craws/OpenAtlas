from typing import Dict

from flask import flash, g, session
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm

from openatlas import app, logger


class Content:

    @staticmethod
    def get_content() -> Dict[str, Dict[str, str]]:
        content: Dict[str, Dict[str, str]] = {}
        for name in ['intro', 'legal_notice', 'contact', 'citation_example',
                     'intro_for_frontend', 'legal_notice_for_frontend', 'contact_for_frontend']:
            content[name] = {language: '' for language in app.config['LANGUAGES'].keys()}
        g.execute("SELECT name, language, text FROM web.i18n;")
        for row in g.cursor.fetchall():
            content[row.name][row.language] = row.text
        return content

    @staticmethod
    def get_translation(name: str) -> str:
        translations = Content.get_content()[name]
        if translations[session['language']]:  # pragma: no cover
            return translations[session['language']]
        return translations[session['settings']['default_language']]

    @staticmethod
    def update_content(name: str, form: FlaskForm) -> None:
        g.execute('BEGIN')
        try:
            for language in app.config['LANGUAGES'].keys():
                sql = 'DELETE FROM web.i18n WHERE name = %(name)s AND language = %(language)s'
                g.execute(sql, {'name': name, 'language': language})
                sql = """
                    INSERT INTO web.i18n (name, language, text)
                    VALUES (%(name)s, %(language)s, %(text)s);"""
                g.execute(sql, {'name': name,
                                'language': language,
                                'text': form.__getattribute__(language).data.strip()})
            g.execute('COMMIT')
        except Exception as e:  # pragma: no cover
            g.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
