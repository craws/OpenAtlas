# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import request, session, url_for, flash
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.models.content import ContentMapper
from openatlas.models.user import UserMapper
from openatlas.util.changelog import Changelog
from werkzeug.utils import redirect

from openatlas.models.entity import EntityMapper
from openatlas.util.util import (link, bookmark_toggle, uc_first, required_group, send_mail,
                                 format_date)


class FeedbackForm(Form):
    subject = SelectField(_('subject'), choices=app.config['FEEDBACK_SUBJECTS'].items())
    description = TextAreaField(_('description'), [InputRequired()])
    send = SubmitField(_('send'))


@app.route('/')
@app.route('/overview')
def index():
    tables = {
        'counts': {'name': 'overview', 'header': [], 'data': []},
        'bookmarks': {
            'name': 'bookmarks',
            'header': ['name', 'class', 'first', 'last'],
            'data': []},
        'latest': {
            'name': 'latest',
            'header': ['name', 'class', 'first', 'last', 'date', 'user'],
            'data': []}}
    if current_user.is_authenticated and hasattr(current_user, 'bookmarks'):
        for entity_id in current_user.bookmarks:
            entity = EntityMapper.get_by_id(entity_id)
            tables['bookmarks']['data'].append([
                link(entity),
                openatlas.classes[entity.class_.code].name,
                entity.first,
                entity.last,
                bookmark_toggle(entity.id, True)])
        for name, count in EntityMapper.get_overview_counts().items():
            count = count if count else 0
            tables['counts']['data'].append([
                '<a href="' + url_for(name + '_index') + '">' + uc_first(_(name)) + '</a>', count])
        for entity in EntityMapper.get_latest(8):
            tables['latest']['data'].append([
                link(entity),
                openatlas.classes[entity.class_.code].name,
                entity.first,
                entity.last,
                format_date(entity.created),
                openatlas.logger.get_log_for_advanced_view(entity.id)['creator_name']])
    intro = ContentMapper.get_translation('intro')
    return render_template('index/index.html', intro=intro, tables=tables)


@app.route('/index/setlocale/<language>')
def set_locale(language):
    session['language'] = language
    if hasattr(current_user, 'id') and current_user.id:
        current_user.settings['language'] = language
        current_user.update_settings()
    return redirect(request.referrer)


@app.route('/overview/feedback', methods=['POST', 'GET'])
@required_group('readonly')
def overview_feedback():
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


@app.route('/overview/contact')
def index_contact():
    return render_template('index/contact.html', contact=ContentMapper.get_translation('contact'))


@app.route('/overview/credits')
def index_credits():
    return render_template('index/credits.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', e=e), 403


@app.errorhandler(418)
def invalid_id(e):
    return render_template('418.html', e=e), 418


@app.route('/overview/changelog')
def index_changelog():
    return render_template('index/changelog.html', versions=Changelog.versions)


@app.route('/unsubscribe/<code>')
def index_unsubscribe(code):
    user = UserMapper.get_by_unsubscribe_code(code)
    text = _('unsubscribe link not valid')
    if user:  # pragma: no cover
        user.settings['newsletter'] = ''
        user.update()
        user.unsubscribe_code = ''
        user.update_settings()
        text = _('You have successfully unsubscribed. You can subscribe again in your Profile.')
    return render_template('index/unsubscribe.html', text=text)
