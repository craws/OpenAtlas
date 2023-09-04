from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.api.import_scripts.arche import (
    fetch_collection_data, import_arche_data)
from openatlas.database.connect import Transaction
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, display_info, is_authorized, manual, required_group)


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
            display_info({
                k: str(v) for k, v in app.config['ARCHE'].items()}),
            buttons=[manual('admin/arche')])},
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            'ARCHE'])


@app.route('/arche/fetch')
@required_group('manager')
def arche_fetch() -> str:  # pragma: no cover
    table = Table(header=['ID', _('name')])
    for entries in fetch_collection_data().values():
        table.rows.append([entries['collection_id'], entries['filename']])

    tabs = {
        'fetched_entities': Tab(
            'fetched_entities',
            table=table,
            buttons=[
                button(_('import ARCHE data'), url_for('arche_import_data'))]
            if table.rows else [
                '<p class="uc-first">' + _('no entities to retrieve') +
                '</p>'])}

    return render_template(
        'tabs.html',
        tabs=tabs,
        crumbs=[['ARCHE', url_for('arche_index')], _('fetch')])


@app.route('/arche/import', methods=['GET', 'POST'])
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
