import datetime
import importlib
import os
from typing import Optional, Union

from flask import flash, g, render_template, request, session, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms.setting import (
    ApiForm, ContentForm, FilesForm, GeneralForm, LogForm, MailForm, MapForm, ModulesForm,
    SimilarForm, TestMailForm)
from openatlas.forms.util import get_form_settings, set_form_settings
from openatlas.models.content import Content
from openatlas.models.date import Date
from openatlas.models.entity import Entity
from openatlas.models.imports import Import
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.settings import Settings
from openatlas.models.user import User
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import (
    button, convert_size, delete_link, display_form, display_info, format_date, format_datetime,
    get_disk_space_info, get_file_path, get_file_stats, is_authorized, link, manual, required_group,
    sanitize, send_mail, uc_first)


@app.route('/admin', methods=["GET", "POST"])
@app.route('/admin/', methods=["GET", "POST"])
@app.route('/admin/<action>/<int:id_>')
@required_group('readonly')
def admin_index(action: Optional[str] = None, id_: Optional[int] = None) -> Union[str, Response]:
    if is_authorized('manager'):
        if id_ and action == 'delete_user':
            user = User.get_by_id(id_)
            if not user \
                    or user.id == current_user.id \
                    or (user.group == 'admin' and not is_authorized('admin')):
                abort(403)  # pragma: no cover
            User.delete(id_)
            flash(_('user deleted'), 'info')
        elif action == 'remove_logo':
            Settings.set_logo()
            return redirect(f"{url_for('admin_index')}#tab-file")
    dirs = {
        'uploads': True if os.access(app.config['UPLOAD_DIR'], os.W_OK) else False,
        'export/sql': True if os.access(app.config['EXPORT_DIR'] / 'sql', os.W_OK) else False,
        'export/csv': True if os.access(app.config['EXPORT_DIR'] / 'csv', os.W_OK) else False}
    tables = {
        'user': Table([
            'username', 'name', 'group', 'email', 'newsletter', 'created', 'last login', 'entities'
        ]),
        'content': Table(['name'] + [language for language in app.config['LANGUAGES'].keys()])}
    for user in User.get_all():
        count = User.get_created_entities_count(user.id)
        email = user.email if is_authorized('manager') or user.settings['show_email'] else ''
        tables['user'].rows.append([
            link(user),
            user.real_name,
            user.group,
            email,
            _('yes') if user.settings['newsletter'] else '',
            format_date(user.created),
            format_date(user.login_last_success),
            format_number(count) if count else ''])
    for item, languages in Content.get_content().items():
        content = [uc_first(_(item))]
        for language in app.config['LANGUAGES'].keys():
            content.append(sanitize(languages[language], 'text'))
        content.append(link(_('edit'), url_for('admin_content', item=item)))
        tables['content'].rows.append(content)
    form = None
    if is_authorized('admin'):
        form = TestMailForm()
        if form.validate_on_submit() and session['settings']['mail']:  # pragma: no cover
            subject = _('Test mail from %(site_name)s', site_name=session['settings']['site_name'])
            body = _('This test mail was sent by %(username)s', username=current_user.username)
            body += f" {_('at')} '{request.headers['Host']}"
            if send_mail(subject, body, form.receiver.data):
                flash(_('A test mail was sent to %(email)s.', email=form.receiver.data), 'info')
        else:
            form.receiver.data = current_user.email
    tabs = {
        'files': Tab(
            _('files'),
            buttons=[
                manual('entity/file'),
                button(_('edit'), url_for('admin_settings', category='files'))
                if is_authorized('manager') else '',
                button(_('list'), url_for('index', view='file')),
                button(_('file'), url_for('insert', class_='file'))],
            content=render_template(
                'admin/file.html',
                writeable_dirs=dirs,
                info=get_form_settings(FilesForm()),
                settings=session['settings'],
                disk_space_info=get_disk_space_info())),
        'user': Tab(
            _('user'),
            table=tables['user'],
            buttons=[
                manual('admin/user'),
                button(_('activity'), url_for('user_activity')),
                button(_('newsletter'), url_for('admin_newsletter'))
                if is_authorized('manager') and session['settings']['mail'] else '',
                button(_('user'), url_for('user_insert')) if is_authorized('manager') else ''])}
    if is_authorized('admin'):
        tabs['general'] = Tab(
            'general',
            content=display_info(get_form_settings(GeneralForm())),
            buttons=[
                manual('admin/general'),
                button(_('edit'), url_for('admin_settings', category='general')),
                button(_('system log'), url_for('admin_log'))])
        tabs['email'] = Tab(
            'email',
            content=display_info(get_form_settings(MailForm())),
            buttons=[
                manual('admin/mail'),
                button(_('edit'), url_for('admin_settings', category='mail'))])
        if session['settings']['mail']:
            tabs['email'].content += display_form(form)
    if is_authorized('manager'):
        tabs['modules'] = Tab(
            _('modules'),
            content=f"""
                <h1>{_('Defaults for new user')}</h1>
                {display_info(get_form_settings(ModulesForm()))}""",
            buttons=[
                manual('admin/modules'),
                button(_('edit'), url_for('admin_settings', category='modules'))])
        tabs['map'] = Tab(
            'map',
            content=display_info(get_form_settings(MapForm())),
            buttons=[
                manual('admin/map'),
                button(_('edit'), url_for('admin_settings', category='map'))])
        tabs['content'] = Tab(
            'content',
            content=tables['content'].display(),
            buttons=[manual('admin/content')])
    if is_authorized('contributor'):
        tabs['data'] = Tab('data', content=render_template(
            'admin/data.html',
            imports=Import.get_all_projects(),
            info=get_form_settings(ApiForm())))
    return render_template('tabs.html', tabs=tabs, title=_('admin'), crumbs=[_('admin')])


@app.route('/admin/content/<string:item>', methods=["GET", "POST"])
@required_group('manager')
def admin_content(item: str) -> Union[str, Response]:
    languages = app.config['LANGUAGES'].keys()
    for language in languages:
        setattr(
            ContentForm,
            language,
            StringField() if item == 'site_name_for_frontend' else TextAreaField())
    form = ContentForm()
    if form.validate_on_submit():
        Content.update_content(item, form)
        flash(_('info update'), 'info')
        return redirect(f"{url_for('admin_index')}#tab-content")
    for language in languages:
        form.__getattribute__(language).data = Content.get_content()[item][language]
    return render_template(
        'admin/content.html',
        item=item,
        form=form,
        languages=languages,
        title=_('content'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-content"], _(item)])


@app.route('/admin/check_links')
@required_group('contributor')
def admin_check_links() -> str:
    return render_template(
        'admin/check_links.html',
        table=Table(
            ['domain', 'property', 'range'],
            rows=[
                [x['domain'], x['property'], x['range']] for x in Link.get_invalid_cidoc_links()]),
        title=_('admin'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-data"], _('check links')])


@app.route('/admin/check_link_duplicates')
@app.route('/admin/check_link_duplicates/<delete>')
@required_group('contributor')
def admin_check_link_duplicates(delete: Optional[str] = None) -> Union[str, Response]:
    if delete:
        count = Link.delete_link_duplicates()
        logger.log('info', 'admin', f"Deleted duplicate links: {count}")
        flash(f"{_('deleted links')}: {count}", 'info')
        return redirect(url_for('admin_check_link_duplicates'))
    table = Table([
        'domain', 'range', 'property_code', 'description', 'type_id', 'begin_from', 'begin_to',
        'begin_comment', 'end_from', 'end_to', 'end_comment', 'count'])
    for row in Link.check_link_duplicates():
        table.rows.append([
            link(Entity.get_by_id(row['domain_id'])),
            link(Entity.get_by_id(row['range_id'])),
            link(g.properties[row['property_code']]),
            row['description'],
            link(g.nodes[row['type_id']]) if row['type_id'] else '',
            format_date(row['begin_from']),
            format_date(row['begin_to']),
            row['begin_comment'],
            format_date(row['end_from']),
            format_date(row['end_to']),
            row['end_comment'],
            row['count']])
    duplicates = False
    if table.rows:
        duplicates = True
    else:  # If no exact duplicates where found check if single types are used multiple times
        table = Table(
            ['entity', 'class', 'base type', 'incorrect multiple types'],
            rows=Link.check_single_type_duplicates())
    return render_template(
        'admin/check_link_duplicates.html',
        table=table,
        duplicates=duplicates,
        title=_('admin'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-data"], _('check link duplicates')])


@app.route('/admin/delete_single_type_duplicate/<int:entity_id>/<int:node_id>')
@required_group('contributor')
def admin_delete_single_type_duplicate(entity_id: int, node_id: int) -> Response:
    Node.remove_by_entity_and_node(entity_id, node_id)
    flash(_('link removed'), 'info')
    return redirect(url_for('admin_check_link_duplicates'))


@app.route('/admin/settings/<category>', methods=['POST', 'GET'])
@required_group('manager')
def admin_settings(category: str) -> Union[str, Response]:
    if category in ['general', 'mail'] and not is_authorized('admin'):
        abort(403)  # pragma: no cover
    form_name = f"{uc_first(category)}Form"
    form = getattr(importlib.import_module('openatlas.forms.setting'), form_name)()
    if form.validate_on_submit():
        Transaction.begin()
        try:
            Settings.update(form)
            logger.log('info', 'settings', 'Settings updated')
            Transaction.commit()
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        tab = 'data' if category == 'api' else category
        tab = 'email' if category == 'mail' else tab
        return redirect(f"{url_for('admin_index')}#tab-{tab}")
    set_form_settings(form)
    return render_template(
        'display_form.html',
        form=form,
        manual_page=f"admin/{category}",
        title=_('admin'),
        crumbs=[
            [_('admin'),
             f"{url_for('admin_index')}#tab-{'data' if category == 'api' else category}"],
            _(category)])


@app.route('/admin/similar', methods=['POST', 'GET'])
@required_group('contributor')
def admin_check_similar() -> str:
    form = SimilarForm()
    form.classes.choices = [(x.name, x.label) for name, x in g.classes.items() if x.label]
    table = None
    if form.validate_on_submit():
        table = Table(['name', _('count')])
        for sample_id, sample in Entity.get_similar_named(form).items():
            html = link(sample['entity'])
            for entity in sample['entities']:
                html += f'<br><br><br><br><br>{link(entity)}'  # Workaround for linebreaks in tables
            table.rows.append([html, len(sample['entities']) + 1])
    return render_template(
        'admin/check_similar.html',
        table=table,
        form=form,
        title=_('admin'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-data"], _('check similar names')])


@app.route('/admin/check/dates')
@required_group('contributor')
def admin_check_dates() -> str:
    tabs = {
        'dates':
            Tab(
                'invalid_dates',
                table=Table(['name', 'class', 'type', 'created', 'updated', 'description'])),
        'link_dates': Tab('invalid_link_dates', table=Table(['link', 'domain', 'range'])),
        'involvement_dates':
            Tab(
                'invalid_involvement_dates',
                table=Table(['actor', 'event', 'class', 'involvement', 'description']))}
    for entity in Date.get_invalid_dates():
        tabs['dates'].table.rows.append([
            link(entity),
            entity.class_.label,
            entity.print_standard_type(),
            format_date(entity.created),
            format_date(entity.modified),
            entity.description])
    for link_ in Date.get_invalid_link_dates():
        name = ''
        if link_.property.code == 'OA7':  # pragma: no cover
            name = 'relation'
        elif link_.property.code == 'P107':  # pragma: no cover
            name = 'member'
        elif link_.property.code in ['P11', 'P14', 'P22', 'P23']:
            name = 'involvement'
        tabs['link_dates'].table.rows.append([
            link(_(name), url_for(f'{name}_update', id_=link_.id, origin_id=link_.domain.id)),
            link(link_.domain),
            link(link_.range)])
    for link_ in Date.invalid_involvement_dates():
        event = link_.domain
        actor = link_.range
        data = [
            link(actor),
            link(event),
            event.class_.label,
            link_.type.name if link_.type else '',
            link_.description,
            link(_('edit'), url_for('involvement_update', id_=link_.id, origin_id=actor.id))]
        tabs['involvement_dates'].table.rows.append(data)
    for tab in tabs.values():
        tab.buttons = [manual('admin/data_integrity_checks')]
        if not tab.table.rows:
            tab.content = _('Congratulations, everything looks fine!')  # pragma: no cover
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('admin'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-data"], _('check dates')])


@app.route('/admin/orphans')
@required_group('contributor')
def admin_orphans() -> str:
    header = ['name', 'class', 'type', 'system type', 'created', 'updated', 'description']
    tabs = {
        'orphans': Tab('orphans', table=Table(header)),
        'unlinked': Tab('unlinked', table=Table(header)),
        'nodes': Tab('type', table=Table(
            ['name', 'root'],
            [[link(node), link(g.nodes[node.root[-1]])] for node in Node.get_node_orphans()])),
        'missing_files': Tab('missing_files', table=Table(header)),
        'orphaned_files': Tab('orphaned_files', table=Table(['name', 'size', 'date', 'ext'])),
        'circular': Tab('circular_dependencies', table=Table(
            ['entity'],
            [[link(e)] for e in Entity.get_entities_linked_to_itself()]))}

    for entity in filter(lambda x: not isinstance(x, ReferenceSystem), Entity.get_orphans()):
        tabs['unlinked' if entity.class_.view else 'orphans'].table.rows.append([
            link(entity),
            link(entity.class_),
            entity.print_standard_type(),
            entity.class_.label,
            format_date(entity.created),
            format_date(entity.modified),
            entity.description])

    # Orphaned file entities with no corresponding file
    entity_file_ids = []
    for entity in Entity.get_by_class('file', nodes=True):
        entity_file_ids.append(entity.id)
        if not get_file_path(entity):
            tabs['missing_files'].table.rows.append([
                link(entity),
                link(entity.class_),
                entity.print_standard_type(),
                entity.class_.label,
                format_date(entity.created),
                format_date(entity.modified),
                entity.description])

    # Orphaned files with no corresponding entity
    for file in app.config['UPLOAD_DIR'].iterdir():
        if file.name != '.gitignore' and int(file.stem) not in entity_file_ids:
            tabs['orphaned_files'].table.rows.append([
                file.stem,
                convert_size(file.stat().st_size),
                format_date(datetime.datetime.utcfromtimestamp(file.stat().st_ctime)),
                file.suffix,
                link(_('download'), url_for('download_file', filename=file.name)),
                delete_link(file.name, url_for('admin_file_delete', filename=file.name))])

    for tab in tabs.values():
        tab.buttons = [manual('admin/data_integrity_checks')]
        if not tab.table.rows:
            tab.content = _('Congratulations, everything looks fine!')
    if tabs['orphaned_files'].table.rows and is_authorized('admin'):
        tabs['orphaned_files'].buttons.append(
            button(
                _('delete all files'),
                url_for('admin_file_delete', filename='all'),
                onclick="return confirm('" +
                        uc_first(_('delete all files without corresponding entities?')) + "')"))
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('admin'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-data"], _('orphans')])


@app.route('/admin/file/delete/<filename>')
@required_group('contributor')
def admin_file_delete(filename: str) -> Response:  # pragma: no cover
    if filename != 'all':  # Delete one file
        try:
            (app.config['UPLOAD_DIR'] / filename).unlink()
            flash(f"{filename} {_('was deleted')}", 'info')
        except Exception as e:
            logger.log('error', 'file', f'deletion of {filename} failed', e)
            flash(_('error file delete'), 'error')
        return redirect(f"{url_for('admin_orphans')}#tab-orphaned-files")

    if is_authorized('admin'):  # Delete all files with no corresponding entity
        entity_file_ids = [entity.id for entity in Entity.get_by_class('file')]
        for file in app.config['UPLOAD_DIR'].iterdir():
            if file.name != '.gitignore' and int(file.stem) not in entity_file_ids:
                try:
                    (app.config['UPLOAD_DIR'] / file.name).unlink()
                except Exception as e:
                    logger.log('error', 'file', f'deletion of {file.name} failed', e)
                    flash(_('error file delete'), 'error')
    return redirect(f"{url_for('admin_orphans')}#tab-orphaned-files")


@app.route('/admin/logo/')
@app.route('/admin/logo/<int:id_>')
@required_group('manager')
def admin_logo(id_: Optional[int] = None) -> Union[str, Response]:
    if session['settings']['logo_file_id']:
        abort(418)  # pragma: no cover - Logo already set
    if id_:
        Settings.set_logo(id_)
        return redirect(f"{url_for('admin_index')}#tab-file")
    file_stats = get_file_stats()
    table = Table([''] + g.table_headers['file'] + ['date'])
    for entity in Entity.get_display_files():
        date = 'N/A'
        if entity.id in file_stats:
            date = format_date(datetime.datetime.utcfromtimestamp(file_stats[entity.id]['date']))
        table.rows.append([
            link(_('set'), url_for('admin_logo', id_=entity.id)),
            entity.name,
            entity.print_standard_type(),
            convert_size(file_stats[entity.id]['size']) if entity.id in file_stats else 'N/A',
            file_stats[entity.id]['ext'] if entity.id in file_stats else 'N/A',
            entity.description,
            date])
    return render_template(
        'admin/logo.html',
        table=table,
        title=_('logo'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-files"], _('logo')])


@app.route('/admin/log', methods=['POST', 'GET'])
@required_group('admin')
def admin_log() -> str:
    form = LogForm()
    form.user.choices = [(0, _('all'))] + User.get_users_for_form()
    table = Table(['date', 'priority', 'type', 'message', 'user', 'info'], order=[[0, 'desc']])
    logs = logger.get_system_logs(form.limit.data, form.priority.data, form.user.data)
    for row in logs:
        user = None
        if row['user_id']:
            try:
                user = link(User.get_by_id(row['user_id']))
            except AttributeError:  # pragma: no cover - user already deleted
                user = f"id {row['user_id']}"
        table.rows.append([
            format_datetime(row['created']),
            f"{row['priority']} {app.config['LOG_LEVELS'][row['priority']]}",
            row['type'],
            row['message'],
            user,
            row['info']])
    return render_template(
        'admin/log.html',
        table=table,
        form=form,
        title=_('admin'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-general"], _('system log')])


@app.route('/admin/log/delete')
@required_group('admin')
def admin_log_delete() -> Response:
    logger.delete_all_system_logs()
    flash(_('Logs deleted'), 'info')
    return redirect(url_for('admin_log'))


@app.route('/admin/newsletter', methods=['POST', 'GET'])
@required_group('manager')
def admin_newsletter() -> Union[str, Response]:
    class NewsLetterForm(FlaskForm):  # type: ignore
        subject = StringField(
            '',
            [InputRequired()],
            render_kw={'placeholder': uc_first(_('subject')), 'autofocus': True})
        body = TextAreaField(
            '',
            [InputRequired()],
            render_kw={'placeholder': uc_first(_('content'))})
        save = SubmitField(_('send'))

    form = NewsLetterForm()
    form.save.label.text = uc_first(_('send'))
    if form.validate_on_submit():  # pragma: no cover
        count = 0
        for user_id in (request.form.getlist('recipient')):
            user = User.get_by_id(user_id)
            if user and user.settings['newsletter'] and user.active and user.email:
                code = User.generate_password()
                user.unsubscribe_code = code
                user.update()
                link_ = f"{request.scheme}://{request.headers['Host']}"
                link_ += url_for('index_unsubscribe', code=code)
                unsubscribe = '\n\n' + _('To unsubscribe use the link below.') + '\n\n' + link_
                if send_mail(form.subject.data, form.body.data + unsubscribe, user.email):
                    count += 1
        flash(f"{_('Newsletter send')}: {count}", 'info')
        return redirect(url_for('admin_index'))
    table = Table(['username', 'email', 'receiver'])
    for user in User.get_all():
        if user and user.settings['newsletter'] and user.active:  # pragma: no cover
            table.rows.append([
                user.username,
                user.email,
                f'<input value="{user.id}" name="recipient" type="checkbox" checked="checked">'])
    return render_template(
        'admin/newsletter.html',
        form=form,
        table=table,
        title=_('newsletter'),
        crumbs=[[_('admin'), f"{url_for('admin_index')}#tab-user"], _('newsletter')])
