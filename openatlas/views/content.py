# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Union

from flask import flash, render_template, session, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import TextAreaField

from openatlas import app
from openatlas.models.content import ContentMapper
from openatlas.util import util
from openatlas.util.table import Table
from openatlas.util.util import required_group


class ContentForm(FlaskForm):
    pass


@app.route('/admin/content')
@required_group('manager')
def content_index() -> str:
    table = Table(['name'] + [language for language in app.config['LANGUAGES'].keys()] + ['text'])
    for item, languages in ContentMapper.get_content().items():
        url = url_for('content_view', item=item)
        content = ['<a href="' + url + '">' + util.uc_first(_(item)) + '</a>']
        html_ok = '<img src="/static/images/icons/dialog-apply.png" alt="ok">'
        for language in app.config['LANGUAGES'].keys():
            content.append(html_ok if languages[language] else '')
        content.append(languages[session['language']])
        table.rows.append(content)
    return render_template('content/index.html', table=table)


@app.route('/admin/content/view/<string:item>')
@required_group('manager')
def content_view(item) -> str:
    return render_template('content/view.html', item=item, content=ContentMapper.get_content())


@app.route('/admin/content/update/<string:item>', methods=["GET", "POST"])
@required_group('manager')
def content_update(item: str) -> Union[str, Response]:
    languages = app.config['LANGUAGES'].keys()
    for language in languages:
        setattr(ContentForm, language, TextAreaField())
    form = ContentForm()
    if form.validate_on_submit():
        ContentMapper.update_content(item, form)
        flash(_('info update'), 'info')
        return redirect(url_for('content_view', item=item))
    content = ContentMapper.get_content()
    for language in languages:
        form.__getattribute__(language).data = content[item][language]
    return render_template('content/update.html', item=item, form=form, languages=languages)
