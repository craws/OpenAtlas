from flask import render_template, url_for, flash, g
from werkzeug.utils import redirect

from openatlas import app
from openatlas.api.arche.function import fetch_arche_data, import_arche_data
from openatlas.database.connect import Transaction
from openatlas.models.imports import Import
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import required_group, display_info, button, \
    is_authorized
from flask_babel import lazy_gettext as _


@app.route('/arche')
@required_group('readonly')
def arche_index() -> str:
    content = {
        'ARCHE ID': app.config['ARCHE_ID'],
        'ARCHE Collection IDs': str(app.config['ARCHE_COLLECTION_IDS']),
        'ARCHE URL': app.config['ARCHE_BASE_URL']}
    if is_authorized('manager'):
        content['Fetch data'] = button(_('fetch'), url_for('arche_fetch'))
    return render_template(
        'tabs.html',
        tabs={'info': Tab('info', content=display_info(content))},
        crumbs=['ARCHE'])


@app.route('/arche/fetch')
@required_group('manager')
def arche_fetch() -> str:
    tabs = {}
    content = {
        _('import data'): button(
            _('import arche data'), url_for('arche_import_data'))}
    # Development data, can be deleted in production
    # content[_('complete data')] = str(fetch_arche_data_deprecated())
    # content[_('sanitized data')] = str(arche_import_data)

    names = []
    import_ = Table(
        header=['ID', _('name'), _('image link'), _('image thumbnail link'),
                _('creator'), _('latitude'), _('longitude'), _('description'),
                _('date')])
    for entries in fetch_arche_data().values():
        for metadata in entries.values():
            import_.rows.append([
                metadata['image_id'],
                metadata['name'],
                metadata['image_link'],
                metadata['image_link_thumbnail'],
                metadata['creator'],
                metadata['latitude'],
                metadata['longitude'],
                metadata['description'],
                metadata['date']])
            names.append(metadata['name'].lower())

    if duplicates := Import.check_duplicates('file', names):
        dup_table = Table(header=['name'])
        for i in duplicates:
            dup_table.rows.append([i])
        tabs['duplicates'] = Tab('duplicates', table=dup_table)
        content[_('warning')] = str(_('there are duplicates'))

    tabs['fetched entities'] = Tab('fetched_entities',  table=import_)

    tabs['import'] = Tab('import', content=display_info(content))
    return render_template(
        'tabs.html',
        tabs=tabs,
        crumbs=[['ARCHE', url_for('arche_index')], _('fetch')])


@app.route('/arche/import', methods=['POST', 'GET'])
@required_group('manager')
def arche_import_data() -> str:
    Transaction.begin()
    try:
        entities = import_arche_data()
        Transaction.commit()
        g.logger.log('info', 'import', f'import: {len(entities)}')
        flash(f"{_('import of')}: {len(entities)}", 'info')
    except Exception as e:  # pragma: no cover
        Transaction.rollback()
        g.logger.log('error', 'import', 'import failed', e)
        flash(_('error transaction'), 'error')
    return redirect(url_for('arche_fetch'))
