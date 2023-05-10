from typing import Any

import requests

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.type import Type


def import_vocabs_data(id_: str) -> int:
    hierarchies = fetch_top_level(id_)
    print(hierarchies)
    return 1


def fetch_top_level(id_: str) -> list[dict[str, Any]]:
    req = requests.get(
        f"{app.config['VOCABS']['api_uri']}{app.config['VOCABS']['id']}/{id_}",
        timeout=60,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW'])
        # Todo: auth can be deleted if public
    )
    hierarchies = []
    for entry in req.json()[id_.lower()]:
        name = entry['uri'].rsplit('/', 1)[-1]
        entry['name'] = name  # can be deleted?
        hierarchy = Entity.insert('type', entry['label'])
        Type.insert_hierarchy(hierarchy, 'custom', ['artifact'], True)
        entry['subs'] = fetch_children(entry['uri'], hierarchy)
        hierarchies.append(entry)
    return hierarchies


def fetch_children(uri: str, super_: Entity) -> list[dict[str, Any]]:
    req = requests.get(
        f"{app.config['VOCABS']['api_uri']}"
        f"{app.config['VOCABS']['id']}/narrower",
        params={'uri': uri},
        timeout=60,
        auth=(app.config['VOCABS_USER'],
              app.config['VOCABS_PW']))  # Todo: auth can be deleted if public
    children = []
    for entry in req.json()['narrower']:
        name = entry['uri'].rsplit('/', 1)[-1]
        entry['name'] = name  # can be deleted?
        child = Entity.insert('type', entry['prefLabel'])
        child.link('P127', super_)
        entry['subs'] = fetch_children(entry['uri'], child)
        children.append(entry)
    return children
