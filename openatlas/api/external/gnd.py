from typing import Any

import requests
from flask import g

from openatlas.display.util import link


def print_values(values: dict[str: str]) -> str:
    items = []
    for item in values:
        items.append(link(item["label"], item["id"], external=True))
    return '<br>'.join(items)


def fetch_gnd(id_: str) -> dict[str, Any]:
    url = f'{g.gnd.resolver_url}{id_}.json'
    info = {}
    try:
        data = requests.get(url, timeout=10).json()
    except Exception:  # pragma: no cover
        return {}
    if 'preferredName' in data:
        info['preferred name'] = data['preferredName']
    if 'gender' in data:
        info['gender'] = print_values(data['gender'])
    if 'dateOfBirth' in data:
        info['date of birth'] = data['dateOfBirth']
    if 'placeOfBirth' in data:
        info['place of birth'] = print_values(data['placeOfBirth'])
    if 'dateOfDeath' in data:
        info['date of death'] = data['dateOfDeath']
    if 'placeOfDeath' in data:
        info['place of death'] = print_values(data['placeOfDeath'])
    if 'type' in data:
        info['type'] = '<br>'.join(data['type'])

    return info
