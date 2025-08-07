import zipfile
from collections import defaultdict
from io import BytesIO
from itertools import groupby
from typing import Any

import pandas as pd
from flask import Response, g

from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis


def build_dataframe(entity: Entity) -> dict[str, Any]:
    geom = get_csv_geom_entry(entity)
    return {
        'id': str(entity.id),
        'name': entity.name,
        'description': entity.description,
        'begin_from': entity.begin_from,
        'begin_to': entity.begin_to,
        'begin_comment': entity.begin_comment,
        'end_from': entity.end_from,
        'end_to': entity.end_to,
        'end_comment': entity.end_comment,
        'cidoc_class': entity.cidoc_class.name,
        'system_class': entity.class_.name,
        'geom_type': geom['type'],
        'coordinates': geom['coordinates']}


def build_link_dataframe(link: Link) -> dict[str, Any]:
    return {
        'id': link.id,
        'range_id': link.range.id,
        'range_name': link.range.name,
        'domain_id': link.domain.id,
        'domain_name': link.domain.name,
        'description': link.description,
        'begin_from': link.begin_from,
        'begin_to': link.begin_to,
        'begin_comment': link.begin_comment,
        'end_from': link.end_from,
        'end_to': link.end_to,
        'end_comment': link.end_comment}


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
        key = f"{link.property.i18n['en'].replace(' ', '_')}_" \
              f"{link.range.class_.name}"
        links[key].append(link.range.name)
    for link in entity_dict['links_inverse']:
        key = f"{link.property.i18n['en'].replace(' ', '_')}_" \
              f"{link.range.class_.name}"
        if link.property.i18n_inverse['en']:
            key = link.property.i18n_inverse['en'].replace(' ', '_')
            key += '_' + link.domain.class_.name
        links[key].append(link.domain.name)
    links.pop('has_type_type', None)
    return links


def get_csv_geom_entry(entity: Entity) -> dict[str, None]:
    geom = {'type': None, 'coordinates': None}
    if entity.class_.group['name'] == 'place' or entity.class_.name == 'artifact':
        geom = get_csv_geometry(entity.get_linked_entity_safe('P53'))
    elif entity.class_.name == 'object_location':
        geom = get_csv_geometry(entity)
    return geom


def get_csv_geometry(entity: Entity) -> dict[str, Any]:
    dict_: dict[str, Any] = {'type': None, 'coordinates': None}
    if (geoms := Gis.get_by_id(entity.id)) \
            and entity.cidoc_class.code == 'E53':
        dict_ = {key: [geom[key] for geom in geoms] for key in geoms[0]}
    return dict_


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
