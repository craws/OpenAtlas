from typing import Dict, List, Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from psycopg2 import IntegrityError
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.display import external_url, link
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import is_authorized, required_group


@app.route('/reference_system')
@app.route('/reference_system/<action>/<int:id_>')
def reference_system_index(action: Optional[str] = None, id_: Optional[int] = None) -> str:
    if id_ and action == 'delete':
        system = ReferenceSystem.get_by_id(id_)
        if system.forms:
            flash(_('Deletion not possible because forms are attached'), 'error')
        else:
            system.delete()
            logger.log_user(id_, 'delete')
            flash(_('entity deleted'), 'info')
    table = Table(['name', 'website URL', 'resolver URL', 'description'])
    for system in ReferenceSystem.get_all():
        table.rows.append([link(system),
                           external_url(system.website_url),
                           external_url(system.resolver_url),
                           system.description])
    return render_template('reference_system/index.html', table=table)


@app.route('/reference_system/insert', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_insert() -> Union[str, Response]:
    form = build_form('reference_system')
    if form.validate_on_submit():
        url = save(form)
        if url:
            return redirect(url)
    return render_template('reference_system/insert.html', form=form)


@app.route('/reference_system/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_update(id_: int) -> Union[str, Response]:
    entity = ReferenceSystem.get_by_id(id_)
    form = build_form('reference_system', entity)
    if form.validate_on_submit():
        url = save(form, entity)
        if url:
            return redirect(url)
    return render_template('reference_system/update.html', form=form, entity=entity)


@app.route('/reference_system/remove_form/<int:entity_id>/<int:form_id>', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_remove_form(entity_id: int, form_id: int):
    # Todo: check if there are no form connections anymore
    try:
        ReferenceSystem.remove_form(entity_id, form_id)
        flash(_('info update'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'database', 'remove form failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('entity_view', id_=entity_id))


def reference_system_view(entity: Entity) -> Union[str, Response]:
    tabs = {name: Tab(name, origin=entity) for name in ['info']}
    info: Dict[str, Union[str, List[str]]] = {
        _('website URL'): external_url(entity.website_url),
        _('resolver URL'): external_url(entity.resolver_url)}
    for form_id, form_ in ReferenceSystem.get_forms(entity.id).items():
        tabs[form_['name'].replace(' ', '-')] = Tab(form_['name'].replace(' ', '-'), origin=entity)
        tabs[form_['name'].replace(' ', '-')].table.header = [_('entity'), 'id', _('precision')]
    for link_ in entity.get_links('P67'):
        name = link_.description
        if entity.resolver_url:
            name = '<a href="{url}" target="_blank">{name}</a>'.format(
                url=entity.resolver_url + name,
                name=name)
        tab_name = link_.range.view_name.capitalize().replace(' ', '-')
        if tab_name == 'Actor':
            tab_name = g.classes[link_.range.class_.code].name.replace(' ', '_')
        tabs[tab_name].table.rows.append([link(link_.range), name, link_.type.name])
    for form_id, form_ in ReferenceSystem.get_forms(entity.id).items():
        if not tabs[form_['name'].replace(' ', '-')].table.rows and is_authorized('manager'):
            tabs[form_['name'].replace(' ', '-')].buttons = [
                link(_('remove'),
                     url_for('reference_system_remove_form', entity_id=entity.id, form_id=form_id))]
    return render_template('reference_system/view.html', entity=entity, tabs=tabs, info=info)


def save(form: FlaskForm, entity: Optional[Entity] = None, ) -> str:
    g.cursor.execute('BEGIN')
    try:
        if not entity:
            log_action = 'insert'
            entity = ReferenceSystem.insert(form)
        else:
            log_action = 'update'
            entity.name = form.name.data
            entity.description = form.description.data
            entity.website_url = form.website_url.data if form.website_url.data else None
            entity.resolver_url = form.resolver_url.data if form.resolver_url.data else None
            ReferenceSystem.update(entity)
        ReferenceSystem.add_forms(entity, form)
        g.cursor.execute('COMMIT')
        logger.log_user(entity.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
        return url_for('entity_view', id_=entity.id)
    except IntegrityError as e:
        g.cursor.execute('ROLLBACK')
        flash(_('error name exists'), 'error')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    return ''
