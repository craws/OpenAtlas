from typing import Any, Optional

import requests
from flask import g

from openatlas import app
from openatlas.api.import_scripts.util import get_exact_match
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem

def import_vocabs_data(id_: str) -> int:
    return len(fetch_top_level(id_, get_vocabs_reference_system(id_)))


def fetch_top_level(
        id_: str,
        ref: Optional[ReferenceSystem] = None) -> list[dict[str, Any]]:
    req = requests.get(
        f"{g.settings['vocabs_base_url']}{g.settings['vocabs_endpoint']}{id_}"
        "/topConcepts",
        timeout=60,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW']))
    exact_match_id = get_exact_match().id
    hierarchies = []
    hierarchy = None
    for entry in req.json()['topconcepts']:
        name = entry['uri'].rsplit('/', 1)[-1]
        if ref:
            hierarchy = Entity.insert(
                'type',
                entry['label'],
                'Automatically imported by VOCABS')
            #Type.insert_hierarchy(hierarchy, 'custom', ['artifact'], True)
            ref.link(
                'P67',
                hierarchy,
                name,
                type_id=exact_match_id)
        entry['subs'] = import_children(entry['uri'], id_, hierarchy, ref)
        hierarchies.append(entry)
    return hierarchies


def import_children(
        uri: str,
        id_: str,
        super_: Optional[Entity],
        ref: Optional[ReferenceSystem]) -> list[dict[str, Any]]:
    req = requests.get(
        f"{g.settings['vocabs_base_url']}{g.settings['vocabs_endpoint']}{id_}"
        "/narrower",
        params={'uri': uri},
        timeout=60,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW']))
    exact_match_id = get_exact_match().id
    children = []
    child = None
    for entry in req.json()['narrower']:
        name = entry['uri'].rsplit('/', 1)[-1]
        if super_ and ref:
            child = Entity.insert('type', entry['prefLabel'])
            child.link('P127', super_)
            ref.link('P67', child, name, type_id=exact_match_id)
        entry['subs'] = import_children(entry['uri'], id_, child, ref)
        children.append(entry)
    return children


def get_vocabs_reference_system(id_: str) -> ReferenceSystem:
    system = None
    for system_ in g.reference_systems.values():
        if system_.name == 'VOCABS':
            system = system_
    if not system:
        system = ReferenceSystem.insert_system({
            'name': 'VOCABS',
            'description': 'VOCABS by ACDH-CH (autogenerated)',
            'website_url': g.settings['vocabs_base_url'],
            'resolver_url': f"{g.settings['vocabs_base_url']}{id_}/"})
    # if 'artifact' not in system.classes:
    #     Db.add_classes(system.id, ['artifact'])
    return system


def get_vocabularies():
    out = []
    for voc in fetch_vocabularies():
        out.append(voc | fetch_vocabulary_details(voc['uri']))
    return out


def fetch_vocabulary_details(id_: str) -> dict[str, str]:
    req = requests.get(
        f"{g.settings['vocabs_base_url']}{g.settings['vocabs_endpoint']}{id_}",
        params={'lang': 'en'},
        timeout=60,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW']))
    data = req.json()
    return {
        'id': data['id'],
        'title': data['title'],
        'defaultLanguage': data['defaultLanguage'],
        'languages': data['languages'],
        'conceptUri': data['conceptschemes'][0]['uri'] if data[
            'conceptschemes'] else ''
    }


def fetch_vocabulary_metadata(id_: str, uri: str) -> dict[str, str]:
    req = requests.get(
        f"{g.settings['vocabs_base_url']}{g.settings['vocabs_endpoint']}{id_}"
        "/data",
        params={'uri': uri, 'format': 'application/ld+json'},
        timeout=60,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW']))
    data = req.json()
    return data['graph'][0]


def fetch_vocabularies() -> list[dict[str, str]]:
    req = requests.get(
        f"{g.settings['vocabs_base_url']}{g.settings['vocabs_endpoint']}"
        "vocabularies",
        params={'lang': 'en'},
        timeout=60,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW']))
    return req.json()['vocabularies']
