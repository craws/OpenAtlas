from flask import render_template, url_for, g, flash
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas.api.import_scripts.vocabs import import_vocabs_data, \
    fetch_top_level
from openatlas.database.connect import Transaction
from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, display_info, is_authorized, manual, required_group)


@app.route('/vocabs')
@required_group('readonly')
def vocabs_index() -> str:
    if is_authorized('manager'):
        app.config['VOCABS']['concepts'] = button(
            _('show concepts'),
            url_for('vocabs_fetch', concept='topConcepts'))
    return render_template(
        'tabs.html',
        tabs={'info': Tab(
            'info',
            display_info({
                k: str(v) for k, v in app.config['VOCABS'].items()}),
            buttons=[manual('admin/vocabs')])},
        crumbs=['VOCABS'])


@app.route('/vocabs/<concept>')
@required_group('manager')
def vocabs_fetch(concept: str) -> str:
    data = fetch_top_level(concept)
    table = Table(header=[_('name'), _('uri')])
    for entry in data:
        table.rows.append([entry['label'], entry['uri']])
    tabs = {
        f'fetched_{concept}': Tab(
            f'fetched_{concept.lower()}',
            table=table,
            buttons=[button(
                _('import'),
                url_for('vocabs_import_data', concept=concept))]
            if table.rows else [
                '<p class="uc-first">' + _('no entities to retrieve') +
                '</p>'])}
    return render_template(
        'tabs.html',
        tabs=tabs,
        crumbs=[['VOCABS', url_for('vocabs_index')], _('fetch')])


@app.route('/vocabs/import/<concept>', methods=['POST', 'GET'])
@required_group('manager')
def vocabs_import_data(concept: str) -> Response:
    try:
        count = import_vocabs_data(concept)
        Transaction.commit()
        g.logger.log('info', 'import', f'import: {count} top concepts')
        flash(f"{_('import of')}: {count} {_('top concepts')}", 'info')
    except Exception as e:
        Transaction.rollback()
        g.logger.log('error', 'import', 'import failed', e)
        flash(_('error transaction'), 'error')
    return redirect(url_for('vocabs_index'))
