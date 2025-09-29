from flask import flash, g, render_template, request, session, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import SelectField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    bookmark_toggle, button, link, required_group, send_mail)
from openatlas.display.util2 import manual, uc_first
from openatlas.models.dates import format_date
from openatlas.forms.field import SubmitField
from openatlas.models.content import get_translation
from openatlas.models.entity import Entity
from openatlas.models.user import User


@app.route('/')
@app.route('/overview')
def overview() -> str:
    if not current_user.is_authenticated:
        return render_template(
            'tabs.html',
            tabs={
                'info': Tab(
                    'info',
                    content=render_template(
                        'index/index_guest.html',
                        intro=get_translation('intro')))},
            crumbs=['overview'])
    frontend_url = current_user.settings['frontend_website_url']
    tabs = {
        'info': Tab(
            'info',
            buttons=[
                link(
                    '<i class="fas fa-book"></i> ' + uc_first(_('manual')),
                    "/static/manual/index.html",
                    class_=app.config['CSS']['button']['primary'],
                    external=True),
                button(_('model'), url_for('model_index')),
                button(
                    _('reference systems'),
                    url_for('index', group='reference_system')),
                button(
                    _('network visualization'),
                    url_for('network', dimensions=0)),
                link(
                    '<i class="fas fa-eye"></i> ' +
                    uc_first(_('presentation site')),
                    frontend_url,
                    external=True) if frontend_url else '']),
        'bookmarks': Tab(
            'bookmarks',
            _('bookmarks'),
            table=Table(['name', 'class', 'begin', 'end'])),
        'notes': Tab(
            'notes',
            _('notes'),
            table=Table(
                ['date', _('visibility'), 'entity', 'class', _('note')]))}
    tables = {
        'overview': Table(
            [_('class'), _('count')],
            paging=False,
            defs=[{'className': 'dt-body-right', 'targets': 1}]),
        'latest': Table([
                _('latest'), _('name'), _('class'), _('begin'), _('end'),
                _('user')],
            paging=False,
            order=[[0, 'desc']])}
    for entity_id in current_user.bookmarks:
        entity = Entity.get_by_id(entity_id)
        tabs['bookmarks'].table.rows.append([
            link(entity),
            uc_first(entity.class_.label),
            entity.dates.first,
            entity.dates.last,
            bookmark_toggle(entity.id, True)])
    for note in User.get_notes_by_user_id(current_user.id):
        entity = Entity.get_by_id(note['entity_id'])
        tabs['notes'].table.rows.append([
            format_date(note['created']),
            _('public') if note['public'] else _('private'),
            link(entity),
            uc_first(entity.class_.label),
            note['text'],
            link(_("view"), url_for("note_view", id_=note["id"]))])
    if tabs['notes'].table.rows:
        tabs['notes'].buttons = [manual('tools/notes')]
    for name, count in Entity.get_overview_counts().items():
        if not g.classes[name].group:
            continue
        url = ''
        if name not in [
                'feature', 'stratigraphic_unit', 'source_translation']:
            url = url_for('index', group=g.classes[name].group['name'])
        if name == 'administrative_unit':
            url = f"{url_for('type_index')}#menu-tab-place"
        elif name == 'type':
            url = url_for('type_index')
        tables['overview'].rows.append([
            link(g.classes[name].label, url) if url
            else uc_first(g.classes[name].label),
            format_number(count)])
    for entity in Entity.get_latest(15):
        tables['latest'].rows.append([
            format_date(entity.created),
            link(entity),
            uc_first(entity.class_.label),
            entity.dates.first,
            entity.dates.last,
            link(g.logger.get_log_info(entity.id)['creator'])])
    tabs['info'].content = render_template('index/index.html', tables=tables)
    return render_template('tabs.html', tabs=tabs, crumbs=['overview'])


@app.route('/index/setlocale/<language>')
def set_locale(language: str) -> Response:
    if language not in app.config['LANGUAGES']:
        language = g.settings['default_language']
    session['language'] = language
    if hasattr(current_user, 'id') and current_user.id:
        current_user.settings['language'] = language
        current_user.update_language()
    return redirect(request.referrer or url_for('overview'))


@app.route('/overview/feedback', methods=['GET', 'POST'])
@required_group('readonly')
def index_feedback() -> str | Response:

    class FeedbackForm(FlaskForm):
        subject = SelectField(
            _('subject'),
            render_kw={'autofocus': True},
            choices=(
                ('suggestion', uc_first(_('suggestion'))),
                ('question', uc_first(_('question'))),
                ('problem', uc_first(_('problem')))))
        description = TextAreaField(_('description'), [InputRequired()])
        save = SubmitField(_('send'))

    form = FeedbackForm()
    if form.validate_on_submit() and g.settings['mail']:
        body = \
            f'{form.subject.data} from {current_user.username} ' \
            f'({current_user.id}) {current_user.email} at ' \
            f'{request.headers["Host"]}\n\n' \
            f'{form.description.data}'
        if send_mail(
                form.subject.data + f" from {g.settings['site_name']}",
                body,
                g.settings['mail_recipients_feedback']):
            flash(_('info feedback thanks'), 'info')
        else:
            flash(_('error mail send'), 'error')  # pragma: no cover
        return redirect(url_for('overview'))
    return render_template(
        'index/feedback.html',
        form=form,
        title=_('feedback'),
        crumbs=[_('feedback')])


@app.route('/overview/content/<item>')
def index_content(item: str) -> str:
    return render_template(
        'content.html',
        content=get_translation(item),
        title=_(_(item)),
        crumbs=[_(item)])


@app.route('/unsubscribe/<code>')
def index_unsubscribe(code: str) -> str:
    user = User.get_by_unsubscribe_code(code)
    content = _('unsubscribe link not valid')
    if user:
        user.settings['newsletter'] = ''
        user.unsubscribe_code = ''
        user.update()
        user.remove_newsletter()
        content = _(
            'You have successfully unsubscribed. '
            'You can subscribe again in your Profile.')
    return render_template(
        'content.html',
        content=content,
        crumbs=[_('unsubscribe newsletter')])
