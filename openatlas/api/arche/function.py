from typing import Any

import rdflib
import requests
from requests import Response

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.imports import is_float
from openatlas.database.gis import Gis as Db
from openatlas.models.reference_system import ReferenceSystem


def fetch_arche_data() -> dict[int, Any]:
    collections = {}
    for id_ in app.config['ARCHE_COLLECTION_IDS']:
        req = requests.get(
            f"{app.config['ARCHE_BASE_URL']}/api/{id_}/metadata",
            headers={'Accept': 'application/n-triples'})
        collections[id_] = get_metadata(n_triples_to_json(req))
    return collections


def get_metadata(data: dict[str, Any]) -> dict[str, Any]:
    metadata = {}
    for uri, node in data.items():
        for value in node.values():
            if '_metadata.json' in str(value[0]):
                json_ = requests.get(uri).json()
                image_url = get_linked_image(node['isMetadataFor'])
                metadata[uri.rsplit('/', 1)[1]] = {
                    'image_id': image_url.rsplit('/', 1)[1],
                    'image_link': image_url,
                    'image_link_thumbnail':
                        f"{app.config['ARCHE_THUMBNAIL']}"
                        f"{image_url.replace('https://', '')}?width=1200",
                    'creator': json_['EXIF:Artist'],
                    'latitude': json_['EXIF:GPSLatitude'],
                    'longitude': json_['EXIF:GPSLongitude'],
                    'description': json_['XMP:Description']
                    if 'XMP:Description' in json_ else '',
                    'name': json_['IPTC:ObjectName'],
                    'date': json_['EXIF:CreateDate']}
    return metadata


def get_linked_image(data: list[dict[str, Any]]) -> str:
    for image in data:
        if str(image['mime'][0]) == 'image/jpeg':
            return image['__uri__']


def import_arche_data() -> list[Entity]:
    entities = []
    arche_ref = ReferenceSystem.get_by_name('ARCHE')
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
                type_id=arche_ref.precision_default_id)

            location = Entity.insert('object_location', f"Location of {name}")
            artifact.link('P53', location)
            if is_float(metadata['longitude']) \
                    and is_float(metadata['latitude']):
                Db.insert(
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

            file = Entity.insert('file', name, metadata['description'])
            file_response = requests.get(metadata['image_link_thumbnail'])
            filename = f"{file.id}.{name.rsplit('.', 1)[1].lower()}"
            open(str(app.config['UPLOAD_DIR'] / filename), "wb") \
                .write(file_response.content)
            file.link('P67', range_=artifact)
            entities.append(artifact)
            entities.append(file)
    return entities


###############################################################################
# Script from                                                                 #
# https://acdh-oeaw.github.io/arche-docs/aux/rdf_compacting_and_framing.html  #
###############################################################################

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


########################################
# Can be deleted if not needed anymore #
########################################

def fetch_arche_data_deprecated() -> dict[int, Any]:
    collections = {}
    for id_ in app.config['ARCHE_COLLECTION_IDS']:
        req = requests.get(
            f"{app.config['ARCHE_BASE_URL']}/api/{id_}/metadata",
            headers={'Accept': 'application/n-triples'})
        collections[id_] = sort_data_deprecated(n_triples_to_json(req))
    return collections


def sort_data_deprecated(data: dict[str, Any]) -> dict[str, Any]:
    files = {
        'metadata': {},
        'not_unique_values': {},
        'jpeg': {},
        'tiff': {}}
    for uri, node in data.items():
        uri_split = uri.rsplit('/', 1)[1]
        for prop, value in node.items():
            if 'metadata' in str(value[0]):
                files['metadata'][uri_split] = json_dict_deprecated(uri, node)
            if 'not_unique_values' in str(value[0]):
                files['not_unique_values'][uri_split] \
                    = json_dict_deprecated(uri, node)
            if str(value[0]) in ['image/jpeg', 'image/tiff']:
                value = str(value[0].rsplit('/', 1)[1])
                files[value][uri_split] = image_dict_deprecated(uri, node)
    return files


def json_dict_deprecated(uri: str, node: dict[str, Any]) -> dict[str, Any]:
    return {
        'metadataARCHE': node,
        'metadataFile': requests.get(uri).json(),
        'isMetadataFor': get_linked_image_id_deprecated(node['isMetadataFor'])}


def image_dict_deprecated(uri: str, node: dict[str, Any]) -> dict[str, Any]:
    return {
        'metadataARCHE': node,
        'originalFileLink': uri,
        'thumbnailLink':
            f"{app.config['ARCHE_THUMBNAIL']}"
            f"{uri.replace('https://', '')}?width=400"}


def get_linked_image_id_deprecated(data: list[dict[str, Any]]) -> str:
    for image in data:
        if str(image['mime'][0]) == 'image/jpeg':
            return image['__uri__'].rsplit('/', 1)[1]
