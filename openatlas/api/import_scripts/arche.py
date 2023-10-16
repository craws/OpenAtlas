from typing import Any, Optional

import requests
from flask import g

from openatlas.api.import_scripts.util import request_arche_metadata
from openatlas import app
from openatlas.api.import_scripts.util import (
    get_exact_match, get_or_create_type, get_reference_system)
from openatlas.database.reference_system import ReferenceSystem as Db
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type


def fetch_collection_data() -> dict[str, Any]:
    collections = get_collections()
    collection_jpgs = request_arche_metadata(collections['2_JPEGs'])
    return get_metadata(collection_jpgs)


def get_collections() -> dict[str, Any]:
    project_id = app.config['ARCHE']['id']
    collections_dict = {}
    for collection in request_arche_metadata(project_id)['@graph']:
        if collection['@type'] == 'n1:Collection':
            title = collection['n1:hasTitle']['@value']
            collections_dict[title] = collection['@id'].replace('n0:', '')
    return collections_dict


def get_metadata(data: dict[str, Any]) -> dict[str, Any]:
    existing_ids = get_existing_ids()
    metadata = {}
    for collection in data['@graph']:
        if collection['@type'] == "n1:Collection":
            if collection["n1:hasFilename"] == "2_JPEGs":
                continue
            id_ = collection['@id'].replace('n0:', '')
            if int(id_) in existing_ids:
                continue
            collection_url = (data['@context']['n0'] + id_)
            metadata[collection_url] = {
                'collection_id': id_,
                'filename': collection['n1:hasFilename']}
    return metadata


def get_existing_ids() -> list[int]:
    system = get_arche_reference_system()
    return [int(link_.description) for link_ in system.get_links('P67')]


def fetch_exif(id_: str) -> dict[str, Any]:
    req = requests.get(
        'https://arche-exif.acdh.oeaw.ac.at/',
        params={'id': id_})
    return req.json()


def get_single_image_of_collection(id_: int) -> str:
    file_collection = request_arche_metadata(id_)
    return_id = 'string'
    for resource in file_collection['@graph']:
        if resource['@type'] == 'n1:Resource':
            return_id = file_collection['@context']['n0'] + resource[
                '@id'].replace('n0:', '')
            break
    return return_id


def get_orthophoto(filename: str) -> str:
    collections = get_collections()
    collection_ortho = request_arche_metadata(collections['4_Orthophotos'])
    id_ = ''
    for entry in collection_ortho['@graph']:
        if entry['@type'] == 'n1:Collection' and \
                entry['n1:hasTitle']['@value'] == filename:
            folder = request_arche_metadata(entry['@id'].replace('n0:', ''))
            for item in folder['@graph']:
                if item['@type'] == 'n1:Resource':
                    if item['n1:hasFormat'] == 'image/png':
                        id_ = collection_ortho['@context']['n0'] \
                              + item['@id'].replace('n0:', '')
                        break
    return id_


def import_arche_data() -> int:
    count = 0
    person_types = get_or_create_person_types()
    for entries in fetch_collection_data().values():
        exif = get_exif(entries)
        name = entries['filename']
        artifact = Entity.insert('artifact', name)

        get_reference_system('ARCHE').link(
            'P67',
            artifact,
            entries['collection_id'],
            type_id=get_exact_match().id)

        location = Entity.insert('object_location', f"Location of {name}")
        artifact.link('P53', location)
        # if is_float(item['longitude']) and is_float(item['latitude']):
        #     Db_gis.insert(
        #         shape='Point',
        #         data={
        #             'entity_id': location.id,
        #             'name': name,
        #             'description': '',
        #             'type': 'centerpoint',
        #             'geojson':
        #                 f'{{"type":"Point", "coordinates": '
        #                 f'[{item["longitude"]},'
        #                 f'{item["latitude"]}]}}'})
        #
        # production = Entity.insert(
        #     'production',
        #     f'Production of graffito from {name}')
        # production.link('P108', artifact)
        #
        file = Entity.insert('file', name, f"Created by {exif['Creator']}")

        file.link(
            'P2',
            get_or_create_type(
                get_hierarchy_by_name('License'),
                exif['Copyright']))
        filename = f"{file.id}.png"
        ortho_photo: str = get_orthophoto(entries['filename'])
        thumb_req = requests.get(
            'https://arche-thumbnails.acdh.oeaw.ac.at/',
            params={'id': ortho_photo, 'width': 1200},  # type: ignore
            timeout=60).content
        open(str(app.config['UPLOAD_PATH'] / filename), "wb").write(thumb_req)
        file.link('P67', artifact)

        creator = get_or_create_person(
            exif['Creator'],
            person_types['photographer_type'])

        creation = Entity.insert(
            'creation',
            f'Creation of photograph from {name}')
        creation.update({'attributes': {'begin_from': exif['CreateDate']}})
        creation.link('P94', file)
        creation.link('P14', creator)

        count += 1
    return count


def get_exif(entries: dict[str, Any]) -> dict[str, Any]:
    single_img_id = get_single_image_of_collection(entries['collection_id'])
    return fetch_exif(single_img_id)


def get_hierarchy_by_name(name: str) -> Optional[Type]:
    type_ = None
    for type_id in g.types:
        if g.types[type_id].name == name:
            if not g.types[type_id].root:
                type_ = g.types[type_id]
    return type_


def get_or_create_person(name: str, relevance: Type) -> Entity:
    for entity in Entity.get_by_cidoc_class('E21'):
        if entity.name == name:
            return entity
    entity = Entity.insert(
        'person',
        name,
        'Automatically created by ARCHE import')
    entity.link('P2', relevance)
    return entity


def get_or_create_person_types() -> dict[str, Any]:
    hierarchy = get_hierarchy_by_name('Relevance')
    if not hierarchy:
        hierarchy = Entity.insert('type', 'Relevance')  # type: ignore
        Type.insert_hierarchy(
            hierarchy, 'custom', ['person'], True)  # type: ignore
    return {
        'photographer_type': get_or_create_type(hierarchy, 'Photographer'),
        'artist_type': get_or_create_type(hierarchy, 'Graffito artist')}


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
            'resolver_url': f"{app.config['ARCHE']['url']}/browser/detail/"})
    if 'artifact' not in system.classes:
        Db.add_classes(system.id, ['artifact'])
    return system
