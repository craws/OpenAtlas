import sys
from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas.models.gis import Gis
from openatlas.util.display import link
from openatlas import app
from openatlas.forms.form import build_table_form
from openatlas.models.entity import Entity
from openatlas.models.user import User
from openatlas.util.display import (add_edit_link, add_remove_link, get_base_table_data,
                                    get_entity_data, get_profile_image_table_link, uc_first)
from openatlas.util.tab import Tab
from openatlas.util.util import is_authorized, required_group
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

    if entity.view_name not in ['source', 'event']:
        # Return the respective view function, e.g. place_view() in views/place.py if it is a place
        return getattr(sys.modules['openatlas.views.' + entity.view_name],
                       '{name}_view'.format(name=entity.view_name))(entity)

    objects = None
    profile_image_id = None
    entity.note = User.get_note(entity)
    tabs = {'info': Tab('info', entity)}
    if entity.view_name == 'source':
        for name in ['event', 'actor', 'place', 'feature', 'stratigraphic_unit', 'find',
                     'human_remains', 'reference', 'text', 'file']:
            tabs[name] = Tab(name, entity)
        for text in entity.get_linked_entities('P73', nodes=True):
            tabs['text'].table.rows.append([link(text),
                                            next(iter(text.nodes)).name if text.nodes else '',
                                            text.description])
        for link_ in entity.get_links('P67'):
            range_ = link_.range
            data = get_base_table_data(range_)
            data = add_remove_link(data, range_.name, link_, entity, range_.table_name)
            tabs[range_.table_name].table.rows.append(data)
        profile_image_id = entity.get_profile_image_id()
        for link_ in entity.get_links('P67', True):
            domain = link_.domain
            data = get_base_table_data(domain)
            if domain.view_name == 'file':  # pragma: no cover
                extension = data[3]
                data.append(
                    get_profile_image_table_link(domain, entity, extension, profile_image_id))
                if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    profile_image_id = domain.id
            if domain.view_name not in ['file']:
                data.append(link_.description)
                data = add_edit_link(data, url_for('reference_link_update',
                                                   link_id=link_.id,
                                                   origin_id=entity.id))
            data = add_remove_link(data, domain.name, link_, entity, domain.view_name)
            tabs[domain.view_name].table.rows.append(data)

    if entity.view_name == 'event':
        for name in ['info', 'subs', 'source', 'actor', 'reference', 'file']:
            tabs[name] = Tab(name, entity)
        for sub_event in entity.get_linked_entities('P117', inverse=True, nodes=True):
            tabs['subs'].table.rows.append(get_base_table_data(sub_event))
        tabs['actor'].table.header.insert(5, _('activity'))  # Add a table column for activity
        for link_ in entity.get_links(['P11', 'P14', 'P22', 'P23']):
            first = link_.first
            if not link_.first and entity.first:
                first = '<span class="inactive">' + entity.first + '</span>'
            last = link_.last
            if not link_.last and entity.last:
                last = '<span class="inactive">' + entity.last + '</span>'
            data = [link(link_.range),
                    g.classes[link_.range.class_.code].name,
                    link_.type.name if link_.type else '',
                    first,
                    last,
                    g.properties[link_.property.code].name_inverse,
                    link_.description]
            if is_authorized('contributor'):
                data.append(
                    link(_('edit'),
                         url_for('involvement_update', id_=link_.id, origin_id=entity.id)))
            data = add_remove_link(data, link_.range.name, link_, entity, 'actor')
            tabs['actor'].table.rows.append(data)
        profile_image_id = entity.get_profile_image_id()

        for link_ in entity.get_links('P67', True):
            domain = link_.domain
            data = get_base_table_data(domain)
            if domain.view_name == 'file':
                extension = data[3]
                data.append(
                    get_profile_image_table_link(domain, entity, extension, profile_image_id))
                if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    profile_image_id = domain.id
            if domain.view_name not in ['source', 'file']:
                data.append(link_.description)
                data = add_edit_link(data, url_for('reference_link_update',
                                                   link_id=link_.id,
                                                   origin_id=entity.id))
                if domain.view_name == 'reference_system':
                    entity.reference_systems.append(link_)
                    continue
            data = add_remove_link(data, domain.name, link_, entity, domain.view_name)
            tabs[domain.view_name].table.rows.append(data)
        objects = [location.get_linked_entity_safe('P53', True) for location
                   in entity.get_linked_entities(['P7', 'P26', 'P27'])]

    return render_template('entity/view.html',
                           entity=entity,
                           gis_data=Gis.get_all(objects) if objects else None,
                           tabs=tabs,
                           info=get_entity_data(entity),
                           crumb=[[_(entity.view_name), url_for('entity_view', id_=entity.id)],
                                  entity.name],
                           profile_image_id=profile_image_id)


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
