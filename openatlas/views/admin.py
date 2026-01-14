from __future__ import annotations

import importlib
import math
import os
import shutil
from pathlib import Path
from subprocess import run
from typing import Any, Optional

from flask import flash, g, render_template, request, url_for
from flask_babel import format_number, gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.image_processing import create_resized_images
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, check_iiif_file_exist, display_info, link, required_group,
    send_mail)
from openatlas.display.util2 import (
    convert_size, display_bool, is_authorized, manual, sanitize, uc_first)
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField
from openatlas.forms.setting import (
    ApiForm, ContentForm, FileForm, FrontendForm, GeneralForm, IiifForm,
    LogForm, MailForm, MapForm, ModulesForm, TestMailForm)
from openatlas.forms.util import get_form_settings, set_form_settings
from openatlas.models.content import get_content, update_content
from openatlas.models.dates import format_date
from openatlas.models.entity import Entity
from openatlas.models.imports import Project
from openatlas.models.settings import update_settings
from openatlas.models.user import User


@app.route('/admin', methods=['GET', 'POST'], strict_slashes=False)
@required_group('readonly')
def admin_index() -> str:
    users = User.get_all()
    tabs = {
        'file': Tab(
            'file',
            _('files'),
            content=render_template(
                'file.html',
                info=get_form_settings(FileForm()),
                disk_space_info=get_disk_space_info()),
            buttons=[
                manual('entity/file'),
                button(_('edit'), url_for('settings', category='file'))
                if is_authorized('manager') else '']),
        'user': Tab(
            'user',
            _('user'),
            table=get_user_table(users),
            buttons=[
                manual('admin/user'),
                button(_('activity'), url_for('user_activity')),
                get_newsletter_button(users),
                button(_('user'), url_for('user_insert'))
                if is_authorized('manager') else ''])}
    if is_authorized('admin'):
        tabs['general'] = Tab(
            'general',
            _('general'),
            content=display_info(get_form_settings(GeneralForm())),
            buttons=[
                manual('admin/general'),
                button(_('edit'), url_for('settings', category='general')),
                button(_('system log'), url_for('log'))])
        tabs['mail'] = Tab(
            'mail',
            _('email'),
            display_info(get_form_settings(MailForm())) + get_test_mail_form(),
            buttons=[
                manual('admin/mail'),
                button(_('edit'), url_for('settings', category='mail'))])
        tabs['iiif'] = Tab(
            'iiif',
            _('IIIF'),
            content=display_info(get_form_settings(IiifForm())),
            buttons=[
                manual('admin/iiif'),
                button(_('edit'), url_for('settings', category='iiif')),
                button(
                    f'{_('convert all files')} ({count_files_to_convert()})',
                    url_for('convert_iiif_files')),
                button(
                    f'{_('delete all IIIF files')} '
                    f'({count_files_to_delete()})',
                    url_for('delete_iiif_files'))])
    if is_authorized('manager'):
        tabs['modules'] = Tab(
            'modules',
            _('modules'),
            content='<h1>' + uc_first(_('defaults for new user')) + '</h1>'
                    + display_info(get_form_settings(ModulesForm())),
            buttons=[
                manual('admin/modules'),
                button(_('edit'), url_for('settings', category='modules'))])
        tabs['map'] = Tab(
            'map',
            _('map'),
            content=display_info(get_form_settings(MapForm())),
            buttons=[
                manual('admin/map'),
                button(_('edit'), url_for('settings', category='map'))])
        tabs['content'] = Tab(
            'content',
            _('content'),
            content=get_content_table(),
            buttons=[manual('admin/content')])
        tabs['frontend'] = Tab(
            'frontend',
            _('presentation site'),
            content=display_info(get_form_settings(FrontendForm())),
            buttons=[
                manual('admin/presentation_site'),
                button(_('edit'), url_for('settings', category='frontend'))])
    if is_authorized('contributor'):
        tabs['data'] = Tab(
            'data',
            _('data'),
            content=render_template(
                'admin/data.html',
                imports=Project.get_all(),
                info=get_form_settings(ApiForm())))
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('admin'),
        crumbs=[_('admin')])


def get_content_table() -> str:
    table = Table(['name'] + list(app.config['LANGUAGES']))
    for item, languages in get_content().items():
        content = [uc_first(_(item))]
        for language in app.config['LANGUAGES']:
            content.append(sanitize(languages[language]) or '')
        content.append(link(_('edit'), url_for('admin_content', item=item)))
        table.rows.append(content)
    return table.display()


def get_test_mail_form() -> str:
    if not g.settings['mail']:
        return ''
    form = TestMailForm()
    if form.validate_on_submit():
        subject = _(
            'Test mail from %(site_name)s',
            site_name=g.settings['site_name'])
        body = (_(
            'This test mail was sent by %(username)s',
            username=current_user.username) +
            f' {_('at')} {request.headers['Host']}')
        if send_mail(subject, body, form.receiver.data):  # type: ignore
            flash(
                _('A test mail was sent to %(email)s.',
                    email=form.receiver.data),
                'info')
    elif request.method == 'GET':
        form.receiver.data = current_user.email
    return display_form(form)


def get_newsletter_button(users: list[User]) -> str:
    if g.settings['mail'] and is_authorized('manager'):
        for user in users:
            if user.settings['newsletter']:
                return button(_('newsletter'), url_for('newsletter'))
    return ''


def get_user_table(users: list[User]) -> Table:
    table = Table([
        'username', 'name', 'group', 'email', 'newsletter', 'created',
        'last login', 'entities'])
    if is_authorized('manager'):
        table.columns.append(_('info'))
    for user in users:
        user_entities = ''
        if count := User.get_created_entities_count(user.id):
            user_entities = link(
                format_number(count),
                url_for("user_entities", id_=user.id))
        row = [
            link(user),
            user.real_name,
            user.group,
            user.email if is_authorized('manager')
            or user.settings['show_email'] else '',
            display_bool(user.settings['newsletter'], False),
            format_date(user.created),
            format_date(user.login_last_success),
            user_entities]
        if is_authorized('editor'):
            row.append(user.description)
        table.rows.append(row)
    return table


@app.route('/admin/content/<string:item>', methods=['GET', 'POST'])
@required_group('manager')
def admin_content(item: str) -> str | Response:
    for language in app.config['LANGUAGES']:
        setattr(
            ContentForm,
            language,
            TextAreaField(render_kw={'class': 'tinymce'}))
    setattr(ContentForm, 'save', SubmitField(_('save')))
    form = ContentForm()
    if form.validate_on_submit():
        data = []
        for language in app.config['LANGUAGES']:
            data.append({
                'name': item,
                'language': language,
                'text': getattr(form, language).data or ''})
        update_content(data)
        flash(_('info update'))
        return redirect(f"{url_for('admin_index')}#tab-content")
    for language in app.config['LANGUAGES']:
        getattr(form, language).data = get_content()[item][language]
    return render_template(
        'tabs.html',
        tabs={'content': Tab('content', form=form)},
        title=_('content'),
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-content'],
            _(item)])


@app.route('/settings/<category>', methods=['GET', 'POST'])
@required_group('manager')
def settings(category: str) -> str | Response:
    if category in ['general', 'mail', 'iiif'] and not is_authorized('admin'):
        abort(403)
    form = getattr(
        importlib.import_module('openatlas.forms.setting'),
        f'{uc_first(category)}Form')()
    tab = category.replace('api', 'data')
    if form.validate_on_submit():
        data = {}
        for field in form:
            if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
                continue
            value = field.data
            if field.type == 'FieldList':
                value = ' '.join(set(filter(None, field.data)))
            if field.type == 'BooleanField':
                value = 'True' if field.data else ''
            data[field.name] = value
        update_settings(data)
        g.logger.log('info', 'settings', 'Settings updated')
        flash(_('info update'))
        return redirect(f'{url_for('admin_index')}#tab-{tab}')
    if request.method == 'GET':
        set_form_settings(form)
    return render_template(
        'content.html',
        content=display_form(
            form,
            manual_page='admin/' +
            category.replace('frontend', 'presentation_site')),
        title=_('admin'),
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-{tab}'],
            _(category)])


@app.route('/log', methods=['GET', 'POST'])
@required_group('admin')
def log() -> str:
    form: Any = LogForm()
    form.user.choices = \
        [(0, _('all'))] + [(u.id, u.username) for u in User.get_all()]
    table = Table(
        ['date', 'priority', 'type', 'message', 'user', 'info'],
        order=[[0, 'desc']])
    logs = g.logger.get_system_logs(
        form.limit.data,
        form.priority.data,
        form.user.data)
    for row in logs:
        user = None
        if row['user_id']:
            user = f'user id: {row['user_id']}'
            if user_ := User.get_by_id(row['user_id']):
                user = link(user_)
        table.rows.append([
            row['created'].replace(microsecond=0).isoformat()
            if row['created'] else '',
            f'{row['priority']} {app.config['LOG_LEVELS'][row['priority']]}',
            row['type'],
            row['message'],
            user,
            row['info']])
    buttons = [
        button(
            _('delete all logs'),
            url_for('log_delete'),
            onclick=f"return confirm('{_('delete all logs')}?')")]
    return render_template(
        'tabs.html',
        tabs={'log': Tab('log', form=form, table=table, buttons=buttons)},
        title=_('admin'),
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-general'],
            _('system log')])


@app.route('/log/delete')
@required_group('admin')
def log_delete() -> Response:
    g.logger.delete_all_system_logs()
    flash(_('Logs deleted'))
    return redirect(url_for('log'))


@app.route('/newsletter', methods=['GET', 'POST'])
@required_group('manager')
def newsletter() -> str | Response:
    class NewsLetterForm(FlaskForm):
        subject = StringField(
            '',
            [InputRequired()],
            render_kw={
                'class': 'w-100',
                'placeholder': uc_first(_('subject')),
                'autofocus': True})
        body = TextAreaField(
            '',
            [InputRequired()],
            render_kw={
                'class': 'w-100',
                'rows': '8',
                'placeholder': uc_first(_('content'))})
        save = SubmitField(uc_first(_('send')))

    form = NewsLetterForm()
    if form.validate_on_submit():
        count = 0
        for user_id in request.form.getlist('recipient'):
            user = User.get_by_id(int(user_id))
            if user \
                    and user.settings['newsletter'] \
                    and user.active \
                    and user.email:
                code = User.generate_password()
                user.unsubscribe_code = code
                user.update()
                link_ = f'{request.scheme}://{request.headers['Host']}'
                link_ += url_for('index_unsubscribe', code=code)
                if send_mail(
                        form.subject.data,
                        f'{form.body.data}\n\n'
                        f'{_('To unsubscribe use the link below.')}\n\n'
                        f'{link_}',
                        user.email):
                    count += 1
        flash(f"{_('Newsletter send')}: {count}")
        return redirect(url_for('admin_index'))
    table = Table(['username', 'email', 'receiver'])
    for user in User.get_all():
        if user and user.settings['newsletter'] and user.active:
            table.rows.append([
                user.username,
                user.email,
                f'<input value="{user.id}" name="recipient" type="checkbox" '
                'checked="checked">'])
    return render_template(
        'admin/newsletter.html',
        form=form,
        table=table,
        title=_('newsletter'),
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-user'],
            _('newsletter')])


@app.route('/resize_images')
@required_group('admin')
def resize_images() -> Response:
    create_resized_images()
    flash(_('images were created'))
    return redirect(url_for('admin_index') + '#tab-data')


def get_disk_space_info() -> Optional[dict[str, Any]]:
    def upload_ident_with_iiif() -> bool:
        if not iiif_path:
            return False  # pragma: no cover
        return app.config['UPLOAD_PATH'].resolve() == iiif_path.resolve()

    paths = {
        'export': {
            'path': app.config['EXPORT_PATH'], 'size': 0, 'mounted': False},
        'upload': {
            'path': app.config['UPLOAD_PATH'], 'size': 0, 'mounted': False},
        'processed': {
            'path': app.config['PROCESSED_IMAGE_PATH'],
            'size': 0,
            'mounted': False}}
    iiif_path = None
    if g.settings['iiif_path']:
        iiif_path = Path(g.settings['iiif_path'])
        if not upload_ident_with_iiif():
            paths['iiif'] = {'path': iiif_path, 'size': 0, 'mounted': False}
    keys = []
    for key, path in paths.items():
        if os.access(path['path'], os.W_OK):
            size = run(
                ['du', '-sb', path['path']],
                capture_output=True,
                text=True,
                check=True)
            path['size'] = int(size.stdout.split()[0])
            mounted = run(
                ['df', path['path']],
                capture_output=True,
                text=True,
                check=True)
            path['mounted'] = '/mnt/' in mounted.stdout.split()[-1]
            keys.append(key)
    files_size = sum(paths[key]['size'] for key in keys)
    stats = shutil.disk_usage(app.config['UPLOAD_PATH'])
    percent: dict[str, int | Any] = {
        'free': 100 - math.ceil(stats.free / (stats.total / 100)),
        'project': math.ceil(files_size / (stats.total / 100)),
        'export': math.ceil(paths['export']['size'] / (files_size / 100)),
        'upload': math.ceil(paths['upload']['size'] / (files_size / 100)),
        'iiif': 0}
    if iiif_path and not upload_ident_with_iiif():
        percent['iiif'] = math.ceil(paths['iiif']['size'] / (files_size / 100))
    percent['processed'] = math.ceil(
        paths['processed']['size'] / (files_size / 100))
    other_files = stats.total - stats.free - files_size
    percent['other'] = 100 - (percent['project'] + percent['free'])
    return {
        'total': convert_size(stats.total),
        'project': convert_size(files_size),
        'export': convert_size(paths['export']['size']),
        'upload': convert_size(paths['upload']['size']),
        'processed': convert_size(paths['processed']['size']),
        'iiif': convert_size(
            paths['iiif']['size'] if iiif_path and not upload_ident_with_iiif()
            else 0),
        'other_files': convert_size(other_files),
        'free': convert_size(stats.free),
        'percent': percent,
        'mounted': [k for k, v in paths.items() if v['mounted']]}


def count_files_to_convert() -> int:
    total_files = 0
    converted_files = 0
    existing_files = [entity.id for entity in Entity.get_by_class('file')]
    for id_, path in g.files.items():
        if id_ in existing_files and path.suffix in g.display_file_ext:
            total_files += 1
            if check_iiif_file_exist(id_):
                converted_files += 1
    return total_files - converted_files


def count_files_to_delete() -> int:
    return len([id_ for id_ in g.files if check_iiif_file_exist(id_)])
