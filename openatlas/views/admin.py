# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os
from collections import OrderedDict
from os.path import basename, splitext

import datetime
from flask import flash, g, render_template, request, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import Email, InputRequired

from openatlas import app, logger
from openatlas.forms.forms import TableField
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.models.node import NodeMapper
from openatlas.models.settings import SettingsMapper
from openatlas.models.user import UserMapper
from openatlas.util.util import (convert_size, format_date, format_datetime, get_file_path, link,
                                 required_group, send_mail, truncate_string, uc_first)


class LogForm(Form):
    limit = SelectField(_('limit'), choices=((0, _('all')), (100, 100), (500, 500)), default=100)
    priority = SelectField(_('priority'), choices=(app.config['LOG_LEVELS'].items()), default=6)
    user = SelectField(_('user'), choices=([(0, _('all'))]), default=0)
    apply = SubmitField(_('apply'))


class NewsLetterForm(Form):
    subject = StringField(
        '', [InputRequired()], render_kw={'placeholder': _('subject'), 'autofocus': True})
    body = TextAreaField('', [InputRequired()], render_kw={'placeholder': _('content')})
    send = SubmitField(uc_first(_('send')))


class FileForm(Form):
    file_upload_max_size = IntegerField(_('max file size in MB'))
    file_upload_allowed_extension = StringField('allowed file extensions')
    save = SubmitField(uc_first(_('save')))


class LogoForm(Form):
    file = TableField(_('file'), [InputRequired()])
    save = SubmitField(uc_first(_('change logo')))


class TestMail(Form):
    receiver = StringField(_('test mail receiver'), [InputRequired(), Email()])
    send = SubmitField(_('send test mail'))


class GeneralForm(Form):
    site_name = StringField(uc_first(_('site name')))
    site_header = StringField(uc_first(_('site header')))
    default_language = SelectField(uc_first(
        _('default language')),
        choices=app.config['LANGUAGES'].items())
    default_table_rows = SelectField(
        uc_first(_('default table rows')),
        choices=app.config['DEFAULT_TABLE_ROWS'].items(),
        coerce=int)
    log_level = SelectField(
        uc_first(_('log level')),
        choices=app.config['LOG_LEVELS'].items(),
        coerce=int)
    debug_mode = BooleanField(uc_first(_('debug mode')))
    random_password_length = IntegerField(uc_first(_('random password length')))
    minimum_password_length = IntegerField(uc_first(_('minimum password length')))
    reset_confirm_hours = IntegerField(uc_first(_('reset confirm hours')))
    failed_login_tries = IntegerField(uc_first(_('failed login tries')))
    failed_login_forget_minutes = IntegerField(uc_first(_('failed login forget minutes')))
    save = SubmitField(uc_first(_('save')))


class MailForm(Form):
    mail = BooleanField(uc_first(_('mail')))
    mail_transport_username = StringField(uc_first(_('mail transport username')))
    mail_transport_host = StringField(uc_first(_('mail transport host')))
    mail_transport_port = StringField(uc_first(_('mail transport port')))
    mail_from_email = StringField(uc_first(_('mail from email')), [Email()])
    mail_from_name = StringField(uc_first(_('mail from name')))
    mail_recipients_feedback = StringField(uc_first(_('mail recipients feedback')))
    save = SubmitField(uc_first(_('save')))


@app.route('/admin')
@required_group('readonly')
def admin_index():
    export_path = app.config['EXPORT_FOLDER_PATH']
    writeable_dirs = {
        'upload': True if os.access(app.config['UPLOAD_FOLDER_PATH'], os.W_OK) else False,
        'export/sql': True if os.access(export_path + '/sql', os.W_OK) else False,
        'export/csv': True if os.access(export_path + '/csv', os.W_OK) else False}
    return render_template('admin/index.html', writeable_dirs=writeable_dirs)


@app.route('/admin/check_links')
@app.route('/admin/check_links/<check>')
@required_group('admin')
def admin_check_links(check=None):
    table = None
    if check:
        table = {'id': 'check', 'header': ['domain', 'property', 'range'], 'data': []}
        for result in LinkMapper.check_links():  # pragma: no cover
            table['data'].append([result['domain'], result['property'], result['range']])
    return render_template('admin/check_links.html', table=table)


@app.route('/admin/file', methods=['POST', 'GET'])
@required_group('admin')
def admin_file():
    form = FileForm()
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            SettingsMapper.update_file_settings(form)
            logger.log('info', 'settings', 'Settings updated')
            g.cursor.execute('COMMIT')
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('admin_index'))
    form.file_upload_max_size.data = session['settings']['file_upload_max_size']
    form.file_upload_allowed_extension.data = session['settings']['file_upload_allowed_extension']
    return render_template('admin/file.html', form=form)


@app.route('/admin/orphans')
@app.route('/admin/orphans/<delete>')
@required_group('admin')
def admin_orphans(delete=None):
    if delete:
        count = EntityMapper.delete_orphans(delete)
        flash(_('info orphans deleted:') + ' ' + str(count), 'info')
        return redirect(url_for('admin_orphans'))
    header = ['name', 'class', 'type', 'system type', 'created', 'updated', 'description']
    tables = {
        'orphans': {'id': 'orphans', 'header': header, 'data': []},
        'unlinked': {'id': 'unlinked', 'header': header, 'data': []},
        'nodes': {'id': 'nodes', 'header': ['name', 'root'], 'data': []},
        'missing_files': {'id': 'missing_files', 'header': header, 'data': []},
        'orphaned_files': {'id': 'orphaned_files', 'data': [],
                           'header': ['name', 'size', 'date', 'ext']}}
    for entity in EntityMapper.get_orphans():
        name = 'unlinked' if entity.class_.code in app.config['CODE_CLASS'].keys() else 'orphans'
        tables[name]['data'].append([
            link(entity),
            link(entity.class_),
            entity.print_base_type(),
            entity.system_type,
            format_date(entity.created),
            format_date(entity.modified),
            truncate_string(entity.description)])
    for node in NodeMapper.get_orphans():
        tables['nodes']['data'].append([link(node), link(g.nodes[node.root[-1]])])

    file_ids = []
    # Get orphaned file entities (no corresponding file)
    for entity in EntityMapper.get_by_system_type('file'):
        file_ids.append(str(entity.id))
        if not get_file_path(entity):
            tables['missing_files']['data'].append([
                link(entity),
                link(entity.class_),
                entity.print_base_type(),
                entity.system_type,
                format_date(entity.created),
                format_date(entity.modified),
                truncate_string(entity.description)])

    # Get orphaned files (no corresponding entity)
    path = app.config['UPLOAD_FOLDER_PATH']
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        name = basename(file)
        file_path = path + '/' + name
        if name != '.gitignore' and splitext(name)[0] not in file_ids:
            confirm = ' onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"'
            tables['orphaned_files']['data'].append([
                name,
                convert_size(os.path.getsize(file_path)),
                format_date(datetime.datetime.fromtimestamp(os.path.getmtime(file_path))),
                splitext(name)[1],
                '<a href="' + url_for('download_file', filename=name) + '">' + uc_first(
                    _('download')) + '</a>',
                '<a href="' + url_for(
                    'admin_file_delete', filename=name) + '" ' + confirm + '>Delete</a>'])
    return render_template('admin/orphans.html', tables=tables)


@app.route('/admin/logo/', methods=['POST', 'GET'])
@app.route('/admin/logo/<action>')
@required_group('manager')
def admin_logo(action=None):
    if action == 'remove':
        SettingsMapper.set_logo('')
        return redirect(url_for('admin_logo'))
    if session['settings']['logo_file_id']:
        path = get_file_path(int(session['settings']['logo_file_id']))
        return render_template(
            'admin/logo.html', filename=os.path.basename(path) if path else False)
    form = LogoForm()
    if form.validate_on_submit():
        SettingsMapper.set_logo(form.file.data)
        return redirect(url_for('admin_logo'))
    return render_template('admin/logo.html', form=form)


@app.route('/admin/file/delete/<filename>')
@required_group('admin')
def admin_file_delete(filename):  # pragma: no cover
    if filename != 'all':
        try:
            os.remove(app.config['UPLOAD_FOLDER_PATH'] + '/' + filename)
            flash(filename + ' ' + _('was deleted'), 'info')
        except Exception as e:
            logger.log('error', 'file', 'deletion of ' + filename + ' failed', e)
            flash(_('error file delete'), 'error')
        return redirect(url_for('admin_orphans') + '#tab-orphaned-files')

    # Get all files with entities
    file_ids = []
    for entity in EntityMapper.get_by_system_type('file'):
        file_ids.append(str(entity.id))
    # Get orphaned files (no corresponding entity)
    path = app.config['UPLOAD_FOLDER_PATH']
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        filename = basename(file)
        if filename != '.gitignore' and splitext(filename)[0] not in file_ids:
            try:
                os.remove(app.config['UPLOAD_FOLDER_PATH'] + '/' + filename)
            except Exception as e:
                logger.log('error', 'file', 'deletion of ' + filename + ' failed', e)
                flash(_('error file delete'), 'error')
    return redirect(url_for('admin_orphans') + '#tab-orphaned-files')


@app.route('/admin/log', methods=['POST', 'GET'])
@required_group('admin')
def admin_log():
    form = LogForm()
    form.user.choices = [(0, _('all'))] + UserMapper.get_users()
    table = {
        'id': 'log', 'header': ['date', 'priority', 'type', 'message', 'user', 'IP', 'info'],
        'data': []}
    logs = logger.get_system_logs(form.limit.data, form.priority.data, form.user.data)
    for row in logs:
        user = UserMapper.get_by_id(row.user_id) if row.user_id else None
        table['data'].append([
            format_datetime(row.created),
            str(row.priority) + ' ' + app.config['LOG_LEVELS'][row.priority],
            row.type,
            row.message,
            link(user) if user and user.id else row.user_id,
            row.ip,
            row.info.replace('\n', '<br />')])
    return render_template('admin/log.html', table=table, form=form)


@app.route('/admin/log/delete')
@required_group('admin')
def admin_log_delete():
    logger.delete_all_system_logs()
    flash(_('Logs deleted'))
    return redirect(url_for('admin_log'))


@app.route('/admin/newsletter', methods=['POST', 'GET'])
@required_group('admin')
def admin_newsletter():
    form = NewsLetterForm()
    if form.validate_on_submit():  # pragma: no cover
        recipients = 0
        for user_id in (request.form.getlist('recipient')):
            user = UserMapper.get_by_id(user_id)
            if user.settings['newsletter'] and user.active:
                code = UserMapper.generate_password()
                user.unsubscribe_code = code
                user.update()
                link_ = request.scheme + '://' + request.headers['Host']
                link_ += url_for('index_unsubscribe', code=code)
                unsubscribe = '\n\n' + _('To unsubscribe use the link below.') + '\n\n' + link_
                if send_mail(form.subject.data, form.body.data + unsubscribe, user.email):
                    recipients += 1
        flash(_('Newsletter send') + ': ' + str(recipients), 'info')
        return redirect(url_for('admin_index'))
    table = {'id': 'user', 'header': ['username', 'email', 'receiver'], 'data': []}
    for user in UserMapper.get_all():
        if user.settings['newsletter'] and user.active:  # pragma: no cover
            checkbox = '<input value="' + str(user.id) + '" name="recipient"'
            checkbox += ' type="checkbox" checked="checked">'
            table['data'].append([user.username, user.email, checkbox])
    return render_template('admin/newsletter.html', form=form, table=table)


@app.route('/admin/mail', methods=["GET", "POST"])
@required_group('admin')
def admin_mail():
    form = TestMail()
    settings = session['settings']
    if form.validate_on_submit() and session['settings']['mail']:  # pragma: no cover
        user = current_user
        subject = _('Test mail from %(site_name)s', site_name=session['settings']['site_name'])
        body = _('This test mail was sent by %(username)s', username=user.username)
        body += ' ' + _('at') + ' ' + request.headers['Host']
        if send_mail(subject, body, form.receiver.data):
            flash(_('A test mail was sent to %(email)s.', email=form.receiver.data))
    else:
        form.receiver.data = current_user.email
    mail_settings = OrderedDict([
        (_('mail'), uc_first(_('on')) if settings['mail'] else uc_first(_('off'))),
        (_('mail transport username'), settings['mail_transport_username']),
        (_('mail transport host'), settings['mail_transport_host']),
        (_('mail transport port'), settings['mail_transport_port']),
        (_('mail from email'), settings['mail_from_email']),
        (_('mail from name'), settings['mail_from_name']),
        (_('mail recipients feedback'), ';'.join(settings['mail_recipients_feedback']))])
    return render_template(
        'admin/mail.html', settings=settings, mail_settings=mail_settings, form=form)


@app.route('/admin/general', methods=["GET", "POST"])
@required_group('admin')
def admin_general():
    settings = session['settings']
    general_settings = OrderedDict([
        (_('site name'), settings['site_name']),
        (_('site header'), settings['site_header']),
        (_('default language'), app.config['LANGUAGES'][settings['default_language']]),
        (_('default table rows'), settings['default_table_rows']),
        (_('log level'), app.config['LOG_LEVELS'][int(settings['log_level'])]),
        (_('debug mode'), uc_first(_('on')) if settings['debug_mode'] else uc_first(_('off'))),
        (_('random password length'), settings['random_password_length']),
        (_('minimum password length'), settings['minimum_password_length']),
        (_('reset confirm hours'), settings['reset_confirm_hours']),
        (_('failed login tries'), settings['failed_login_tries']),
        (_('failed login forget minutes'), settings['failed_login_forget_minutes'])])
    return render_template(
        'admin/general.html', settings=settings, general_settings=general_settings)


@app.route('/admin/general/update', methods=["GET", "POST"])
@required_group('admin')
def admin_general_update():
    form = GeneralForm()
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            SettingsMapper.update(form)
            logger.log('info', 'settings', 'Settings updated')
            g.cursor.execute('COMMIT')
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('admin_general'))
    for field in SettingsMapper.fields:
        if field in ['default_table_rows', 'log_level']:
            getattr(form, field).data = int(session['settings'][field])
        elif field in form:
            getattr(form, field).data = session['settings'][field]
    return render_template('admin/general_update.html', form=form, settings=session['settings'])


@app.route('/admin/mail/update', methods=["GET", "POST"])
@required_group('admin')
def admin_mail_update():
    form = MailForm()
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            SettingsMapper.update(form)
            logger.log('info', 'settings', 'Settings updated')
            g.cursor.execute('COMMIT')
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('admin_mail'))
    if request.method == 'GET':
        for field in SettingsMapper.fields:
            if field in ['mail_recipients_feedback']:
                getattr(form, field).data = ';'.join(session['settings'][field])
            elif field in form:
                getattr(form, field).data = session['settings'][field]
    return render_template('admin/mail_update.html', form=form, settings=session['settings'])
