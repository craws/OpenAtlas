# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, flash, url_for, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms.validators import DataRequired
from wtforms import SelectField, SubmitField, TextAreaField, StringField

import openatlas
from openatlas import app, EntityMapper, NodeMapper
from openatlas.models.user import UserMapper
from openatlas.util.util import (required_group, link, truncate_string, format_datetime, uc_first,
                                 send_mail, format_date)


class LogForm(Form):
    limit = SelectField(_('limit'), choices=((0, 'all'), (100, 100), (500, 500)), default=100)
    priority = SelectField(_('priority'), choices=(app.config['LOG_LEVELS'].items()), default=6)
    user = SelectField(_('user'), choices=([(0, 'all')] + UserMapper.get_users()), default=0)
    apply = SubmitField(_('apply'))


class NewsLetterForm(Form):
    subject = StringField('', [DataRequired()], render_kw={"placeholder": uc_first(_('subject'))})
    body = TextAreaField('', [DataRequired()], render_kw={"placeholder": uc_first(_('content'))})
    send = SubmitField(uc_first(_('send')))


@app.route('/admin')
@required_group('manager')
def admin_index():
    return render_template('admin/index.html')


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
        'orphans': {'name': 'orphans', 'header': header, 'data': []},
        'unlinked': {'name': 'unlinked', 'header': header, 'data': []},
        'nodes': {'name': 'nodes', 'header': ['name', 'root'], 'data': []}}
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
        tables['nodes']['data'].append([link(node), link(openatlas.nodes[node.root[-1]])])
    return render_template('admin/orphans.html', tables=tables)


@app.route('/admin/log', methods=['POST', 'GET'])
@required_group('admin')
def admin_log():
    form = LogForm()
    table = {
        'name': 'log',
        'header': ['date', 'priority', 'type', 'message', 'user', 'IP', 'info'],
        'data': []}
    logs = openatlas.logger.get_system_logs(form.limit.data, form.priority.data, form.user.data)
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
    openatlas.logger.delete_all_system_logs()
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
            if user.settings['newsletter']:
                code = UserMapper.generate_password()
                user.unsubscribe_code = code
                user.update()
                link_ = request.scheme + '://' + request.headers['Host']
                link_ += url_for('index_unsubscribe', code=code)
                unsubscribe = '\n\n' + _('To unsubscribe use the link below.') + '\n\n' + link_
                if send_mail(form.subject.data + unsubscribe, form.body.data, user.email):
                    recipients += 1
        flash(_('Newsletter send') + ': ' + str(recipients), 'info')
        return redirect(url_for('admin_index'))
    table = {'name': 'user', 'header': ['username', 'email', 'receiver'], 'data': []}
    for user in UserMapper.get_all():
        if user.settings['newsletter']:  # pragma: no cover
            checkbox = '<input value="' + str(user.id) + '" name="recipient"'
            checkbox += ' type="checkbox" checked="checked">'
            table['data'].append([user.username, user.email, checkbox])
    return render_template('admin/newsletter.html', form=form, table=table)
