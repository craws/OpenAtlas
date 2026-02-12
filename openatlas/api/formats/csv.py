import zipfile
from collections import defaultdict
from io import BytesIO
from itertools import groupby
from typing import Any

import pandas as pd
from flask import Response, g
from shapely import GeometryCollection
from shapely.geometry import shape

from openatlas.models.entity import Entity, Link
from openatlas.models.gis import get_gis_by_id


def build_dataframe(entity: Entity) -> dict[str, Any]:
    return {
        'id': str(entity.id),
        'name': entity.name,
        'description': entity.description,
        'begin_from': entity.dates.begin_from,
        'begin_to': entity.dates.begin_to,
        'begin_comment': entity.dates.begin_comment,
        'end_from': entity.dates.end_from,
        'end_to': entity.dates.end_to,
        'end_comment': entity.dates.end_comment,
        'cidoc_class': entity.cidoc_class.name,
        'system_class': entity.class_.name,
        'coordinates': get_csv_geom_entry(entity)}


def build_link_dataframe(link: Link) -> dict[str, Any]:
    return {
        'id': link.id,
        'range_id': link.range.id,
        'range_name': link.range.name,
        'domain_id': link.domain.id,
        'domain_name': link.domain.name,
        'description': link.description,
        'begin_from': link.dates.begin_from,
        'begin_to': link.dates.begin_to,
        'begin_comment': link.dates.begin_comment,
        'end_from': link.dates.end_from,
        'end_to': link.dates.end_to,
        'end_comment': link.dates.end_comment}


def get_csv_types(entity_dict: dict[str, Any]) -> dict[Any, list[Any]]:
    types: dict[str, Any] = defaultdict(list)
    for type_ in entity_dict['entity'].types:
        hierarchy = [g.types[root].name for root in type_.root]
        value = ''
        for link in entity_dict['links']:
            if link.range.id == type_.id and link.description:
                value += link.description
                if link.range.id == type_.id and type_.description:
                    value += f' {type_.description}'
        key = ' > '.join(map(str, hierarchy))
        types[key].append(type_.name + (f": {value}" if value else ''))
    return types


def get_csv_links(entity_dict: dict[str, Any]) -> dict[str, Any]:
    links: dict[str, Any] = defaultdict(list)
    for link in entity_dict['links']:
        key = link.property.i18n['en'].replace(' ', '_') + '_' + \
            link.range.class_.name
        links[key].append(link.range.name)
    for link in entity_dict['links_inverse']:
        key = link.property.i18n['en'].replace(' ', '_') + '_' + \
            link.range.class_.name
        if link.property.i18n_inverse['en']:
            key = link.property.i18n_inverse['en'].replace(' ', '_') + '_' + \
                link.domain.class_.name
        links[key].append(link.domain.name)
    links.pop('has_type_type', None)
    return links


def get_csv_geom_entry(entity: Entity) -> str:
    geom_data = []
    if entity.class_.group.get('name') in ['place', 'artifact']:
        geom_data = get_gis_by_id(entity.get_linked_entity_safe('P53').id)
    elif entity.class_.name == 'object_location':
        geom_data = get_gis_by_id(entity.id)
    if not geom_data:
        return ''
    shapes = [shape(geom) for geom in geom_data]
    if len(shapes) == 1:
        return shapes[0].wkt
    else:
        return GeometryCollection(shapes).wkt


def get_grouped_entities(entities: list[dict[str, Any]]) -> dict[str, Any]:
    grouped_entities = {}
    for class_, entities_ in groupby(
            sorted(
                entities,
                key=lambda entity: entity['openatlas_class_name']),
            key=lambda entity: entity['openatlas_class_name']):
        grouped_entities[class_] = list(entities_)
    return grouped_entities


def export_database_csv(tables: dict[str, Any], filename: str) -> Response:
    archive = BytesIO()
    with zipfile.ZipFile(archive, 'w') as zipped_file:
        for name, entries in tables.items():
            if name == 'entities':
                for system_class, frame \
                        in get_grouped_entities(entries).items():
                    with zipped_file.open(
                            f'{system_class}.csv', 'w') as file:
                        file.write(bytes(
                            pd.DataFrame(data=frame).to_csv(),
                            encoding='utf-8'))
            else:
                with zipped_file.open(f'{name}.csv', 'w') as file:
                    file.write(bytes(
                        pd.DataFrame(data=entries).to_csv(),
                        encoding='utf-8'))
    return Response(
        archive.getvalue(),
        mimetype='application/zip',
        headers={
            'Content-Disposition': f'attachment;filename={filename}.zip'})
