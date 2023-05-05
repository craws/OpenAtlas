from typing import Any

import requests

from openatlas import app


def fetch_top_level(id_: str) -> list[dict[str, str]]:
    req = requests.get(
        f"{app.config['VOCABS']['api_uri']}{app.config['VOCABS']['id']}/{id_}",
        timeout=60,
        auth=('test', 'fH8gL1NEjryt')  # Todo: auth can be deleted if public
    )
    data = []
    for entry in req.json()[id_.lower()]:
        data.append({
            'name': entry['prefLabel'] if id_ == 'groups' else entry[
                'label'],
            'uri': f"{app.config['VOCABS']['uri']}{app.config['VOCABS']['id']}"
                   f"/{entry['uri'].rsplit('/', 1)[-1]}"
            # Todo: if public: 'uri': entry['uri']
        })
    return data


def import_vocabs_data(id_: str) -> int:
    top_level = fetch_top_level(id_)
    if id_ == 'groups':
        get_group_children(top_level)
    return 1


def get_group_children(data: list[dict[str, str]]) -> dict[str, Any]:
    return None
