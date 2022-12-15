from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display import display
from openatlas.display.tab import Tab
from openatlas.forms.form import get_table_form
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.table import Table
from openatlas.util.util import (
    button, display_form, is_authorized, link, required_group, uc_first)
from openatlas.views.link import AddReferenceForm


@app.route('/entity/<int:id_>')
@required_group('readonly')
def view(id_: int) -> Union[str, Response]:
    if id_ in g.types:  # Types have their own view
        entity = g.types[id_]
        if not entity.root:
            return redirect(
                f"{url_for('type_index')}"
                f"#menu-tab-{entity.category}_collapse-{id_}")
    elif id_ in g.reference_systems:
        entity = g.reference_systems[id_]
    else:
        entity = Entity.get_by_id(id_, types=True, aliases=True)
        if not entity.class_.view:
            flash(_("This entity can't be viewed directly."), 'error')
            abort(400)
    class_name = \
        f"{''.join(i.capitalize() for i in entity.class_.name.split('_'))}"
    manager = getattr(display, f'{class_name}Display')(entity)
    return render_template(
        'tabs.html',
        tabs=manager.tabs,
        entity=entity,
        gis_data=manager.gis_data,
        crumbs=manager.crumbs)

    #if isinstance(entity, ReferenceSystem):
    #    tabs |= add_tabs_for_reference_system(entity)


@app.route('/entity/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def entity_add_file(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                'P67',
                request.form['checkbox_values'], inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-file")
    return render_template(
        'content.html',
        content=get_table_form(
            'file',
            entity.get_linked_entities('P67', inverse=True)),
        entity=entity,
        title=entity.name,
        crumbs=[
            [_(entity.class_.view), url_for('index', view=entity.class_.view)],
            entity,
            f"{_('link')} {_('file')}"])


@app.route('/entity/add/source/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_source(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                'P67',
                request.form['checkbox_values'],
                inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-source")
    return render_template(
        'content.html',
        content=get_table_form(
            'source',
            entity.get_linked_entities('P67', inverse=True)),
        title=entity.name,
        crumbs=[
            [_(entity.class_.view), url_for('index', view=entity.class_.view)],
            entity,
            f"{_('link')} {_('source')}"])


@app.route('/entity/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_reference(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    form = AddReferenceForm()
    if form.validate_on_submit():
        entity.link_string(
            'P67',
            form.reference.data,
            description=form.page.data,
            inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-reference")
    form.page.label.text = uc_first(_('page / link text'))
    return render_template(
        'content.html',
        content=display_form(form),
        entity=entity,
        crumbs=[
            [_(entity.class_.view), url_for('index', view=entity.class_.view)],
            entity,
            f"{_('link')} {_('reference')}"])

def add_tabs_for_reference_system(entity: ReferenceSystem) -> dict[str, Tab]:
    tabs = {}
    for name in entity.classes:
        tabs[name] = Tab(
            name,
            entity=entity,
            table=Table([_('entity'), 'id', _('precision')]))
    for link_ in entity.get_links('P67'):
        name = link_.description
        if entity.resolver_url:
            name = \
                f'<a href="{entity.resolver_url}{name}"' \
                f' target="_blank" rel="noopener noreferrer">{name}</a>'
        tabs[link_.range.class_.name].table.rows.append([
            link(link_.range),
            name,
            link_.type.name])
    for name in entity.classes:
        tabs[name].buttons = []
        if not tabs[name].table.rows and is_authorized('manager'):
            tabs[name].buttons = [button(
                _('remove'),
                url_for(
                    'reference_system_remove_class',
                    system_id=entity.id,
                    class_name=name))]
    return tabs
