from typing import Optional

from flask import render_template, url_for, g, flash, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas.api.import_scripts.vocabs import (
    import_vocabs_data, fetch_top_level, get_vocabularies,
    fetch_vocabulary_details, fetch_vocabulary_metadata)
from openatlas.database.connect import Transaction
from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, display_info, is_authorized, required_group, display_form, link)
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
                if is_authorized('manager') else '',
                button(_('show vocabularies'), url_for('show_vocabularies'))
            ])},
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


@app.route('/vocabs/vocabularies')
@required_group('manager')
def show_vocabularies() -> str:
    vocabularies = get_vocabularies()
    table = Table(
        header=[_('name'), 'ID', _('default language'), _('languages')])
    for entry in vocabularies:
        table.rows.append([
            entry['title'],
            entry['id'],
            entry['defaultLanguage'],
            ' '.join(entry['languages']),
            vocabulary_detail(
                url_for('vocabulary_detail_view', id_=entry['id']))])
    tabs = {'vocabularies': Tab(_('vocabularies'), table=table)}
    return render_template(
        'tabs.html',
        tabs=tabs,
        title='VOCABS',
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            ['VOCABS', f"{url_for('vocabs_index')}"],
            _('vocabularies')])


def vocabulary_detail(url: str) -> Optional[str]:
    return link(_('details'), url) if is_authorized('manager') else None






@app.route('/vocabs/<id_>')
@required_group('manager')
def vocabulary_detail_view(id_: str) -> str:
    details = fetch_vocabulary_details(id_)
    data = fetch_vocabulary_metadata(id_, details['conceptUri'])
    print(data)
    tabs = {'vocabularies': Tab(
        _('vocabularies'),
        display_info({
            _('title'): details['title'],
            _('contributor'): data['dc11:contributor'],
            _('relation'): data['dc11:relation'],
            _('creator'): data['dc11:creator'],
            _('description'): data['dc11:description']['value'],
            _('languages'): '<br>'.join(data['dc11:language']),
            _('subject'): '<br>'.join(data['dc11:subject']),
            _('publisher'): data['dc11:publisher'],
            _('license'): data['dct:license'],
            _('rights_holder'): data['dct:rightsHolder'],
            _('version'): data['owl:versionInfo'],
        }),
        )}
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=details['title'],
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            ['VOCABS', f"{url_for('vocabs_index')}"],
            [_('vocabularies'), f"{url_for('show_vocabularies')}"],
            details['title']])


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
