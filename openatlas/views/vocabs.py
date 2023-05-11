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
            url_for('vocabs_fetch', id_='topConcepts'))
    return render_template(
        'tabs.html',
        tabs={'info': Tab(
            'info',
            display_info({
                k: str(v) for k, v in app.config['VOCABS'].items()}),
            buttons=[manual('admin/vocabs')])},
        crumbs=['VOCABS'])


@app.route('/vocabs/<id_>')
@required_group('manager')
def vocabs_fetch(id_: str) -> str:
    data = fetch_top_level(id_)
    table = Table(
        header=[_('name'), _('uri')])
    for entry in data:
        table.rows.append([entry['label'], entry['uri']])
    tabs = {
        f'fetched_{id_}': Tab(
            f'fetched_{id_}',
            table=table,
            buttons=[
                button(_('import'),
                       url_for('vocabs_import_data', id_=id_))]
            if table.rows else [
                '<p class="uc-first">' + _('no entities to retrieve') +
                '</p>'])}
    return render_template(
        'tabs.html',
        tabs=tabs,
        crumbs=[['VOCABS', url_for('vocabs_index')], _('fetch')])


@app.route('/vocabs/import/<id_>', methods=['POST', 'GET'])
@required_group('manager')
def vocabs_import_data(id_: str) -> Response:
    # try:
    count = import_vocabs_data(id_)
    Transaction.commit()
    g.logger.log('info', 'import', f'import: {count}')
    flash(f"{_('import of')}: {count}", 'info')
    # except Exception as e:
    #     Transaction.rollback()
    #     g.logger.log('error', 'import', 'import failed', e)
    #     flash(_('error transaction'), 'error')
    return redirect(url_for('vocabs_index'))
