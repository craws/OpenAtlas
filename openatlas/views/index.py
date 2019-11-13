# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Tuple, Union

from flask import flash, g, render_template, request, session, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.models.content import ContentMapper
from openatlas.models.entity import EntityMapper
from openatlas.models.user import UserMapper
from openatlas.util.changelog import Changelog
from openatlas.util.table import Table
from openatlas.util.util import (bookmark_toggle, format_date, link, required_group, send_mail,
                                 truncate_string, uc_first)


class FeedbackForm(FlaskForm):
    subject = SelectField(_('subject'),
                          choices=list(app.config['FEEDBACK_SUBJECTS'].items()),
                          render_kw={'autofocus': True})
    description = TextAreaField(_('description'), [InputRequired()])
    send = SubmitField(_('send'))


@app.route('/')
@app.route('/overview')
def index() -> str:
    tables = {'overview': Table(paging=False, defs='[{className: "dt-body-right", targets: 1}]'),
              'bookmarks': Table(['name', 'class', 'first', 'last'],
                                 defs='[{className: "dt-body-right", targets: [2,3]}]'),
              'notes': Table(['name', 'class', 'first', 'last', _('note')],
                             defs='[{className: "dt-body-right", targets: [2,3]}]'),
              'latest': Table(['name', 'class', 'first', 'last', 'date', 'user'],
                              order='[[4, "desc"]]',
                              defs='[{className: "dt-body-right", targets: [2,3]}]')}
    if current_user.is_authenticated and hasattr(current_user, 'bookmarks'):
        for entity_id in current_user.bookmarks:
            entity = EntityMapper.get_by_id(entity_id)
            tables['bookmarks'].rows.append([link(entity), g.classes[entity.class_.code].name,
                                             entity.first, entity.last,
                                             bookmark_toggle(entity.id, True)])
        for entity_id, text in UserMapper.get_notes().items():
            entity = EntityMapper.get_by_id(entity_id)
            tables['notes'].rows.append([link(entity), g.classes[entity.class_.code].name,
                                        entity.first, entity.last, truncate_string(text)])
        for name, count in EntityMapper.get_overview_counts().items():
            if count:
                count = format_number(count) if count else ''
                url = url_for(name + '_index') if name != 'find' else url_for('place_index')
                tables['overview'].rows.append([
                    '<a href="' + url + '">' + uc_first(_(name)) + '</a>', count])
        for entity in EntityMapper.get_latest(8):
            tables['latest'].rows.append([
                link(entity), g.classes[entity.class_.code].name,
                entity.first, entity.last, format_date(entity.created),
                link(logger.get_log_for_advanced_view(entity.id)['creator'])])
    intro = ContentMapper.get_translation('intro')
    return render_template('index/index.html', intro=intro, tables=tables)


@app.route('/index/setlocale/<language>')
def set_locale(language: str) -> Response:
    session['language'] = language
    if hasattr(current_user, 'id') and current_user.id:
        current_user.settings['language'] = language
        current_user.update_settings()
    return redirect(request.referrer)


@app.route('/overview/feedback', methods=['POST', 'GET'])
@required_group('readonly')
def index_feedback() -> Union[str, Response]:
    form = FeedbackForm()
    if form.validate_on_submit() and session['settings']['mail']:  # pragma: no cover
        subject = form.subject.data + ' from ' + session['settings']['site_name']
        user = current_user
        body = form.subject.data + ' from ' + user.username + ' (' + str(user.id) + ') '
        body += user.email + ' at ' + request.headers['Host'] + "\n\n" + form.description.data
        if send_mail(subject, body, session['settings']['mail_recipients_feedback']):
            flash(_('info feedback thanks'), 'info')
        else:
            flash(_('error mail send'), 'error')
        return redirect(url_for('index'))
    return render_template('index/feedback.html', form=form)


@app.route('/overview/content/<item>')
def index_content(item: str) -> str:
    return render_template('index/content.html', text=ContentMapper.get_translation(item),
                           title=item)


@app.route('/overview/credits')
def index_credits() -> str:
    return render_template('index/credits.html')


@app.errorhandler(403)
def forbidden(e) -> Tuple[str, int]:
    return render_template('403.html', e=e), 403


@app.errorhandler(404)
def page_not_found(e) -> Tuple[str, int]:
    return render_template('404.html', e=e), 404


@app.errorhandler(418)
def invalid_id(e) -> Tuple[str, int]:
    return render_template('418.html', e=e), 418


@app.errorhandler(422)
def unprocessable_entity(e) -> Tuple[str, int]:
    return render_template('422.html', e=e), 422


@app.route('/overview/changelog')
def index_changelog() -> str:
    return render_template('index/changelog.html', versions=Changelog.versions)


@app.route('/unsubscribe/<code>')
def index_unsubscribe(code: str) -> str:
    user = UserMapper.get_by_unsubscribe_code(code)
    text = _('unsubscribe link not valid')
    if user:  # pragma: no cover
        user.settings['newsletter'] = ''
        user.update()
        user.unsubscribe_code = ''
        user.update_settings()
        text = _('You have successfully unsubscribed. You can subscribe again in your Profile.')
    return render_template('index/unsubscribe.html', text=text)
