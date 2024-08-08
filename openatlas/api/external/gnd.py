from typing import Any

import requests
from flask import g

from openatlas.display.util import link


def fetch_gnd(id_: str) -> dict[str, Any]:
    url = f'{g.gnd.resolver_url}{id_}.json'
    info: dict[str, str] = {}
    try:
        data = requests.get(url, timeout=10).json()
    except Exception:  # pragma: no cover
        return info
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


def print_values(values: list[dict[str, str]]) -> str:
    return '<br>'.join(
        [link(item['label'], item['id'], external=True) for item in values])
