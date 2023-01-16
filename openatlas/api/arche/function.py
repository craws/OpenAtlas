from typing import Any, Union

import rdflib
import requests
from flask import g, flash
from requests import Response, HTTPError
from werkzeug.exceptions import abort

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.imports import is_float
from openatlas.database.gis import Gis as Db_gis
from openatlas.models.reference_system import ReferenceSystem
from openatlas.database.reference_system import ReferenceSystem as Db
from openatlas.models.type import Type


def fetch_arche_data() -> dict[int, Any]:
    collections = {}
    for id_ in app.config['ARCHE']['collection_ids']:
        req = requests.get(
            f"{app.config['ARCHE']['base_url']}/api/{id_}/metadata",
            headers={'Accept': 'application/n-triples'},
            proxies={'http': 'http://fifi.arz.oeaw.ac.at:8080'})
        try:
            collections[id_] = get_metadata(n_triples_to_json(req))
        except HTTPError as http_error:
            flash(f'ARCHE fetch failed: {http_error}', 'error')
            abort(404)
    return collections


def get_metadata(data: dict[str, Any]) -> dict[str, Any]:
    system = get_arche_reference_system()
    existing_ids = \
        [int(link_.description) for link_ in system.get_links('P67')]
    metadata = {}
    for uri, node in data.items():
        for value in node.values():
            if '_metadata.json' in str(value[0]):
                json_ = requests.get(uri).json()
                image_url = get_linked_image(node['isMetadataFor'])
                image_id = int(image_url.rsplit('/', 1)[1])
                if image_id in existing_ids:
                    continue
                metadata[uri.rsplit('/', 1)[1]] = {
                    'image_id': image_id,
                    'image_link': image_url,
                    'image_link_thumbnail':
                        f"{app.config['ARCHE']['thumbnail_url']}"
                        f"{image_url.replace('https://', '')}?width=1200",
                    'creator': json_['EXIF:Artist'],
                    'latitude': json_['EXIF:GPSLatitude'],
                    'longitude': json_['EXIF:GPSLongitude'],
                    'description': json_['XMP:Description']
                    if 'XMP:Description' in json_ else '',
                    'name': json_['IPTC:ObjectName'],
                    'license': json_['EXIF:Copyright'],
                    'date': json_['EXIF:CreateDate']}
    return metadata


def get_linked_image(data: list[dict[str, Any]]) -> str:
    return [image['__uri__']
            for image in data if str(image['mime'][0]) == 'image/jpeg'][0]


def get_or_create_type(super_: Union[str, Type], type_name: str) -> Type:
    super_ = get_hierarchy_by_name(super_) \
        if isinstance(super_, str) else super_
    type_ = get_type_by_name(type_name)
    if not type_:
        type_ = Entity.insert('type', type_name)
        type_.link('P127', super_)
    return type_


def get_type_by_name(type_name: str) -> Type:
    type_ = None
    for type_id in g.types:
        if g.types[type_id].name == type_name:
            type_ = g.types[type_id]
    return type_


def get_hierarchy_by_name(type_name: str) -> Type:
    type_ = None
    for type_id in g.types:
        if g.types[type_id].name == type_name:
            if not g.types[type_id].root:
                type_ = g.types[type_id]
    return type_


def get_license_types(licenses: list[str]) -> list[Type]:
    return [get_or_create_type('License', license_) for license_ in licenses]


def get_creator_type(creators: list[str]) -> list[Type]:
    hierarchy = 'Creator'
    if not get_hierarchy_by_name('Creator'):
        hierarchy = Entity.insert('type', 'Creator')
        Type.insert_hierarchy(hierarchy, 'custom', ['file'], False)
    return [get_or_create_type(hierarchy, creator) for creator in creators]


def get_photographers(creators: list[str]) -> list[Entity]:
    creator_entities = []
    for entity in Entity.get_by_cidoc_class('E21', types=True):
        if entity.name in creators:
            creator_entities.append(entity)
            creators.remove(entity.name)
    if creators:
        for creator in creators:
            creator_entities.append(Entity.insert(
                'person',
                creator,
                'Automatically created by ARCHE import'))
    return creator_entities


def get_list_of_entries(entries: dict[str, Any], key: str) -> list[str]:
    return list(set(metadata[key] for metadata in entries.values()))


def link_arche_entity_to_type(
        entity: Entity,
        types: list[Type],
        type_name: str) -> None:
    for type_ in types:
        if type_.name == type_name:
            entity.link('P2', type_)


def import_arche_data() -> list[Entity]:
    entities = []
    arche_ref = [
        system for system in g.reference_systems.values()
        if system.name == 'ARCHE'][0]
    exact_match_id = None
    for sub_id in Type.get_hierarchy('External reference match').subs:
        if g.types[sub_id].name == 'exact match':
            exact_match_id = sub_id
    photograph_type = get_or_create_type('Event', 'photograph')
    photographers = []
    types = []
    for entries in fetch_arche_data().values():
        licenses = get_license_types(get_list_of_entries(entries, 'license'))
        creators_list = get_list_of_entries(entries, 'creator')
        creator_types = get_creator_type(creators_list)
        photographers = get_photographers(creators_list)
        types = licenses + creator_types
    for entries in fetch_arche_data().values():
        for metadata in entries.values():
            name = metadata['name']

            artifact = Entity.insert(
                'artifact',
                name.rsplit('.', 1)[0],
                metadata['description'])
            dates = {'begin_from': metadata['date']}
            artifact.update({'attributes': dates})

            arche_ref.link(
                'P67',
                artifact,
                metadata['image_id'],
                type_id=exact_match_id)

            location = Entity.insert('object_location', f"Location of {name}")
            artifact.link('P53', location)
            if is_float(metadata['longitude']) \
                    and is_float(metadata['latitude']):
                Db_gis.insert(
                    shape='Point',
                    data={
                        'entity_id': location.id,
                        'name': name,
                        'description': '',
                        'type': 'centerpoint',
                        'geojson':
                            f'{{"type":"Point", "coordinates": '
                            f'[{metadata["longitude"]},'
                            f'{metadata["latitude"]}]}}'})

            for creator in photographers:
                if creator.name == metadata['creator']:
                    event = Entity.insert(
                        'production',
                        f'Creation of photography from {name}')
                    event.link('P7', location)
                    event.update({'attributes': dates})
                    event.link('P2', photograph_type)
                    event.link('P11', creator)
                    event.link('P108', artifact)

            file = Entity.insert(
                'file',
                name,
                f"Created by {metadata['creator']}"
                if metadata['creator'] else '')
            link_arche_entity_to_type(file, types, metadata['license'])
            link_arche_entity_to_type(file, types, metadata['creator'])
            file_response = requests.get(metadata['image_link_thumbnail'])
            filename = f"{file.id}.{name.rsplit('.', 1)[1].lower()}"
            open(str(app.config['UPLOAD_DIR'] / filename), "wb") \
                .write(file_response.content)
            file.link('P67', range_=artifact)
            entities.append(artifact)
            entities.append(file)
    return entities


def get_arche_reference_system() -> ReferenceSystem:
    system = None
    for system_ in g.reference_systems.values():
        if system_.name == 'ARCHE':
            system = system_
    if not system:
        system = ReferenceSystem.insert_system({
            'name': 'ARCHE',
            'description': 'ARCHE by ACDH-CH (autogenerated)',
            'website_url': 'https://arche.acdh.oeaw.ac.at/',
            'resolver_url': app.config['ARCHE']['base_url']})
    if 'artifact' not in system.classes:
        Db.add_classes(system.id, ['artifact'])
    return system


# Script from
# https://acdh-oeaw.github.io/arche-docs/aux/rdf_compacting_and_framing.html


def n_triples_to_json(req: Response) -> dict[str, Any]:
    context = get_arche_context()
    data = rdflib.Graph()
    data.parse(data=req.text, format="nt")

    # create Python-native data model based on dictionaries
    nodes = {}
    for (sbj, prop, obj) in data:
        sbj = str(sbj)
        prop = str(prop)
        # skip RDF properties for which we don't know the mapping
        if prop not in context:
            continue

        # map prop name according to the context
        prop = context[prop]

        # if the triple points to another node in the graph,
        # maintain the reference
        if not isinstance(obj, rdflib.term.Literal):
            if str(obj) not in nodes:
                nodes[str(obj)] = {'__uri__': str(obj)}
            obj = nodes[str(obj.toPython())]

        # manage the data
        if sbj not in nodes:
            nodes[sbj] = {'__uri__': sbj}
        if prop not in nodes[sbj]:
            nodes[sbj][prop] = []
        nodes[sbj][prop].append(
            obj if not isinstance(obj, rdflib.term.Literal)
            else obj.toPython())
    return nodes


def get_arche_context() -> dict[str, Any]:
    context = requests.get(
        'https://arche.acdh.oeaw.ac.at/api/describe',
        headers={'Accept': 'application/json'})
    context = context.json()['schema']
    # adding isMetadataFor because it is not in /describe
    context['isMetadataFor'] = \
        'https://vocabs.acdh.oeaw.ac.at/schema#isMetadataFor'
    # flip the context so it's uri->shortName
    return {v: k for k, v in context.items() if isinstance(v, str)}
