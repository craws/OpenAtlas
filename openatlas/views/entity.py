from typing import Any, Dict, List, Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.forms.form import build_table_form
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.models.overlay import Overlay
from openatlas.models.place import get_structure
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.user import User
from openatlas.util.display import (add_edit_link, add_remove_link, button, get_base_table_data,
                                    get_entity_data, get_file_path, get_profile_image_table_link,
                                    link, uc_first)
from openatlas.util.filters import display_delete_link
from openatlas.util.tab import Tab
from openatlas.util.util import is_authorized, required_group
from openatlas.views.reference import AddReferenceForm


@app.route('/entity/<int:id_>')
@required_group('readonly')
def entity_view(id_: int) -> Union[str, Response]:
    if id_ in g.nodes:  # Nodes have their own view
        entity = g.nodes[id_]
        if not entity.root:
            if entity.class_.code == 'E53':
                tab_hash = '#menu-tab-places_collapse-'
            elif entity.standard:
                tab_hash = '#menu-tab-standard_collapse-'
            elif entity.value_type:
                tab_hash = '#menu-tab-value_collapse-'
            else:
                tab_hash = '#menu-tab-custom_collapse-'
            return redirect(url_for('node_index') + tab_hash + str(id_))
    elif id_ in g.reference_systems:
        entity = g.reference_systems[id_]
    else:
        entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        if not entity.view_name:
            flash(_("This entity can't be viewed directly."), 'error')
            abort(400)

    event_links = None  # Needed for actor
    structure = None  # Needed for place
    gis_data = None  # Needed for place
    overlays = None  # Needed for place
    entity.note = User.get_note(entity)
    tabs = {'info': Tab('info', entity)}

    # Todo: moving functionality from separate views here was an important step but this if/else is
    #  way too long and error prone to manage or expand, maybe refactor with object/inheritance?
    if entity.view_name == 'node':
        for name in ['subs', 'entities']:
            tabs[name] = Tab(name, entity)
        root = g.nodes[entity.root[-1]] if entity.root else None
        if root and root.value_type:  # pragma: no cover
            tabs['entities'].table.header = [_('name'), _('value'), _('class'), _('info')]
        for item in entity.get_linked_entities(['P2', 'P89'], inverse=True, nodes=True):
            if item.class_.code == 'E32':  # Don't add reference systems themselves
                continue  # pragma: no cover
            if entity.class_.code == 'E53':  # pragma: no cover
                object_ = item.get_linked_entity('P53', inverse=True)
                if not object_:  # If it's a location show the object, continue otherwise
                    continue
                item = object_
            data = [link(item)]
            if root and root.value_type:  # pragma: no cover
                data.append(format_number(item.nodes[entity]))
            data.append(g.classes[item.class_.code].name)
            data.append(item.description)
            tabs['entities'].table.rows.append(data)
        for sub_id in entity.subs:
            sub = g.nodes[sub_id]
            tabs['subs'].table.rows.append([link(sub), sub.count, sub.description])
        if not tabs['entities'].table.rows:  # If no entities available get links with this type_id
            tabs['entities'].table.header = [_('domain'), _('range')]
            for row in Link.get_entities_by_node(entity):
                tabs['entities'].table.rows.append([link(Entity.get_by_id(row.domain_id)),
                                                    link(Entity.get_by_id(row.range_id))])

    elif entity.view_name == 'reference_system':
        for form_id, form_ in entity.get_forms().items():
            tabs[form_['name'].replace(' ', '-')] = Tab(form_['name'].replace(' ', '-'),
                                                        origin=entity)
            tabs[form_['name'].replace(' ', '-')].table.header = [_('entity'), 'id', _('precision')]
        for link_ in entity.get_links('P67'):
            name = link_.description
            if entity.resolver_url:
                name = \
                    '<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>'.format(
                        url=entity.resolver_url + name, name=name)
            tab_name = link_.range.view_name.capitalize().replace(' ', '-')
            if tab_name == 'Actor':  # Instead actor the tabs person, group and legal body are shown
                tab_name = g.classes[link_.range.class_.code].name.replace(' ', '-')
            elif tab_name == 'Place':
                tab_name = link_.range.system_type.title().replace(' ', '-')
            elif tab_name == 'Object':  # pragma: no cover
                tab_name = 'Artifact'
            elif tab_name == 'Node':  # pragma: no cover
                tab_name = 'Type'
            tabs[tab_name].table.rows.append([link(link_.range), name, link_.type.name])
        for form_id, form_ in entity.get_forms().items():
            if not tabs[form_['name'].replace(' ', '-')].table.rows and is_authorized('manager'):
                tabs[form_['name'].replace(' ', '-')].buttons = [
                    button(_('remove'), url_for('reference_system_remove_form',
                                                system_id=entity.id,
                                                form_id=form_id))]
    elif entity.view_name == 'object':
        for name in ['source', 'event']:
            tabs[name] = Tab(name, entity)
        for link_ in entity.get_links('P128'):
            data = get_base_table_data(link_.range)
            data = add_remove_link(data, link_.range.name, link_, entity, link_.range.table_name)
            tabs['source'].table.rows.append(data)
        for link_ in entity.get_links('P25', inverse=True):
            data = get_base_table_data(link_.domain)
            data = add_remove_link(data, link_.range.name, link_, entity, link_.range.table_name)
            tabs['event'].table.rows.append(data)
    elif entity.view_name == 'reference':
        for name in ['source', 'event', 'actor', 'place', 'feature', 'stratigraphic_unit',
                     'find', 'human_remains', 'file', 'object']:
            tabs[name] = Tab(name, entity)
        for link_ in entity.get_links(['P67', 'P128']):
            range_ = link_.range
            data = get_base_table_data(range_)
            data.append(link_.description)
            data = add_edit_link(data, url_for('reference_link_update',
                                               link_id=link_.id,
                                               origin_id=entity.id))
            data = add_remove_link(data, range_.name, link_, entity, range_.table_name)
            tabs[range_.table_name].table.rows.append(data)
    elif entity.view_name == 'place':
        for name in ['source', 'event', 'actor', 'reference']:
            tabs[name] = Tab(name, entity)
        if entity.system_type == 'place':
            tabs['feature'] = Tab('feature', origin=entity)
        elif entity.system_type == 'feature':
            tabs['stratigraphic_unit'] = Tab('stratigraphic_unit', origin=entity)
        elif entity.system_type == 'stratigraphic unit':
            tabs['find'] = Tab('find', origin=entity)
            tabs['human_remains'] = Tab('human_remains', origin=entity)
        entity.location = entity.get_linked_entity_safe('P53', nodes=True)
        event_ids = []  # Keep track of already inserted events to prevent doubles
        for event in entity.location.get_linked_entities(['P7', 'P26', 'P27'], inverse=True):
            tabs['event'].table.rows.append(get_base_table_data(event))
            event_ids.append(event.id)
        for event in entity.get_linked_entities('P24', inverse=True):
            if event.id not in event_ids:  # Don't add again if already in table
                tabs['event'].table.rows.append(get_base_table_data(event))
        for link_ in entity.location.get_links(['P74', 'OA8', 'OA9'], inverse=True):
            actor = Entity.get_by_id(link_.domain.id)
            tabs['actor'].table.rows.append([link(actor),
                                             g.properties[link_.property.code].name,
                                             actor.class_.name,
                                             actor.first,
                                             actor.last,
                                             actor.description])
        structure = get_structure(entity)
        if structure:
            for item in structure['subunits']:
                data = get_base_table_data(item)
                tabs[item.system_type.replace(' ', '_')].table.rows.append(data)
        gis_data = Gis.get_all([entity], structure)
        if gis_data['gisPointSelected'] == '[]' \
                and gis_data['gisPolygonSelected'] == '[]' \
                and gis_data['gisLineSelected'] == '[]' \
                and (not structure or not structure['super_id']):
            gis_data = {}
    elif entity.view_name == 'actor':
        for name in ['source', 'event', 'relation', 'member_of', 'member']:
            tabs[name] = Tab(name, entity)
        event_links = entity.get_links(['P11', 'P14', 'P22', 'P23', 'P25'], True)
        for link_ in event_links:
            event = link_.domain
            places = event.get_linked_entities(['P7', 'P26', 'P27'])
            link_.object_ = None
            for place in places:
                object_ = place.get_linked_entity_safe('P53', True)
                entity.linked_places.append(object_)
                link_.object_ = object_  # Needed later for first/last appearance info
            first = link_.first
            if not link_.first and event.first:
                first = '<span class="inactive">' + event.first + '</span>'
            last = link_.last
            if not link_.last and event.last:
                last = '<span class="inactive">' + event.last + '</span>'
            data = [link(event),
                    g.classes[event.class_.code].name,
                    link(link_.type),
                    first,
                    last,
                    link_.description]
            data = add_edit_link(data,
                                 url_for('involvement_update', id_=link_.id, origin_id=entity.id))
            data = add_remove_link(data, link_.domain.name, link_, entity, 'event')
            tabs['event'].table.rows.append(data)
        for link_ in entity.get_links('OA7') + entity.get_links('OA7', True):
            type_ = ''
            if entity.id == link_.domain.id:
                related = link_.range
                if link_.type:
                    type_ = link(link_.type.get_name_directed(),
                                 url_for('entity_view', id_=link_.type.id))
            else:
                related = link_.domain
                if link_.type:
                    type_ = link(link_.type.get_name_directed(True),
                                 url_for('entity_view', id_=link_.type.id))
            data = [type_, link(related), link_.first, link_.last, link_.description]
            data = add_edit_link(data,
                                 url_for('relation_update', id_=link_.id, origin_id=entity.id))
            data = add_remove_link(data, related.name, link_, entity, 'relation')
            tabs['relation'].table.rows.append(data)
        for link_ in entity.get_links('P107', True):
            data = [link(link_.domain), link(link_.type), link_.first, link_.last,
                    link_.description]
            data = add_edit_link(data, url_for('member_update', id_=link_.id, origin_id=entity.id))
            data = add_remove_link(data, link_.domain.name, link_, entity, 'member-of')
            tabs['member_of'].table.rows.append(data)
        if entity.class_.code not in app.config['CLASS_CODES']['group']:
            del tabs['member']
        else:
            for link_ in entity.get_links('P107'):
                data = [link(link_.range), link(link_.type), link_.first, link_.last,
                        link_.description]
                if is_authorized('contributor'):
                    data.append(link(_('edit'),
                                     url_for('member_update', id_=link_.id, origin_id=entity.id)))
                data = add_remove_link(data, link_.range.name, link_, entity, 'member')
                tabs['member'].table.rows.append(data)
    elif entity.view_name == 'file':
        entity.image_id = entity.id if get_file_path(entity.id) else None
        for name in ['source', 'event', 'actor', 'place', 'feature', 'stratigraphic_unit', 'find',
                     'human_remains', 'reference', 'node', 'object']:
            tabs[name] = Tab(name, entity)
        for link_ in entity.get_links('P67'):
            range_ = link_.range
            data = get_base_table_data(range_)
            data = add_remove_link(data, range_.name, link_, entity, range_.table_name)
            tabs[range_.table_name].table.rows.append(data)
        for link_ in entity.get_links('P67', True):
            data = get_base_table_data(link_.domain)
            data.append(link_.description)
            data = add_edit_link(data,
                                 url_for('reference_link_update', link_id=link_.id,
                                         origin_id=entity.id))
            data = add_remove_link(data, link_.domain.name, link_, entity, 'reference')
            tabs['reference'].table.rows.append(data)
    elif entity.view_name == 'source':
        for name in ['event', 'actor', 'place', 'feature', 'stratigraphic_unit', 'find',
                     'human_remains', 'object', 'text']:
            tabs[name] = Tab(name, entity)
        for text in entity.get_linked_entities('P73', nodes=True):
            tabs['text'].table.rows.append([link(text),
                                            next(iter(text.nodes)).name if text.nodes else '',
                                            text.description])
        for link_ in entity.get_links('P67'):
            range_ = link_.range
            data = get_base_table_data(range_)
            data = add_remove_link(data, range_.name, link_, entity, range_.table_name)
            if range_.table_name in tabs:  # e.g. source has no tab for object (information carrier)
                tabs[range_.table_name].table.rows.append(data)
    elif entity.view_name == 'event':
        for name in ['subs', 'source', 'actor']:
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
        entity.linked_places = [location.get_linked_entity_safe('P53', True) for location
                                in entity.get_linked_entities(['P7', 'P26', 'P27'])]
    if entity.view_name in ['actor', 'event', 'node', 'place', 'source', 'object']:
        if entity.view_name not in ['node', 'reference']:
            tabs['reference'] = Tab('reference', entity)
        tabs['file'] = Tab('file', entity)
        entity.image_id = entity.get_profile_image_id()
        for link_ in entity.get_links('P67', inverse=True):
            domain = link_.domain
            data = get_base_table_data(domain)
            if domain.view_name == 'file':  # pragma: no cover
                extension = data[3]
                data.append(
                    get_profile_image_table_link(domain, entity, extension, entity.image_id))
                if not entity.image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    entity.image_id = domain.id
                if entity.view_name == 'place' and is_authorized('editor') and \
                        current_user.settings['module_map_overlay']:
                    tabs['file'].table.header.append(uc_first(_('overlay')))
                    overlays = Overlay.get_by_object(entity)
                    if extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                        if domain.id in overlays:
                            data = add_edit_link(data,
                                                 url_for('overlay_update',
                                                         id_=overlays[domain.id].id))
                        else:
                            data.append(link(_('link'), url_for('overlay_insert',
                                                                image_id=domain.id,
                                                                place_id=entity.id,
                                                                link_id=link_.id)))
                    else:  # pragma: no cover
                        data.append('')
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
    if not gis_data:
        gis_data = Gis.get_all(entity.linked_places) if entity.linked_places else None
    return render_template('entity/view.html',
                           entity=entity,
                           tabs=tabs,
                           buttons=add_buttons(entity),
                           structure=structure,  # Needed for place views
                           overlays=overlays,  # Needed for place views
                           gis_data=gis_data,
                           info=get_entity_data(entity, event_links=event_links),
                           title=entity.name,
                           crumbs=add_crumbs(entity, structure))


def add_crumbs(entity: Union[Entity, Node], structure: Optional[Dict[str, Any]]) -> List[str]:
    crumbs = [[_(entity.view_name.replace('_', ' ')),
               url_for('index', class_=entity.view_name)], entity.name]
    if structure:
        crumbs = [
            [_(entity.view_name).replace('_', ' '), url_for('index', class_=entity.view_name)],
            structure['place'],
            structure['feature'],
            structure['stratigraphic_unit'],
            entity.name]
    elif entity.view_name == 'node':
        crumbs = [[_('types'), url_for('node_index')]]
        if entity.root:
            for node_id in reversed(entity.root):
                crumbs += [g.nodes[node_id]]
        crumbs += [entity.name]
    elif entity.view_name == 'translation':
        crumbs = [[_('source'), url_for('index', class_='source')],
                  entity.get_linked_entity('P73', True),
                  entity.name]
    return crumbs


def add_buttons(entity: Union[Entity, Node, ReferenceSystem]) -> List[str]:
    buttons = []
    if entity.view_name == 'node':
        if is_authorized('editor') and entity.root and not g.nodes[entity.root[0]].locked:
            buttons.append(button(_('edit'), url_for('update', id_=entity.id)))
            if not entity.locked and entity.count < 1 and not entity.subs:
                buttons.append(display_delete_link(None, entity))
    elif entity.view_name == 'reference_system':
        if is_authorized('manager'):
            buttons.append(button(_('edit'), url_for('update', id_=entity.id)))
            if not entity.forms and not entity.system:
                buttons.append(display_delete_link(None, entity))
    elif entity.system_type == 'source translation':
        buttons.append(button(_('edit'), url_for('translation_update', id_=entity.id)))
        buttons.append(display_delete_link(None, entity))
    elif is_authorized('contributor'):
        buttons.append(button(_('edit'), url_for('update', id_=entity.id)))
        if entity.view_name != 'place' or not entity.get_linked_entities('P46'):
            buttons.append(display_delete_link(None, entity))
    return buttons


@app.route('/entity/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def entity_add_file(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-file')
    form = build_table_form('file', entity.get_linked_entities('P67', inverse=True))
    return render_template('form.html',
                           entity=entity,
                           form=form,
                           title=entity.name,
                           crumbs=[[_(entity.view_name), url_for('index', class_=entity.view_name)],
                                   entity,
                                   _('link') + ' ' + _('file')])


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
    return render_template('form.html',
                           form=form,
                           title=entity.name,
                           crumbs=[[_(entity.view_name), url_for('index', class_=entity.view_name)],
                                   entity,
                                   _('link') + ' ' + _('source')])


@app.route('/entity/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_reference(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    form = AddReferenceForm()
    if form.validate_on_submit():
        entity.link_string('P67', form.reference.data, description=form.page.data, inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-reference')
    form.page.label.text = uc_first(_('page / link text'))
    return render_template('display_form.html',
                           entity=entity,
                           form=form,
                           crumbs=[[_(entity.view_name), url_for('index', class_=entity.view_name)],
                                   entity,
                                   _('link') + ' ' + _('reference')])
