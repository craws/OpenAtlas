from flask import render_template, url_for, flash, g, Response
from werkzeug.utils import redirect
from flask_babel import lazy_gettext as _

from openatlas import app
from openatlas.api.arche.function import fetch_arche_data, import_arche_data
from openatlas.database.connect import Transaction
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    required_group, is_authorized, display_info, button, uc_first)


@app.route('/arche')
@required_group('readonly')
def arche_index() -> str:
    if is_authorized('manager'):
        app.config['ARCHE']['fetch'] = \
            button(_('fetch'), url_for('arche_fetch'))
    return render_template(
        'tabs.html',
        tabs={'info': Tab(
            'info',
            content=display_info({
                k: str(v) for k, v in app.config['ARCHE'].items()}))},
        crumbs=['ARCHE'])


@app.route('/arche/fetch')
@required_group('manager')
def arche_fetch() -> str:
    data = fetch_arche_data()
    table = Table(
        header=[
            'ID', _('name'), _('image link'), _('image thumbnail link'),
            _('creator'), _('latitude'), _('longitude'), _('description'),
            _('license'), _('date')])
    for entries in data.values():
        for metadata in entries.values():  # pragma: no cover
            table.rows.append([
                metadata['image_id'],
                metadata['name'],
                metadata['image_link'],
                metadata['image_link_thumbnail'],
                metadata['creator'],
                metadata['latitude'],
                metadata['longitude'],
                metadata['description'],
                metadata['license'],
                metadata['date']])
    tabs = {
        'fetched_entities': Tab(
            'fetched_entities',
            table=table,
            buttons=[
                button(_('import arche data'), url_for('arche_import_data'))]
            if table.rows else [uc_first(_('no entities to retrieve'))])}

    return render_template(
        'tabs.html',
        tabs=tabs,
        crumbs=[['ARCHE', url_for('arche_index')], _('fetch')])


@app.route('/arche/import', methods=['POST', 'GET'])
@required_group('manager')
def arche_import_data() -> Response:  # pragma: no cover
    Transaction.begin()
    try:
        count = import_arche_data()
        Transaction.commit()
        g.logger.log('info', 'import', f'import: {count}')
        flash(f"{_('import of')}: {count}", 'info')
    except Exception as e:
        Transaction.rollback()
        g.logger.log('error', 'import', 'import failed', e)
        flash(_('error transaction'), 'error')
    return redirect(url_for('arche_fetch'))
