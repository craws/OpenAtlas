from typing import Any

import requests
from flask import g


def fetch_gnd(id_: str) -> dict[str, Any]:
    url = f'{g.gnd.resolver_url}{id_}.json'
    info = {}
    try:
        data = requests.get(url, timeout=10).json()
    except Exception:  # pragma: no cover
        return {}
    if 'preferredName' in data:
        info['preferred name'] = data['preferredName']
    return info
