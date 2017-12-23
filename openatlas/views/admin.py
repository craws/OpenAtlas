# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, flash, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import SelectField, SubmitField

import openatlas
from openatlas import app, EntityMapper, NodeMapper
from openatlas.models.user import UserMapper
from openatlas.util.util import required_group, link, truncate_string, format_datetime


class LogForm(Form):
    limit = SelectField(_('limit'), choices=((0, 'all'), (100, 100), (500, 500)), default=100)
    priority = SelectField(_('priority'), choices=(app.config['LOG_LEVELS'].items()), default=6)
    user = SelectField(_('user'), choices=([(0, 'all')] + UserMapper.get_users()), default=0)
    apply = SubmitField(_('apply'))


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
            entity.created,
            entity.modified,
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
    for row in openatlas.logger.get_system_logs(form.limit.data, form.priority.data, form.user.data):
        user = UserMapper.get_by_id(row.user_id) if row.user_id else None
        table['data'].append([
            format_datetime(row.created),
            str(row.priority) + ' ' + app.config['LOG_LEVELS'][row.priority],
            row.type,
            row.message,
            link(user) if user and user.id else row.user_id,
            row.ip,
            truncate_string(row.info)])
    return render_template('admin/log.html', table=table, form=form)


@app.route('/admin/log/delete')
@required_group('admin')
def admin_log_delete():
    openatlas.logger.delete_all_system_logs()
    flash(_('Logs deleted'))
    return redirect(url_for('admin_log'))
