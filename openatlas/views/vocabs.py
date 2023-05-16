from flask import render_template, url_for, g, flash, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas.api.import_scripts.vocabs import (
    import_vocabs_data, fetch_top_level)
from openatlas.database.connect import Transaction
from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, display_info, is_authorized, required_group, display_form)
from openatlas.forms.form import get_vocabs_form
from openatlas.models.settings import Settings


@app.route('/vocabs')
@required_group('readonly')
def vocabs_index() -> str:
    return render_template(
        'tabs.html',
        tabs={'info': Tab(
            'info',
            display_info({
                _('base url'): g.settings['vocabs_base_url'],
                _('endpoint'): g.settings['vocabs_endpoint'],
                _('user'): g.settings['vocabs_user']}),
            buttons=[
                button(_('edit'), url_for('vocabs_update'))
                if is_authorized('manager') else ''])},
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            'VOCABS'])


@app.route('/vocabs/update', methods=['GET', 'POST'])
@required_group('manager')
def vocabs_update() -> str:
    form = get_vocabs_form()
    if form.validate_on_submit():
        Settings.update({
            'vocabs_base_url': form.base_url.data,
            'vocabs_endpoint': form.endpoint.data,
            'vocabs_user': form.vocabs_user.data})
        flash(_('info update'), 'info')
        return redirect(url_for('vocabs_index'))
    if request.method != 'POST':
        form.base_url.data = g.settings['vocabs_base_url']
        form.endpoint.data = g.settings['vocabs_endpoint']
        form.vocabs_user.data = g.settings['vocabs_user']
    return render_template(
        'content.html',
        title='VOCABS',
        content=display_form(form),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            ['VOCABS', f"{url_for('vocabs_index')}"],
            _('edit')])


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


@app.route('/vocabs/import/<concept>', methods=['GET', 'POST'])
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
