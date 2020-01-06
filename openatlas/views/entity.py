import os
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

from flask import flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.models.entity import Entity, EntityMapper
from openatlas.models.gis import GisMapper
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.models.overlay import Overlay
from openatlas.models.user import User
from openatlas.util.table import Table
from openatlas.util.util import (add_system_data, add_type_data, display_remove_link,
                                 format_entry_begin, format_entry_end, get_appearance,
                                 get_base_table_data, get_entity_data, get_file_path,
                                 get_profile_image_table_link, is_authorized, link, required_group,
                                 truncate_string, uc_first)
from openatlas.views.file import preview_file


@app.route('/entity/<int:id_>')
@required_group('readonly')
def entity_view(id_: int) -> Union[str, Response]:
    if id_ in g.nodes:
        if g.nodes[id_].root:
            return node_view(g.nodes[id_])
        else:
            return redirect(url_for('node_index') + '#tab-' + str(id_))
    entity = EntityMapper.get_by_id(id_, nodes=True, aliases=True)
    if not entity.view_name:  # pragma: no cover
        flash(_("This entity can't be viewed directly"), 'error')
        abort(400)
    return getattr(sys.modules[__name__], '{name}_view'.format(name=entity.view_name))(entity)


def actor_view(actor: Entity) -> str:
    actor.note = User.get_note(actor)
    info: List[Tuple[Any, Optional[str]]] = []
    if actor.aliases:
        info.append((uc_first(_('alias')), '<br>'.join(actor.aliases.values())))
    tables = {'file': Table(Table.HEADERS['file'] + [_('main image')]),
              'source': Table(Table.HEADERS['source']),
              'reference': Table(Table.HEADERS['reference'] + ['page / link text']),
              'event': Table(['event', 'class', 'involvement', 'first', 'last', 'description'],
                             defs='[{className: "dt-body-right", targets: [3,4]}]'),
              'relation': Table(['relation', 'actor', 'first', 'last', 'description'],
                                defs='[{className: "dt-body-right", targets: [2,3]}]'),
              'member_of': Table(['member of', 'function', 'first', 'last', 'description'],
                                 defs='[{className: "dt-body-right", targets: [2,3]}]')}
    profile_image_id = actor.get_profile_image_id()
    for link_ in actor.get_links('P67', True):
        domain = link_.domain
        data_ = get_base_table_data(domain)
        if domain.view_name == 'file':
            extension = data_[3].replace('.', '')
            data_.append(
                get_profile_image_table_link(domain, actor, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['source', 'file']:
            data_.append(truncate_string(link_.description))
            if domain.system_type == 'external reference':
                actor.external_references.append(link_)
            if is_authorized('contributor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=actor.id)
                data_.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=actor.id)
            data_.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name].rows.append(data_)

    # Todo: Performance - getting every place of every object for every event is very costly
    event_links = actor.get_links(['P11', 'P14', 'P22', 'P23', 'P25'], True)

    objects = []
    for link_ in event_links:
        event = link_.domain
        places = event.get_linked_entities(['P7', 'P26', 'P27'])
        link_.object_ = None
        for place in places:
            object_ = place.get_linked_entity_safe('P53', True)
            objects.append(object_)
            link_.object_ = object_  # Needed later for first/last appearance info
        first = link_.first
        if not link_.first and event.first:
            first = '<span class="inactive" style="float:right;">' + event.first + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive" style="float:right;">' + event.last + '</span>'
        data = ([link(event),
                 g.classes[event.class_.code].name,
                 link_.type.name if link_.type else '',
                 first,
                 last,
                 truncate_string(link_.description)])
        if is_authorized('contributor'):
            update_url = url_for('involvement_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=actor.id) + '#tab-event'
            if link_.domain.class_.code != 'E9':
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            else:
                data.append('')
            data.append(display_remove_link(unlink_url, link_.domain.name))
        tables['event'].rows.append(data)

    # Add info of dates and places
    begin_place = actor.get_linked_entity('OA8')
    begin_object = None
    if begin_place:
        begin_object = begin_place.get_linked_entity_safe('P53', True)
        objects.append(begin_object)
    end_place = actor.get_linked_entity('OA9')
    end_object = None
    if end_place:
        end_object = end_place.get_linked_entity_safe('P53', True)
        objects.append(end_object)
    label = uc_first(_('born') if actor.class_.code == 'E21' else _('begin'))
    info.append((label, format_entry_begin(actor, begin_object)))
    label = uc_first(_('died') if actor.class_.code == 'E21' else _('end'))
    info.append((label, format_entry_end(actor, end_object)))
    appears_first, appears_last = get_appearance(event_links)
    info.append((_('appears first'), appears_first))
    info.append((_('appears last'), appears_last))

    residence_place = actor.get_linked_entity('P74')
    if residence_place:
        residence_object = residence_place.get_linked_entity_safe('P53', True)
        objects.append(residence_object)
        info.append((uc_first(_('residence')), link(residence_object)))
    add_type_data(actor, info)
    add_system_data(actor, info)

    for link_ in actor.get_links('OA7') + actor.get_links('OA7', True):
        if actor.id == link_.domain.id:
            type_ = link_.type.get_name_directed() if link_.type else ''
            related = link_.range
        else:
            type_ = link_.type.get_name_directed(True) if link_.type else ''
            related = link_.domain
        data = (
            [type_, link(related), link_.first, link_.last, truncate_string(link_.description)])
        if is_authorized('contributor'):
            update_url = url_for('relation_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=actor.id) + '#tab-relation'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, related.name))
        tables['relation'].rows.append(data)
    for link_ in actor.get_links('P107', True):
        data = ([link(link_.domain), link_.type.name if link_.type else '',
                 link_.first, link_.last, truncate_string(link_.description)])
        if is_authorized('contributor'):
            update_url = url_for('member_update', id_=link_.id, origin_id=actor.id)
            unlink_url = url_for('link_delete', id_=link_.id,
                                 origin_id=actor.id) + '#tab-member-of'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, link_.domain.name))
        tables['member_of'].rows.append(data)
    if actor.class_.code in app.config['CLASS_CODES']['group']:
        tables['member'] = Table(['member', 'function', 'first', 'last', 'description'],
                                 defs='[{className: "dt-body-right", targets: [2,3]}]')
        for link_ in actor.get_links('P107'):
            data = ([link(link_.range), link_.type.name if link_.type else '',
                     link_.first, link_.last, truncate_string(link_.description)])
            if is_authorized('contributor'):
                update_url = url_for('member_update', id_=link_.id, origin_id=actor.id)
                unlink_url = url_for('link_delete', id_=link_.id,
                                     origin_id=actor.id) + '#tab-member'
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
                data.append(display_remove_link(unlink_url, link_.range.name))
            tables['member'].rows.append(data)
    gis_data = GisMapper.get_all(objects) if objects else None
    if gis_data:
        if gis_data['gisPointSelected'] == '[]' and gis_data['gisPolygonSelected'] == '[]':
            gis_data = None
    return render_template('actor/view.html', actor=actor, info=info, tables=tables,
                           gis_data=gis_data, profile_image_id=profile_image_id)


def event_view(event: Entity) -> str:
    event.note = User.get_note(event)
    tables = {'file': Table(Table.HEADERS['file'] + [_('main image')]),
              'subs': Table(Table.HEADERS['event']),
              'source': Table(Table.HEADERS['source']),
              'actor': Table(['actor', 'class', 'involvement', 'first', 'last', 'description'],
                             defs='[{className: "dt-body-right", targets: [3,4]}]'),
              'reference': Table(Table.HEADERS['reference'] + ['page / link text'])}
    for link_ in event.get_links(['P11', 'P14', 'P22', 'P23']):
        first = link_.first
        if not link_.first and event.first:
            first = '<span class="inactive" style="float:right;">' + event.first + '</span>'
        last = link_.last
        if not link_.last and event.last:
            last = '<span class="inactive" style="float:right;">' + event.last + '</span>'
        data = ([link(link_.range),
                 g.classes[link_.range.class_.code].name,
                 link_.type.name if link_.type else '',
                 first, last,
                 truncate_string(link_.description)])
        if is_authorized('contributor'):
            update_url = url_for('involvement_update', id_=link_.id, origin_id=event.id)
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=event.id) + '#tab-actor'
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            data.append(display_remove_link(unlink_url, link_.range.name))
        tables['actor'].rows.append(data)
    profile_image_id = event.get_profile_image_id()
    for link_ in event.get_links('P67', True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':
            extension = data[3].replace('.', '')
            data.append(get_profile_image_table_link(domain, event, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['source', 'file']:
            if domain.system_type == 'external reference':
                event.external_references.append(link_)
            data.append(truncate_string(link_.description))
            if is_authorized('contributor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=event.id)
                data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=event.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name].rows.append(data)
    for sub_event in event.get_linked_entities('P117', inverse=True, nodes=True):
        tables['subs'].rows.append(get_base_table_data(sub_event))
    objects = []
    for location in event.get_linked_entities(['P7', 'P26', 'P27']):
        objects.append(location.get_linked_entity_safe('P53', True))
    return render_template('event/view.html', event=event, tables=tables,
                           info=get_entity_data(event), profile_image_id=profile_image_id,
                           gis_data=GisMapper.get_all(objects) if objects else None)


def file_view(file: Entity) -> str:
    path = get_file_path(file.id)
    tables = {}
    for name in ['source', 'event', 'actor', 'place', 'feature', 'stratigraphic-unit', 'find',
                 'reference']:
        tables[name] = Table(Table.HEADERS[name] + (['page'] if name == 'reference' else []))
    for link_ in file.get_links('P67'):
        range_ = link_.range
        data = get_base_table_data(range_)
        view_name = range_.view_name
        view_name = view_name if view_name != 'place' else range_.system_type.replace(' ', '-')
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=file.id)
            data.append(display_remove_link(url + '#tab-' + view_name, range_.name))
        tables[view_name].rows.append(data)
    for link_ in file.get_links('P67', True):
        data = get_base_table_data(link_.domain)
        data.append(link_.description)
        if is_authorized('contributor'):
            update_url = url_for('reference_link_update', link_id=link_.id, origin_id=file.id)
            data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
            unlink_url = url_for('link_delete', id_=link_.id, origin_id=file.id)
            data.append(display_remove_link(unlink_url + '#tab-reference', link_.domain.name))
        tables['reference'].rows.append(data)
    return render_template('file/view.html', missing_file=False if path else True, entity=file,
                           info=get_entity_data(file), tables=tables,
                           preview=True if path and preview_file(path) else False,
                           filename=os.path.basename(path) if path else False)


def object_view(object_: Entity) -> str:
    object_.note = User.get_note(object_)
    tables = {'source': Table(Table.HEADERS['source']), 'event': Table(Table.HEADERS['event'])}
    for link_ in object_.get_links('P128'):
        data = get_base_table_data(link_.range)
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=object_.id)
            data.append(
                display_remove_link(url + '#tab-' + link_.range.table_name, link_.range.name))
        tables['source'].rows.append(data)
    for link_ in object_.get_links('P25', inverse=True):
        data = get_base_table_data(link_.domain)
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=object_.id)
            data.append(
                display_remove_link(url + '#tab-' + link_.range.table_name, link_.range.name))
        tables['event'].rows.append(data)
    return render_template('object/view.html', object_=object_, tables=tables,
                           info=get_entity_data(object_))


def place_view(object_: Entity) -> str:
    object_.note = User.get_note(object_)
    location = object_.get_linked_entity_safe('P53', nodes=True)
    tables = {'file': Table(Table.HEADERS['file'] + [_('main image')]),
              'source': Table(Table.HEADERS['source']),
              'event': Table(Table.HEADERS['event'],
                             defs='[{className: "dt-body-right", targets: [3,4]}]'),
              'reference': Table(Table.HEADERS['reference'] + ['page / link text']),
              'actor': Table([_('actor'), _('property'), _('class'), _('first'), _('last')])}
    if object_.system_type == 'place':
        tables['feature'] = Table(Table.HEADERS['place'] + [_('description')])
    if object_.system_type == 'feature':
        tables['stratigraphic-unit'] = Table(Table.HEADERS['place'] + [_('description')])
    if object_.system_type == 'stratigraphic unit':
        tables['find'] = Table(Table.HEADERS['place'] + [_('description')])
    profile_image_id = object_.get_profile_image_id()
    overlays: Dict[int, Overlay] = {}
    if current_user.settings['module_map_overlay']:
        overlays = Overlay.get_by_object(object_)
        if is_authorized('editor'):
            tables['file'].header.append(uc_first(_('overlay')))

    for link_ in object_.get_links('P67', inverse=True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':
            extension = data[3].replace('.', '')
            data.append(get_profile_image_table_link(domain, object_, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
            if is_authorized('editor') and current_user.settings['module_map_overlay']:
                if extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    if domain.id in overlays:
                        url = url_for('overlay_update', id_=overlays[domain.id].id)
                        data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
                    else:
                        url = url_for('overlay_insert', image_id=domain.id, place_id=object_.id,
                                      link_id=link_.id)
                        data.append('<a href="' + url + '">' + uc_first(_('add')) + '</a>')
                else:  # pragma: no cover
                    data.append('')
        if domain.view_name not in ['source', 'file']:
            data.append(truncate_string(link_.description))
            if domain.system_type.startswith('external reference'):
                object_.external_references.append(link_)
            if is_authorized('contributor') and domain.system_type != 'external reference geonames':
                url = url_for('reference_link_update', link_id=link_.id, origin_id=object_.id)
                data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
            else:
                data.append('')
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=object_.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name].rows.append(data)
    event_ids = []  # Keep track of already inserted events to prevent doubles
    for event in location.get_linked_entities(['P7', 'P26', 'P27'], inverse=True):
        tables['event'].rows.append(get_base_table_data(event))
        event_ids.append(event.id)
    for event in object_.get_linked_entities('P24', inverse=True):
        if event.id not in event_ids:  # Don't add again if already in table
            tables['event'].rows.append(get_base_table_data(event))
    has_subunits = False
    for entity in object_.get_linked_entities('P46', nodes=True):
        has_subunits = True
        data = get_base_table_data(entity)
        data.append(truncate_string(entity.description))
        tables[entity.system_type.replace(' ', '-')].rows.append(data)
    for link_ in location.get_links(['P74', 'OA8', 'OA9'], inverse=True):
        actor = EntityMapper.get_by_id(link_.domain.id, view_name='actor')
        tables['actor'].rows.append([link(actor),
                                     g.properties[link_.property.code].name,
                                     actor.class_.name,
                                     actor.first,
                                     actor.last])
    gis_data: Dict[str, List[Any]] = GisMapper.get_all([object_])
    if gis_data['gisPointSelected'] == '[]' and gis_data['gisPolygonSelected'] == '[]' \
            and gis_data['gisLineSelected'] == '[]':
        gis_data = {}
    place = None
    feature = None
    stratigraphic_unit = None
    if object_.system_type == 'find':
        stratigraphic_unit = object_.get_linked_entity_safe('P46', True)
        feature = stratigraphic_unit.get_linked_entity_safe('P46', True)
        place = feature.get_linked_entity_safe('P46', True)
    elif object_.system_type == 'stratigraphic unit':
        feature = object_.get_linked_entity_safe('P46', True)
        place = feature.get_linked_entity_safe('P46', True)
    elif object_.system_type == 'feature':
        place = object_.get_linked_entity_safe('P46', True)
    return render_template('place/view.html', object_=object_, tables=tables, overlays=overlays,
                           info=get_entity_data(object_, location), gis_data=gis_data,
                           place=place, feature=feature, stratigraphic_unit=stratigraphic_unit,
                           has_subunits=has_subunits, profile_image_id=profile_image_id)


def reference_view(reference: Entity) -> str:
    reference.note = User.get_note(reference)
    tables = {'file': Table(Table.HEADERS['file'] + ['page', _('main image')])}
    for name in ['source', 'event', 'actor', 'place', 'feature', 'stratigraphic-unit', 'find']:
        header_label = 'link text' if reference.system_type == 'external reference' else 'page'
        tables[name] = Table(Table.HEADERS[name] + [header_label])
    for link_ in reference.get_links('P67', True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=reference.id) + '#tab-file'
            data.append(display_remove_link(url, domain.name))
        tables['file'].rows.append(data)
    profile_image_id = reference.get_profile_image_id()
    for link_ in reference.get_links(['P67', 'P128']):
        range_ = link_.range
        data = get_base_table_data(range_)
        data.append(truncate_string(link_.description))
        if range_.view_name == 'file':  # pragma: no cover
            ext = data[3].replace('.', '')
            data.append(get_profile_image_table_link(range_, reference, ext, profile_image_id))
        if is_authorized('contributor'):
            url = url_for('reference_link_update', link_id=link_.id, origin_id=reference.id)
            data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
            url = url_for('link_delete', id_=link_.id, origin_id=reference.id)
            data.append(display_remove_link(url + '#tab-' + range_.table_name, range_.name))
        tables[range_.table_name].rows.append(data)
    return render_template('reference/view.html', reference=reference, tables=tables,
                           info=get_entity_data(reference), profile_image_id=profile_image_id)


def source_view(source: Entity) -> str:
    source.note = User.get_note(source)
    tables = {'text': Table(['text', 'type', 'content']),
              'file': Table(Table.HEADERS['file'] + [_('main image')]),
              'reference': Table(Table.HEADERS['reference'] + ['page'])}
    for text in source.get_linked_entities('P73', nodes=True):
        tables['text'].rows.append([link(text),
                                    next(iter(text.nodes)).name if text.nodes else '',
                                    truncate_string(text.description)])
    for name in ['actor', 'event', 'place', 'feature', 'stratigraphic-unit', 'find']:
        tables[name] = Table(Table.HEADERS[name])
    tables['actor'].defs = '[{className: "dt-body-right", targets: [2,3]}]'
    tables['event'].defs = '[{className: "dt-body-right", targets: [3,4]}]'
    tables['place'].defs = '[{className: "dt-body-right", targets: [2,3]}]'
    for link_ in source.get_links('P67'):
        range_ = link_.range
        data = get_base_table_data(range_)
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=source.id)
            data.append(display_remove_link(url + '#tab-' + range_.table_name, range_.name))
        tables[range_.table_name].rows.append(data)
    profile_image_id = source.get_profile_image_id()
    for link_ in source.get_links('P67', True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':  # pragma: no cover
            extension = data[3].replace('.', '')
            data.append(get_profile_image_table_link(domain, source, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['file']:
            data.append(link_.description)
            if domain.system_type == 'external reference':
                source.external_references.append(link_)
            if is_authorized('contributor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=source.id)
                data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=source.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name].rows.append(data)
    return render_template('source/view.html', source=source, tables=tables,
                           info=get_entity_data(source), profile_image_id=profile_image_id)


def node_view(node: Node) -> str:
    root = g.nodes[node.root[-1]] if node.root else None
    super_ = g.nodes[node.root[0]] if node.root else None
    header = [_('name'), _('class'), _('info')]
    if root and root.value_type:  # pragma: no cover
        header = [_('name'), _('value'), _('class'), _('info')]
    tables = {'entities': Table(header)}
    for entity in node.get_linked_entities(['P2', 'P89'], inverse=True, nodes=True):
        if not node.class_.code == 'E55':  # Get the object if it's a location
            entity = entity.get_linked_entity_safe('P53', True)  # pragma: no cover
        if entity:  # If not entity it is a place node, so do not add
            data = [link(entity)]
            if root and root.value_type:  # pragma: no cover
                data.append(format_number(entity.nodes[node]))
            data.append(g.classes[entity.class_.code].name)
            data.append(truncate_string(entity.description))
            tables['entities'].rows.append(data)
    tables['link_entities'] = Table([_('domain'), _('range')])
    for row in Link.get_entities_by_node(node):
        tables['link_entities'].rows.append([link(EntityMapper.get_by_id(row.domain_id)),
                                             link(EntityMapper.get_by_id(row.range_id))])
    tables['subs'] = Table([_('name'), _('count'), _('info')])
    for sub_id in node.subs:
        sub = g.nodes[sub_id]
        tables['subs'].rows.append([link(sub), sub.count, truncate_string(sub.description)])
    return render_template('types/view.html', node=node, super_=super_, tables=tables, root=root,
                           info=get_entity_data(node))


def translation_view(translation: Entity) -> str:
    return render_template('translation/view.html', info=get_entity_data(translation),
                           source=translation.get_linked_entity('P73', True),
                           translation=translation, )
