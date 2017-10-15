# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import request, session, url_for
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_login import current_user

import openatlas
from openatlas import app
from openatlas.models.content import ContentMapper
from openatlas.util.changelog import Changelog
from werkzeug.utils import redirect

from openatlas.models.entity import EntityMapper
from openatlas.util.util import link, bookmark_toggle, uc_first, required_group


@app.route('/')
@app.route('/overview')
def index():
    tables = {
        'counts': {'name': 'overview', 'header': [], 'data': []},
        'bookmarks': {
            'name': 'bookmarks',
            'header': ['name', 'class', 'first', 'last', ''],
            'data': []}}
    if current_user.is_authenticated:
        for entity_id in current_user.bookmarks:
            entity = EntityMapper.get_by_id(entity_id)
            tables['bookmarks']['data'].append([
                link(entity),
                openatlas.classes[entity.class_.id].name,
                entity.first,
                entity.last,
                bookmark_toggle(entity.id)])
        for name, count in EntityMapper.get_overview_counts().items():
            tables['counts']['data'].append([
                '<a href="' + url_for(name + '_index') + '">' + uc_first(_(name)) + '</a>',
                count])
    return render_template(
        'index/index.html',
        intro=ContentMapper.get_translation('intro'),
        tables=tables)


@app.route('/index/setlocale/<language>')
def set_locale(language):
    session['language'] = language
    if hasattr(current_user, 'id') and current_user.id:
        current_user.settings['language'] = language
        current_user.update_settings()
    return redirect(request.referrer)


@app.route('/index/feedback')
@required_group('readonly')
def index_feedback():
    return render_template('index/feedback.html')


@app.route('/index/contact')
def index_contact():
    return render_template('index/contact.html', contact=ContentMapper.get_translation('contact'))


@app.route('/index/credits')
def index_credits():
    return render_template('index/credits.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', e=e), 403


@app.route('/index/changelog')
def index_changelog():
    return render_template('index/changelog.html', versions=Changelog.versions)
