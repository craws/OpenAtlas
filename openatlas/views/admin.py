import datetime
import importlib
import os
from os.path import basename, splitext
from typing import Optional, Union

from flask import flash, g, render_template, request, session, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import TextAreaField

from openatlas import app, logger
from openatlas.forms.admin_forms import (ApiForm, ContentForm, FilesForm, GeneralForm, LogForm,
                                         MailForm, MapForm, ModulesForm, NewsLetterForm,
                                         SimilarForm, TestMailForm)
from openatlas.forms.forms import get_form_settings, set_form_settings
from openatlas.models.content import Content
from openatlas.models.date import Date
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.models.settings import Settings
from openatlas.models.user import User
from openatlas.util.table import Table
from openatlas.util.util import (get_file_stats, is_authorized, required_group,
                                 send_mail)
from openatlas.util.display import convert_size, delete_link, format_date, format_datetime, \
    get_disk_space_info, \
    get_file_path, link, sanitize, \
    truncate, uc_first


@app.route('/admin', methods=["GET", "POST"])
@app.route('/admin/<action>/<int:id_>')
@required_group('readonly')
def admin_index(action: Optional[str] = None, id_: Optional[int] = None) -> Union[str, Response]:
    if is_authorized('manager'):
        if id_ and action == 'delete_user':
            User.delete(id_)
            flash(_('user deleted'), 'info')
        elif action == 'remove_logo':
            Settings.set_logo()
            return redirect(url_for('admin_index') + '#tab-file')
    export_path = app.config['EXPORT_FOLDER_PATH']
    dirs = {'uploads': True if os.access(app.config['UPLOAD_FOLDER_PATH'], os.W_OK) else False,
            'export/sql': True if os.access(export_path.joinpath('sql'), os.W_OK) else False,
            'export/csv': True if os.access(export_path.joinpath('csv'), os.W_OK) else False}
    tables = {'user': Table(['username', 'name', 'group', 'email', 'newsletter', 'created',
                             'last login', 'entities']),
              'content': Table(['name'] + [language for language in app.config['LANGUAGES'].keys()]
                               + ['text'])}
    for user in User.get_all():
        count = User.get_created_entities_count(user.id)
        email = user.email if is_authorized('manager') or user.settings['show_email'] else ''
        tables['user'].rows.append([link(user),
                                    user.real_name,
                                    user.group,
                                    email,
                                    _('yes') if user.settings['newsletter'] else '',
                                    format_date(user.created),
                                    format_date(user.login_last_success),
                                    format_number(count) if count else ''])
    for item, languages in Content.get_content().items():
        content = [uc_first(_(item))]
        html_ok = '<img src="/static/images/icons/dialog-apply.png" alt="ok">'
        for language in app.config['LANGUAGES'].keys():
            content.append(html_ok if languages[language] else '')
        content.append(sanitize(languages[session['language']], 'text'))
        content.append(link(_('edit'), url_for('admin_content', item=item)))
        tables['content'].rows.append(content)
    form = None
    if is_authorized('admin'):
        form = TestMailForm()
        if form.validate_on_submit() and session['settings']['mail']:  # pragma: no cover
            subject = _('Test mail from %(site_name)s', site_name=session['settings']['site_name'])
            body = _('This test mail was sent by %(username)s', username=current_user.username)
            body += ' ' + _('at') + ' ' + request.headers['Host']
            if send_mail(subject, body, form.receiver.data):
                flash(_('A test mail was sent to %(email)s.', email=form.receiver.data), 'info')
        else:
            form.receiver.data = current_user.email
    return render_template('admin/index.html',
                           form=form,
                           tables=tables,
                           settings=session['settings'],
                           writeable_dirs=dirs,
                           disk_space_info=get_disk_space_info(),
                           info={'file': get_form_settings(FilesForm()),
                                 'general': get_form_settings(GeneralForm()),
                                 'mail': get_form_settings(MailForm()),
                                 'map': get_form_settings(MapForm()),
                                 'api': get_form_settings(ApiForm()),
                                 'modules': get_form_settings(ModulesForm())})


@app.route('/admin/content/<string:item>', methods=["GET", "POST"])
@required_group('manager')
def admin_content(item: str) -> Union[str, Response]:
    languages = app.config['LANGUAGES'].keys()
    for language in languages:
        setattr(ContentForm, language, TextAreaField())
    form = ContentForm()
    if form.validate_on_submit():
        Content.update_content(item, form)
        flash(_('info update'), 'info')
        return redirect(url_for('admin_index') + '#tab-content')
    content = Content.get_content()
    for language in languages:
        form.__getattribute__(language).data = content[item][language]
    return render_template('admin/content.html', item=item, form=form, languages=languages)


@app.route('/admin/check_links')
@required_group('contributor')
def admin_check_links() -> str:
    table = Table(['domain', 'property', 'range'],
                  rows=[[result['domain'], result['property'], result['range']] for result in
                        Link.check_links()])
    return render_template('admin/check_links.html', table=table)


@app.route('/admin/check_link_duplicates')
@app.route('/admin/check_link_duplicates/<delete>')
@required_group('contributor')
def admin_check_link_duplicates(delete: Optional[str] = None) -> Union[str, Response]:
    if delete:
        delete_count = str(Link.delete_link_duplicates())
        logger.log('info', 'admin', 'Deleted duplicate links: ' + delete_count)
        flash(_('deleted links') + ': ' + delete_count, 'info')
        return redirect(url_for('admin_check_link_duplicates'))
    table = Table(['domain', 'range', 'property_code', 'description', 'type_id', 'begin_from',
                   'begin_to', 'begin_comment', 'end_from', 'end_to', 'end_comment', 'count'])
    for result in Link.check_link_duplicates():
        table.rows.append([link(Entity.get_by_id(result.domain_id)),
                           link(Entity.get_by_id(result.range_id)),
                           link(g.properties[result.property_code]),
                           result.description,
                           link(g.nodes[result.type_id]) if result.type_id else '',
                           format_date(result.begin_from),
                           format_date(result.begin_to),
                           result.begin_comment,
                           format_date(result.end_from),
                           format_date(result.end_to),
                           result.end_comment,
                           result.count])
    duplicates = False
    if table.rows:
        duplicates = True
    else:  # If no exact duplicates where found check if single types are used multiple times
        table = Table(['entity', 'class', 'base type', 'incorrect multiple types'],
                      rows=Link.check_single_type_duplicates())
    return render_template('admin/check_link_duplicates.html', table=table, duplicates=duplicates)


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
    form = getattr(importlib.import_module('openatlas.forms.admin_forms'),
                   uc_first(category) + 'Form')()  # Get forms dynamically
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            Settings.update(form)
            logger.log('info', 'settings', 'Settings updated')
            g.cursor.execute('COMMIT')
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        tab = 'data' if category == 'api' else category
        return redirect(url_for('admin_index') + '#tab-' + tab)
    set_form_settings(form)
    return render_template('admin/settings.html', form=form, category=category)


@app.route('/admin/similar', methods=['POST', 'GET'])
@required_group('contributor')
def admin_check_similar() -> str:
    form = SimilarForm()
    choices = ['source', 'event', 'actor', 'place', 'feature', 'stratigraphic unit', 'find',
               'reference', 'file']
    form.classes.choices = [(x, uc_first(_(x))) for x in choices]
    table = None
    if form.validate_on_submit():
        table = Table(['name', uc_first(_('count'))])
        for sample_id, sample in Entity.get_similar_named(form).items():
            html = link(sample['entity'])
            for entity in sample['entities']:
                html += '<br><br><br><br><br>' + link(entity)  # Workaround for linebreaks in tables
            table.rows.append([html, len(sample['entities']) + 1])
    return render_template('admin/check_similar.html', table=table, form=form)


@app.route('/admin/orphans/delete/<parameter>')
@required_group('admin')
def admin_orphans_delete(parameter: str) -> Response:
    count = Entity.delete_orphans(parameter)
    flash(_('info orphans deleted:') + ' ' + str(count), 'info')
    return redirect(url_for('admin_orphans'))


@app.route('/admin/check/dates')
@required_group('contributor')
def admin_check_dates() -> str:
    # Get invalid date combinations (e.g. begin after end)
    tables = {'link_dates': Table(['link', 'domain', 'range']),
              'involvement_dates': Table(['actor', 'event', 'class', 'involvement', 'description']),
              'dates': Table(['name', 'class', 'type', 'system type', 'created', 'updated',
                              'description'])}
    for entity in Date.get_invalid_dates():
        tables['dates'].rows.append([link(entity),
                                     link(entity.class_),
                                     entity.print_base_type(),
                                     entity.system_type,
                                     format_date(entity.created),
                                     format_date(entity.modified),
                                     entity.description])
    for link_ in Date.get_invalid_link_dates():
        label = ''
        if link_.property.code == 'OA7':  # pragma: no cover
            label = 'relation'
        elif link_.property.code == 'P107':  # pragma: no cover
            label = 'member'
        elif link_.property.code in ['P11', 'P14', 'P22', 'P23']:
            label = 'involvement'
        tables['link_dates'].rows.append([
            link(_(label), url_for(label + '_update', id_=link_.id, origin_id=link_.domain.id)),
            link(link_.domain),
            link(link_.range)])
    for link_ in Date.invalid_involvement_dates():
        event = link_.domain
        actor = link_.range
        data = [link(actor),
                link(event),
                g.classes[event.class_.code].name,
                link_.type.name if link_.type else '',
                link_.description,
                link(_('edit'), url_for('involvement_update', id_=link_.id, origin_id=actor.id))]
        tables['involvement_dates'].rows.append(data)
    return render_template('admin/check_dates.html', tables=tables)


@app.route('/admin/orphans')
@required_group('contributor')
def admin_orphans() -> str:
    header = ['name', 'class', 'type', 'system type', 'created', 'updated', 'description']
    tables = {'orphans': Table(header),
              'unlinked': Table(header),
              'missing_files': Table(header),
              'circular': Table(['entity']),
              'nodes': Table(['name', 'root']),
              'orphaned_files': Table(['name', 'size', 'date', 'ext'])}
    tables['circular'].rows = [[link(entity)] for entity in Entity.get_circular()]
    for entity in Entity.get_orphans():
        name = 'unlinked' if entity.class_.code in app.config['CODE_CLASS'].keys() else 'orphans'
        tables[name].rows.append([link(entity),
                                  link(entity.class_),
                                  entity.print_base_type(),
                                  entity.system_type,
                                  format_date(entity.created),
                                  format_date(entity.modified),
                                  entity.description])
    for node in Node.get_node_orphans():
        tables['nodes'].rows.append([link(node), link(g.nodes[node.root[-1]])])

    # Get orphaned file entities with no corresponding file
    file_ids = []
    for entity in Entity.get_by_system_type('file', nodes=True):
        file_ids.append(str(entity.id))
        if not get_file_path(entity):
            tables['missing_files'].rows.append([link(entity),
                                                 link(entity.class_),
                                                 entity.print_base_type(),
                                                 entity.system_type,
                                                 format_date(entity.created),
                                                 format_date(entity.modified),
                                                 entity.description])

    # Get orphaned files with no corresponding entity
    with os.scandir(app.config['UPLOAD_FOLDER_PATH']) as it:
        for file in it:
            name = file.name
            if name != '.gitignore' and splitext(file.name)[0] not in file_ids:
                tables['orphaned_files'].rows.append([
                    name,
                    convert_size(file.stat().st_size),
                    format_date(datetime.datetime.utcfromtimestamp(file.stat().st_ctime)),
                    splitext(name)[1],
                    link(_('download'), url_for('download_file', filename=name)),
                    delete_link(name, url_for('admin_file_delete', filename=name))])
        return render_template('admin/check_orphans.html', tables=tables)


@app.route('/admin/logo/')
@app.route('/admin/logo/<int:id_>')
@required_group('manager')
def admin_logo(id_: Optional[int] = None) -> Union[str, Response]:
    if session['settings']['logo_file_id']:
        abort(418)  # pragma: no cover - Logo already set
    if id_:
        Settings.set_logo(id_)
        return redirect(url_for('admin_index') + '#tab-file')
    file_stats = get_file_stats()
    table = Table([''] + Table.HEADERS['file'] + ['date'])
    for entity in Entity.get_display_files():
        date = 'N/A'
        if entity.id in file_stats:
            date = format_date(datetime.datetime.utcfromtimestamp(file_stats[entity.id]['date']))
        table.rows.append([
            link(_('set'), url_for('admin_logo', id_=entity.id)),
            truncate(entity.name),
            entity.print_base_type(),
            convert_size(file_stats[entity.id]['size']) if entity.id in file_stats else 'N/A',
            file_stats[entity.id]['ext'] if entity.id in file_stats else 'N/A',
            entity.description,
            date])
    return render_template('admin/logo.html', table=table)


@app.route('/admin/file/delete/<filename>')
@required_group('contributor')
def admin_file_delete(filename: str) -> Response:  # pragma: no cover
    if filename != 'all':
        try:
            os.remove(app.config['UPLOAD_FOLDER_PATH'].joinpath(filename))
            flash(filename + ' ' + _('was deleted'), 'info')
        except Exception as e:
            logger.log('error', 'file', 'deletion of ' + filename + ' failed', e)
            flash(_('error file delete'), 'error')
        return redirect(url_for('admin_orphans') + '#tab-orphaned-files')

    if is_authorized('admin'):
        # Get all files with entities
        file_ids = [str(entity.id) for entity in Entity.get_by_system_type('file')]

        # Get orphaned files (no corresponding entity)
        path = app.config['UPLOAD_FOLDER_PATH']
        for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
            filename = basename(file)
            if filename != '.gitignore' and splitext(filename)[0] not in file_ids:
                try:
                    os.remove(app.config['UPLOAD_FOLDER_PATH'].joinpath(filename))
                except Exception as e:
                    logger.log('error', 'file', 'deletion of ' + filename + ' failed', e)
                    flash(_('error file delete'), 'error')
    return redirect(url_for('admin_orphans') + '#tab-orphaned-files')


@app.route('/admin/log', methods=['POST', 'GET'])
@required_group('admin')
def admin_log() -> str:
    form = LogForm()
    form.user.choices = [(0, _('all'))] + User.get_users()
    table = Table(['date', 'priority', 'type', 'message', 'user', 'info'], order=[[0, 'desc']])
    logs = logger.get_system_logs(form.limit.data, form.priority.data, form.user.data)
    for row in logs:
        user = None
        if row.user_id:
            try:
                user = link(User.get_by_id(row.user_id))
            except AttributeError:  # pragma: no cover - user already deleted
                user = 'id ' + str(row.user_id)
        table.rows.append([format_datetime(row.created),
                           str(row.priority) + ' ' + app.config['LOG_LEVELS'][row.priority],
                           row.type,
                           row.message,
                           user,
                           row.info])
    return render_template('admin/log.html', table=table, form=form)


@app.route('/admin/log/delete')
@required_group('admin')
def admin_log_delete() -> Response:
    logger.delete_all_system_logs()
    flash(_('Logs deleted'), 'info')
    return redirect(url_for('admin_log'))


@app.route('/admin/newsletter', methods=['POST', 'GET'])
@required_group('manager')
def admin_newsletter() -> Union[str, Response]:
    form = NewsLetterForm()
    if form.validate_on_submit():  # pragma: no cover
        recipients = 0
        for user_id in (request.form.getlist('recipient')):
            user = User.get_by_id(user_id)
            if user and user.settings['newsletter'] and user.active and user.email:
                code = User.generate_password()
                user.unsubscribe_code = code
                user.update()
                link_ = request.scheme + '://' + request.headers['Host']
                link_ += url_for('index_unsubscribe', code=code)
                unsubscribe = '\n\n' + _('To unsubscribe use the link below.') + '\n\n' + link_
                if send_mail(form.subject.data, form.body.data + unsubscribe, user.email):
                    recipients += 1
        flash(_('Newsletter send') + ': ' + str(recipients), 'info')
        return redirect(url_for('admin_index'))
    table = Table(['username', 'email', 'receiver'])
    for user in User.get_all():
        if user and user.settings['newsletter'] and user.active:  # pragma: no cover
            table.rows.append([
                user.username,
                user.email,
                '<input value="{id}" name="recipient" type="checkbox" checked="checked">'.format(
                    id=user.id)])
    return render_template('admin/newsletter.html', form=form, table=table)
