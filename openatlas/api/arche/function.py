from typing import Any

import rdflib
import requests
from requests import Response

from openatlas import app


def fetch_files() -> dict[int, Any]:
    collections = {}
    for id_ in app.config['ARCHE_COLLECTION_IDS']:
        req = requests.get(
            f"{app.config['ARCHE_BASE_URL']}/api/{id_}/metadata",
            headers={'Accept': 'application/n-triples'})
        collections[id_] = sort_data(n_triples_to_json(req))
    return collections


def sort_data(data: dict[str, Any]) -> dict[str, Any]:
    files = {
        'metadata': {},
        'not_unique_values': {},
        'jpeg': {},
        'tiff': {}}
    for uri, node in data.items():
        uri_split = uri.rsplit('/', 1)[1]
        for prop, value in node.items():
            if 'metadata' in str(value[0]):
                files['metadata'][uri_split] = json_dict(uri, node)
            if 'not_unique_values' in str(value[0]):
                files['not_unique_values'][uri_split] = json_dict(uri, node)
            if str(value[0]) in ['image/jpeg', 'image/tiff']:
                value = str(value[0].rsplit('/', 1)[1])
                files[value][uri_split] = image_dict(uri, node)
    return files


def json_dict(uri: str, node: dict[str, Any]) -> dict[str, Any]:
    return {
        'metadataARCHE': node,
        'metadataFile': requests.get(uri).json(),
        'isMetadataFor': get_linked_image_id(node['isMetadataFor'])}


def image_dict(uri: str, node: dict[str, Any]) -> dict[str, Any]:
    return {
        'metadataARCHE': node,
        'originalFileLink': uri,
        'thumbnailLink':
            f"{app.config['ARCHE_THUMBNAIL']}"
            f"{uri.replace('https://', '')}?width=400"}


def get_linked_image_id(data: list[dict[str, Any]]) -> str:
    for image in data:
        if str(image['mime'][0]) == 'image/jpeg':
            return image['__uri__'].rsplit('/', 1)[1]


########################
# Script from
# https://acdh-oeaw.github.io/arche-docs/aux/rdf_compacting_and_framing.html
########################
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
