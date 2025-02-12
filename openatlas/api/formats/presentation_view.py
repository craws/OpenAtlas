import mimetypes
from collections import defaultdict
from typing import Any

from flask import g, url_for

from openatlas import app
from openatlas.api.endpoints.parser import Parser
from openatlas.api.formats.linked_places import get_lp_time
from openatlas.api.resources.util import (
    get_crm_relation_x, get_geojson_geometries, get_geometric_collection,
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
    if entity.class_.view in ['place', 'artifact']:
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


def get_presentation_files(links_inverse: list[Link]) -> list[dict[str, str]]:
    files = []
    for link in links_inverse:
        if link.domain.class_.name != 'file':
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
        link_: Link, inverse: bool = False) -> dict[str, Any]:
    return {
        'property': get_crm_relation_x(link_, inverse),
        'relationTo': link_.domain.id if inverse else link_.range.id,
        'type': to_camel_case(link_.type.name) if link_.type else None,
        'description': link_.description,
        'when': get_lp_time(link_)}


def get_presentation_view(entity: Entity, parser: Parser) -> dict[str, Any]:
    ids = [entity.id ]
    if entity.class_.view in ['place', 'artifact']:
        entity.location = entity.get_linked_entity_safe('P53')
        ids.append(entity.location.id)

    links = Entity.get_links_of_entities(ids)
    links_inverse = Entity.get_links_of_entities(ids, inverse=True)
    event_ids = [
        l.domain.id for l in links_inverse if l.domain.class_.view == 'event']
    event_links = []
    if event_ids:
        event_links = Entity.get_links_of_entities(
            event_ids,
            ['P7', 'P11', 'P14', 'P22', 'P23', 'P24', 'P25', 'P26', 'P27',
             'P31', 'P108'])

    excluded = app.config['API_PRESENTATION_EXCLUDE_RELATION']

    related_entities = []
    exists: set[int] = set()
    geometric_entities = []
    relation_types = defaultdict(list)
    for l in links + event_links:
        if l.range.class_.name in excluded or l.range.id in exists:
            continue
        if l.range.class_.view in ['place', 'artifact']:
            geometric_entities.append(l.range.id)
        related_entities.append(l.range)
        relation_types[l.range.id].append(get_relation_types_dict(l, True))
    for l in links_inverse:
        if l.domain.class_.name in excluded or l.domain.id in exists:
            continue
        if l.domain.class_.view in ['place', 'artifact']:
            geometric_entities.append(l.domain.id)
        related_entities.append(l.domain)
        relation_types[l.domain.id].append(get_relation_types_dict(l))

    geoms = {}
    if geometric_entities:
        geoms = Gis.get_by_place_ids(geometric_entities)

    relations = defaultdict(list)
    for rel_entity in related_entities:
        standard_type = {}
        if rel_entity.standard_type:
            standard_type =  {
                'id': rel_entity.standard_type.id,
                'title': rel_entity.standard_type.name}
        geometries = {}
        if geoms.get(rel_entity.id):
            geometries = get_geojson_geometries(geoms[rel_entity.id])
        relations[rel_entity.class_.name].append({
            'id': rel_entity.id,
            'systemClass': rel_entity.class_.name,
            'title': rel_entity.name,
            'description': rel_entity.description,
            'aliases': list(rel_entity.aliases.values()),
            'geometries': geometries,
            'when': get_lp_time(rel_entity),
            'standardType': standard_type,
            'relationTypes': relation_types[rel_entity.id]})

    data = {
        'id': entity.id,
        'systemClass': entity.class_.name,
        'title': entity.name,
        'description': entity.description,
        'aliases': list(entity.aliases.values()),
        'geometries': get_geometric_collection(entity, links, parser),
        'when': get_lp_time(entity),
        'types': get_presentation_types(entity, links),
        'externalReferenceSystems': get_reference_systems(links_inverse),
        'files': get_presentation_files(links_inverse),
        'relations': relations}

    return data
