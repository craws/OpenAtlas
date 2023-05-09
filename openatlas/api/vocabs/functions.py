from typing import Any

import requests

from openatlas import app


def fetch_top_level(id_: str) -> dict[str, Any]:
    req = requests.get(
        f"{app.config['VOCABS']['api_uri']}{app.config['VOCABS']['id']}/{id_}",
        timeout=60,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW'])  # Todo: auth can be deleted if public
    )
    hierarchies = {}
    for entry in req.json()[id_.lower()]:
        hierarchies[entry['uri'].rsplit('/', 1)[-1]] = {
            'label': entry['prefLabel'] if id_ == 'groups' else entry['label'],
            'name': entry['uri'].rsplit('/', 1)[-1],
            'uri': f"{app.config['VOCABS']['uri']}{app.config['VOCABS']['id']}"
                   f"/{entry['uri'].rsplit('/', 1)[-1]}",
            'hasMembers': entry['hasMembers'], # only for groups
            'subs': {}
            # Todo: if public: 'uri': entry['uri']
        }
    return hierarchies


def import_vocabs_data(id_: str) -> int:
    hierarchies = fetch_top_level(id_)
    if id_ == 'groups':
        out = add_group_members(hierarchies)
    print(out)
    return 1


def add_group_members(hierarchies: dict[str, Any]) -> list[dict[str, Any]]:
    print(len(hierarchies))
    for hierarchy in hierarchies:
        print(fetch_group_subs(hierarchy))

    return 1


def fetch_group_subs(id_: str):
    req = requests.get(
        f"{app.config['VOCABS']['api_uri']}{app.config['VOCABS']['id']}/groupMembers",
        params={'uri': id_},
        timeout=60,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW']))   # Todo: auth can be deleted if public
    member = {}
    for entry in req.json()['members']:
        member[entry['uri'].rsplit('/', 1)[-1]] = {
            'label': entry['prefLabel'],
            'name': entry['uri'].rsplit('/', 1)[-1],
            'uri': f"{app.config['VOCABS']['uri']}{app.config['VOCABS']['id']}"
                   f"/{entry['uri'].rsplit('/', 1)[-1]}",
            'hasMembers': entry['hasMembers'],
            'subs': {}
            # Todo: if public: 'uri': entry['uri']
        }
    return member
