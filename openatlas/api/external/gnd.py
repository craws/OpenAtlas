from typing import Any

import requests
from flask import g

from openatlas.display.util import link


def fetch_gnd(id_: str) -> dict[str, Any]:
    url = f'https://lobid.org/gnd/{id_}.json'
    url = 'https://lobid.org/gnd/4074335-4.json'
    info = {}
    try:
        data = requests.get(url, timeout=10).json()
    except Exception:  # pragma: no cover
        return {}

    # print(data)

    if 'preferredName' in data:
        info['preferred name'] = data['preferredName']
    return info
