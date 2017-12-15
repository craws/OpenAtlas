# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, flash
from flask_babel import lazy_gettext as _

from openatlas import app, EntityMapper
from openatlas.util.util import required_group, link, truncate_string


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
        flash(_('info orphans deleted:') + str(count), 'info')
    tables = {
        'orphans': {
            'name': 'orphans',
            'header': ['name', 'class', 'type', 'created', 'updated', 'description'],
            'data': []},
        'unlinked': {
            'name': 'unlinked',
            'header': ['name', 'class', 'type', 'created', 'updated', 'description'],
            'data': []}}
    for entity in EntityMapper.get_orphans():
        table_name = 'unlinked' if entity.class_.code in app.config['CODE_CLASS'].keys() else 'orphans'
        tables[table_name]['data'].append([
            link(entity),
            link(entity.class_),
            entity.print_base_type(),
            entity.created,
            entity.modified,
            truncate_string(entity.description)])
    return render_template('admin/orphans.html', tables=tables)
