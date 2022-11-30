from typing import Any

import rdflib
import requests
from flask import Response

from openatlas import app


def fetch_files() -> dict[int, Any]:
    collections = {}
    for id_ in app.config['ARCHE_COLLECTION_IDS']:
        req = requests.get(
            f"{app.config['ARCHE_BASE_URL']}/api/{id_}/metadata",
            headers={'Accept': 'application/n-triples'})
        collections[id_] = filter_all_files(req)
    print(collections)
    # print(collections[1390141]['metadata']['https://arche-curation.acdh-dev.oeaw.ac.at/api/1390185']['isMetadataFor'])
    # print(len(collections[1390141]['not_unique_values']))
    # print(len(collections[1390141]['images']))

    return collections


def filter_all_files(req: Response) -> dict[str, Any]:
    files = {
        'metadata': {},
        'not_unique_values': {},
        'images': {}}
    for uri, node in n_triples_to_json(req).items():
        for prop, value in node.items():
            if 'metadata.json' in str(value[0]):
                files['metadata'][uri.rsplit('/', 1)[1]] = {
                    'metadataARCHE': node,
                    'metadataFile': requests.get(uri).json(),
                    'isMetadataFor':
                        get_jpeg_from_metadata(node['isMetadataFor'])}
            if '_not_unique_values.json' in str(value[0]):
                files['not_unique_values'][uri.rsplit('/', 1)[1]] = {
                    'metadataARCHE': node,
                    'metadataFile': requests.get(uri).json(),
                    'isMetadataFor':
                        get_jpeg_from_metadata(node['isMetadataFor'])}
            if str(value[0]) == 'image/jpeg':
                files['images'][uri.rsplit('/', 1)[1]] = {
                    'metadataARCHE': node,
                    'originalFileLink': uri,
                    'thumbnailLink':
                        f"{app.config['ARCHE_THUMBNAIL']}{uri.replace('https://', '')}?width=400"}
            if str(value[0]) == 'image/tiff':
                files['images'][uri.rsplit('/', 1)[1]] = {
                    'metadataARCHE': node,
                    'originalFileLink': uri,
                    'thumbnailLink':
                        f"{app.config['ARCHE_THUMBNAIL']}{uri.replace('https://', '')}?width=400"}
    return files


def get_jpeg_from_metadata(data: list[dict[str, Any]]) -> str:
    for image in data:
        if str(image['mime'][0]) == 'image/jpeg':
            return image['__uri__'].rsplit('/', 1)[1]


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
            # print(prop)
            continue

        # map prop name according to the context
        prop = context[prop]

        # if the triple points to another node in the graph,
        # maintain the reference
        if not isinstance(obj, rdflib.term.Literal):
            if str(obj) not in nodes:
                nodes[str(obj)] = {'__uri__': str(obj)}
            obj = nodes[str(obj)]

        # manage the data
        if sbj not in nodes:
            nodes[sbj] = {'__uri__': sbj}
        if prop not in nodes[sbj]:
            nodes[sbj][prop] = []
        nodes[sbj][prop].append(obj)
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
