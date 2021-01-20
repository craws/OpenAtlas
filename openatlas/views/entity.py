import datetime
import sys
from typing import Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response


from openatlas import app, logger
from openatlas.forms.form import build_table_form
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.util.display import convert_size, format_date, get_base_table_data, get_file_path, \
    link, uc_first
from openatlas.util.table import Table
from openatlas.util.util import get_file_stats, required_group
from openatlas.views.reference import AddReferenceForm
from openatlas.views.types import node_view


@app.route('/entity/<int:id_>')
@required_group('readonly')
def entity_view(id_: int) -> Union[str, Response]:
    if id_ in g.nodes:
        node = g.nodes[id_]
        if node.root:
            return node_view(node)
        else:  # pragma: no cover
            if node.class_.code == 'E53':
                tab_hash = '#menu-tab-places_collapse-'
            elif node.standard:
                tab_hash = '#menu-tab-standard_collapse-'
            elif node.value_type:
                tab_hash = '#menu-tab-value_collapse-'
            else:
                tab_hash = '#menu-tab-custom_collapse-'
            return redirect(url_for('node_index') + tab_hash + str(id_))
    if id_ in g.reference_systems:
        entity = g.reference_systems[id_]
    else:
        entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        if not entity.view_name:  # pragma: no cover
            flash(_("This entity can't be viewed directly."), 'error')
            abort(400)
    # Return the respective view function, e.g. place_view() in views/place.py if it is a place
    return getattr(sys.modules['openatlas.views.' + entity.view_name],
                   '{name}_view'.format(name=entity.view_name))(entity)


@app.route('/index/<class_>')
@app.route('/index/<class_>/<int:delete_id>')
@required_group('readonly')
def index(class_: str, delete_id: Optional[int] = None) -> Union[str, Response]:
    if delete_id and class_ == 'place':
        entity = Entity.get_by_id(delete_id)
        parent = None if entity.system_type == 'place' else entity.get_linked_entity('P46', True)
        if entity.get_linked_entities(['P46']):
            flash(_('Deletion not possible if subunits exists'), 'error')
            return redirect(url_for('entity_view', id_=delete_id))
        entity.delete()
        logger.log_user(delete_id, 'delete')
        flash(_('entity deleted'), 'info')
        if parent:
            tab = '#tab-' + entity.system_type.replace(' ', '-')
            return redirect(url_for('entity_view', id_=parent.id) + tab)
    elif delete_id:
        Entity.delete_(delete_id)
        logger.log_user(delete_id, 'delete')
        flash(_('entity deleted'), 'info')
        if class_ == 'file':
            try:
                path = get_file_path(delete_id)
                if path:  # Only delete file on disk if it exists to prevent a missing file error
                    path.unlink()
            except Exception as e:  # pragma: no cover
                logger.log('error', 'file', 'file deletion failed', e)
                flash(_('error file delete'), 'error')
    if class_ == 'file':
        table = Table(['date'] + Table.HEADERS['file'])
        file_stats = get_file_stats()
        for entity in Entity.get_by_system_type('file', nodes=True):
            date = 'N/A'
            if entity.id in file_stats:
                date = format_date(
                    datetime.datetime.utcfromtimestamp(file_stats[entity.id]['date']))
            table.rows.append([
                date,
                link(entity),
                entity.print_base_type(),
                convert_size(file_stats[entity.id]['size']) if entity.id in file_stats else 'N/A',
                file_stats[entity.id]['ext'] if entity.id in file_stats else 'N/A',
                entity.description])
    else:
        table = Table(Table.HEADERS[class_])
        if class_ == 'place':
            entities = Entity.get_by_system_type(
                'place',
                nodes=True,
                aliases=current_user.settings['table_show_aliases'])
        else:
            entities = Entity.get_by_menu_item(class_)
        table.rows = [get_base_table_data(item) for item in entities]
    return render_template('entity/index.html',
                           table=table,
                           class_=class_,
                           gis_data=Gis.get_all() if class_ == 'place' else None)


@app.route('/entity/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def entity_add_file(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-file')
    form = build_table_form('file', entity.get_linked_entities('P67', inverse=True))
    return render_template('entity/add_file.html', entity=entity, form=form)


@app.route('/entity/add/source/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_source(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    property_code = 'P128' if entity.class_.code == 'E84' else 'P67'
    inverse = False if entity.class_.code == 'E84' else True
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(property_code, request.form['checkbox_values'], inverse=inverse)
        return redirect(url_for('entity_view', id_=id_) + '#tab-source')
    form = build_table_form('source', entity.get_linked_entities(property_code, inverse=inverse))
    return render_template('entity/add_source.html', entity=entity, form=form)


@app.route('/entity/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_reference(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    form = AddReferenceForm()
    if form.validate_on_submit():
        entity.link_string('P67', form.reference.data, description=form.page.data, inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-reference')
    form.page.label.text = uc_first(_('page / link text'))
    return render_template('entity/add_reference.html', entity=entity, form=form)
