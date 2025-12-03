from __future__ import annotations

import mimetypes
from collections import defaultdict
from typing import Any, Optional

from flask import g, url_for

from openatlas import app
from openatlas.api.endpoints.parser import Parser
from openatlas.api.resources.util import (
    date_to_str, geometry_to_feature_collection, get_crm_relation_x,
    get_iiif_manifest_and_path, get_license_name, get_location_link,
    get_reference_systems, get_value_for_types, to_camel_case)
from openatlas.database.overlay import get_by_object
from openatlas.display.util import get_file_path
from openatlas.models.cidoc import CidocProperty
from openatlas.models.dates import Dates
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis
from openatlas.models.overlay import Overlay


def get_presentation_types(
        entity: Entity,
        links: list[Link]) -> list[dict[str, Any]]:
    types = []
    location_types = {}
    if entity.class_.group.get('name') == 'place':
        location_types = get_location_link(links).range.types
    for type_ in entity.types | location_types:
        is_standard = False
        if entity.standard_type:
            is_standard = entity.standard_type.id == type_.id
        type_dict = {
            'id': type_.id,
            'title': type_.name,
            'descriptions': type_.description,
            'isStandard': is_standard,
            'typeHierarchy': [{
                'label': g.types[root].name,
                'descriptions': g.types[root].description,
                'identifier': url_for(
                    'api.entity', id_=g.types[root].id, _external=True)}
                for root in type_.root]}
        type_dict.update(get_value_for_types(type_, links))
        types.append(type_dict)
    return types


def get_file_dict(
        link: Link,
        overlay: Optional[Overlay] = None,
        root: Optional[bool] = False) -> dict[str, str]:
    path = get_file_path(link.domain.id)
    mime_type = None
    if path:
        mime_type, _ = mimetypes.guess_type(path)  # pragma: no cover
    data = {
        'id': link.domain.id,
        'title': link.domain.name,
        'license': get_license_name(link.domain),
        'creator': link.domain.creator,
        'licenseHolder': link.domain.license_holder,
        'publicShareable': link.domain.public,
        'mimetype': mime_type,
        'fromSuperEntity': root,
        'url': url_for(
            'api.display',
            filename=path.stem,
            _external=True) if path else 'N/A'}
    data.update(get_iiif_manifest_and_path(link.domain.id))
    if overlay:
        data.update({'overlay': overlay.bounding_box})
    return data


def get_presentation_files(
        links_inverse: list[Link],
        entity: Entity,
        parser: Parser,
        root_ids: Optional[list[int]] = None) -> list[dict[str, str]]:
    files = []
    file_links = [
        link_ for link_ in links_inverse if link_.domain.class_.name == 'file']
    if not file_links:
        return []
    overlays = {
        row['image_id']: Overlay(row) for row
        in get_by_object([l.domain.id for l in file_links])}
    for link_ in file_links:
        if parser.place_hierarchy \
                and parser.map_overlay \
                and link_.range.id in root_ids:
            if overlay := overlays.get(link_.domain.id):
                files.append(get_file_dict(link_, overlay, root=True))
        elif link_.range.id == entity.id:
            files.append(
                get_file_dict(link_, overlays.get(link_.domain.id)))
        elif entity.class_.name == 'file' and link_.domain.id == entity.id:
            files.append(
                get_file_dict(link_, overlays.get(link_.domain.id)))
            break
    return files


def get_relation_types_dict(
        link_: Link,
        parser: Parser,
        entity_id: int,
        inverse: bool = False) -> dict[str, Any]:
    relation_to_id = link_.domain.id if inverse else link_.range.id
    if link_.property.code in ['P74', 'OA8', 'OA9', 'P7', 'P26', 'P27']:
        relation_to_id = entity_id
    relation_types = {
        'property': get_crm_relation_x(link_, inverse),
        'relationTo': relation_to_id,
        'type': to_camel_case(link_.type.name) if link_.type else None,
        'description': link_.description,
        'when': get_presentation_time(link_.dates)}
    if parser.remove_empty_values:
        relation_types = {k: v for k, v in relation_types.items() if v}
    return relation_types


def get_relation_types_dict_for_locations(
        entity_id: int,
        property_: CidocProperty,
        parser: Parser) -> dict[str, Any]:
    property_string = f"i_{property_.i18n_inverse['en'].replace(' ', '_')}"
    relation_types = {
        'property': f"crm:{property_.code}{property_string}",
        'relationTo': entity_id,
        'type': None,
        'description': None,
        'when': None}
    if parser.remove_empty_values:
        relation_types = {k: v for k, v in relation_types.items() if v}
    return relation_types


def get_presentation_references(
        links_inverse: list[Link],
        entity_ids: list[int]) -> list[dict[str, Any]]:
    references = []
    check_for_duplicates: dict[int, str] = defaultdict(str)
    for link in links_inverse:
        if link.domain.class_.group.get('name') != 'reference' \
                or link.range.id not in entity_ids \
                or check_for_duplicates[link.domain.id] == link.description:
            continue
        ref = {
            'id': link.domain.id,
            'systemClass': link.domain.class_.name,
            'title': link.domain.name,
            'citation': link.domain.description,
            'pages': link.description}
        if link.domain.standard_type:
            ref.update({
                'type': link.domain.standard_type.name,
                'typeId': link.domain.standard_type.id})
        check_for_duplicates[link.domain.id] = link.description
        references.append(ref)
    return references


def get_presentation_view(entity: Entity, parser: Parser) -> dict[str, Any]:
    ids = [entity.id]
    root_ids: list[int] = []
    if entity.class_.group.get('name') in ['place', 'artifact']:
        entity.location = entity.get_linked_entity_safe('P53')
        ids.append(entity.location.id)
        if parser.place_hierarchy:
            root_ids = Entity.get_linked_entity_ids_recursive(
                entity.id,
                'P46',
                inverse=True)
            root_id = root_ids[-1] if root_ids else entity.id
            place_hierarchy = Entity.get_linked_entity_ids_recursive(
                root_id,
                'P46')
            place_hierarchy.extend(root_ids)
            ids.extend(place_hierarchy)

    links = Entity.get_links_of_entities(ids)
    links_inverse = Entity.get_links_of_entities(ids, inverse=True)
    if entity.class_.group.get('name') == 'event':
        event_ids = [
            l.range.id for l in links
            if l.domain.class_.group.get('name') == 'event']
    else:
        event_ids = [
            l.domain.id for l in links_inverse
            if l.domain.class_.group.get('name') == 'event']
    event_links = []
    if event_ids:
        event_links = Entity.get_links_of_entities(
            event_ids,
            ['P7', 'P11', 'P14', 'P22', 'P23', 'P24', 'P25', 'P26', 'P27',
             'P31', 'P108', 'P134', 'P9'])

    excluded = app.config['API_PRESENTATION_EXCLUDE_RELATION']

    related_entities: list[Entity] = []
    exists: set[int] = set()
    relation_types = defaultdict(list)
    for l in links + event_links:
        if (l.range.class_.name in excluded
                or l.range.id in exists
                or l.range.id == entity.id):
            continue
        related_entities.append(l.range)
        relation_types[l.range.id].append(
            get_relation_types_dict(l, parser, entity.id, True))
    for l in links_inverse:
        if (l.domain.class_.name in excluded
                or l.domain.id in exists
                or l.domain.id == entity.id):
            continue
        related_entities.append(l.domain)
        relation_types[l.domain.id].append(
            get_relation_types_dict(l, parser, entity.id))

    places: list[Entity] = []
    if entity.class_.group.get('name') in ['actor', 'event']:
        if location_links := Entity.get_links_of_entities(
                entity.id,
                ['P74', 'OA8', 'OA9', 'P7', 'P26', 'P27']):
            property_mapping = {}
            location_ids = []
            for link_ in location_links:
                property_mapping[link_.range.id] = link_.property
                location_ids.append(link_.range.id)
            for link_ in Entity.get_links_of_entities(
                    location_ids,
                    'P53',
                    inverse=True):
                places.append(link_.domain)
                relation_types[link_.domain.id].append(
                    get_relation_types_dict_for_locations(
                        entity.id,
                        property_mapping[link_.range.id],
                        parser))

    related_entities = related_entities + places
    exists_: set[int] = set()
    add_ = exists_.add  # Faster than always call exists.add()
    related_entities_ = \
        [e for e in related_entities if not (e.id in exists_ or add_(e.id))]

    all_entities = related_entities_ + [entity]
    geoms = Gis.get_by_entities(all_entities)
    if parser.centroid:
        for id_, geom in \
                Gis.get_centroids_by_entities(all_entities).items():
            geoms[id_].extend(geom)
    relations = defaultdict(list)
    for rel_entity in related_entities_:
        standard_type_ = {}
        if rel_entity.standard_type:
            standard_type_ = {
                'id': rel_entity.standard_type.id,
                'title': rel_entity.standard_type.name}
        geometries = geometry_to_feature_collection(geoms.get(rel_entity.id))
        relation_dict = {
            'id': rel_entity.id,
            'systemClass': rel_entity.class_.name,
            'viewClass': rel_entity.class_.group.get('name'),
            'title': rel_entity.name,
            'description': rel_entity.description,
            'aliases': list(rel_entity.aliases.values()),
            'geometries': geometries,
            'when': get_presentation_time(rel_entity.dates),
            'standardType': standard_type_,
            'relationTypes': relation_types[rel_entity.id]}
        if parser.remove_empty_values:
            relation_dict = {k: v for k, v in relation_dict.items() if v}
        relations[rel_entity.class_.name].append(relation_dict)

    data = {
        'id': entity.id,
        'systemClass': entity.class_.name,
        'viewClass': entity.class_.group.get('name'),
        'title': entity.name,
        'description': entity.get_annotated_text()
        if entity.class_.name == 'source' else entity.description,
        'aliases': list(entity.aliases.values()),
        'geometries': None,
        'when': get_presentation_time(entity.dates),
        'types': get_presentation_types(entity, links),
        'externalReferenceSystems': get_reference_systems(links_inverse),
        'references': get_presentation_references(
            links_inverse,
            [entity.id, *root_ids]),
        'files': get_presentation_files(
            links if entity.class_.name == 'file' else links_inverse,
            entity,
            parser,
            root_ids),
        'relations': relations}
    if entity.class_.group.get('name') in ['place', 'artifact']:
        data['geometries'] = geometry_to_feature_collection(
            geoms.get(entity.id))

    return data


def get_presentation_time(dates: Dates) -> Optional[dict[str, Any]]:
    time = {}
    if dates.begin_from or dates.begin_to:
        begin = {
            'earliest': date_to_str(dates.begin_from),
            'latest': date_to_str(dates.begin_to),
            'comment': dates.begin_comment}
        time['start'] = {k: v for k, v in begin.items() if v}
    if dates.end_from or dates.end_to:
        end = {
            'earliest': date_to_str(dates.end_from),
            'latest': date_to_str(dates.end_to),
            'comment': dates.end_comment}
        time['end'] = {k: v for k, v in end.items() if v}
    return time
