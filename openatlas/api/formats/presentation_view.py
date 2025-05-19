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
from openatlas.display.util import get_file_path
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis


def get_presentation_types(
        entity: Entity,
        links: list[Link]) -> list[dict[str, Any]]:
    types = []
    location_types = {}
    if entity.class_.view == 'place':
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


def get_presentation_files(
        links_inverse: list[Link],
        entity_id: int) -> list[dict[str, str]]:
    files = []
    for link in links_inverse:
        if link.domain.class_.name != 'file' or link.range.id != entity_id:
            continue
        img_id = link.domain.id
        path = get_file_path(img_id)
        mime_type = None
        if path:
            mime_type, _ = mimetypes.guess_type(path)  # pragma: no cover
        data = {
            'id': img_id,
            'title': link.domain.name,
            'license': get_license_name(link.domain),
            'creator': link.domain.creator,
            'licenseHolder': link.domain.license_holder,
            'publicShareable': link.domain.public,
            'mimetype': mime_type,
            'url': url_for(
                'api.display',
                filename=path.stem,
                _external=True) if path else 'N/A'}
        data.update(get_iiif_manifest_and_path(img_id))
        files.append(data)
    return files


def get_relation_types_dict(
        link_: Link,
        parser: Parser,
        inverse: bool = False) -> dict[str, Any]:
    relation_types = {
        'property': get_crm_relation_x(link_, inverse),
        'relationTo': link_.domain.id if inverse else link_.range.id,
        'type': to_camel_case(link_.type.name) if link_.type else None,
        'description': link_.description,
        'when': get_presentation_time(link_)}
    if parser.remove_empty_values:
        relation_types = {k: v for k, v in relation_types.items() if v}
    return relation_types


def get_presentation_references(
        links_inverse: list[Link],
        entity_id: int) -> list[dict[str, Any]]:
    references = []
    for link in links_inverse:
        if (link.domain.class_.view != 'reference'
                or link.range.id != entity_id):
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
        references.append(ref)
    return references


def get_presentation_view(entity: Entity, parser: Parser) -> dict[str, Any]:
    ids = [entity.id]
    if entity.class_.view in ['place', 'artifact']:
        entity.location = entity.get_linked_entity_safe('P53')
        ids.append(entity.location.id)
        if parser.place_hierarchy:
            place_hierarchy = entity.get_linked_entity_ids_recursive('P46')
            place_hierarchy.extend(entity.get_linked_entity_ids_recursive(
                'P46',
                inverse=True))
            ids.extend(place_hierarchy)

    links = Entity.get_links_of_entities(ids)
    links_inverse = Entity.get_links_of_entities(ids, inverse=True)
    if entity.class_.view == 'event':
        event_ids = [
            l.range.id for l in links if l.domain.class_.view == 'event']
    else:
        event_ids = [
            l.domain.id for l in links_inverse
            if l.domain.class_.view == 'event']
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
            get_relation_types_dict(l, parser, True))
    for l in links_inverse:
        if (l.domain.class_.name in excluded
                or l.domain.id in exists
                or l.domain.id == entity.id):
            continue
        related_entities.append(l.domain)
        relation_types[l.domain.id].append(get_relation_types_dict(l, parser))

    exists_: set[int] = set()
    add_ = exists_.add  # Faster than always call exists.add()
    related_entities_ = \
        [e for e in related_entities if not (e.id in exists_ or add_(e.id))]

    geoms = Gis.get_by_entities(related_entities_ + [entity])
    relations = defaultdict(list)
    for rel_entity in related_entities_:
        standard_type_ = {}
        if rel_entity.standard_type:
            standard_type_ = {
                'id': rel_entity.standard_type.id,
                'title': rel_entity.standard_type.name}

        relation_dict = {
            'id': rel_entity.id,
            'systemClass': rel_entity.class_.name,
            'viewClass': rel_entity.class_.view,
            'title': rel_entity.name,
            'description': rel_entity.description,
            'aliases': list(rel_entity.aliases.values()),
            'geometries': geometry_to_feature_collection(
                geoms.get(rel_entity.id)),
            'when': get_presentation_time(rel_entity),
            'standardType': standard_type_,
            'relationTypes': relation_types[rel_entity.id]}
        if parser.remove_empty_values:
            relation_dict = {k: v for k, v in relation_dict.items() if v}

        relations[rel_entity.class_.name].append(relation_dict)

    data = {
        'id': entity.id,
        'systemClass': entity.class_.name,
        'viewClass': entity.class_.view,
        'title': entity.name,
        'description': entity.description,
        'aliases': list(entity.aliases.values()),
        'geometries': geometry_to_feature_collection(geoms.get(entity.id)),
        'when': get_presentation_time(entity),
        'types': get_presentation_types(entity, links),
        'externalReferenceSystems': get_reference_systems(links_inverse),
        'references': get_presentation_references(links_inverse, entity.id),
        'files': get_presentation_files(links_inverse, entity.id),
        'relations': relations}
    return data


def get_presentation_time(entity: Entity | Link) -> Optional[dict[str, Any]]:
    dates = {}
    if entity.begin_from or entity.begin_to:
        begin = {
            'earliest': date_to_str(entity.begin_from),
            'latest': date_to_str(entity.begin_to),
            'comment': entity.begin_comment}
        dates['start'] = {k: v for k, v in begin.items() if v}
    if entity.end_from or entity.end_to:
        end = {
            'earliest': date_to_str(entity.end_from),
            'latest': date_to_str(entity.end_to),
            'comment': entity.end_comment}
        dates['end'] = {k: v for k, v in end.items() if v}
    return dates
