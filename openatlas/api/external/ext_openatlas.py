from typing import Any

import requests
from flask import g

from openatlas import app
from openatlas.display.util import link



def fetch_openatlas(id_: str, url: str) -> dict[str, Any]:
    url = f'{url}{id_}'
    info: dict[str, str] = {}
    print(url)
    try:
        data = requests.get(
            url,
            proxies=app.config['PROXIES'],
            timeout=10).json()
    except Exception as e:  # pragma: no cover
        print(e)
        return info
    print(data)
    return {'name': data['features'][0]['properties']['title']}


def print_values(values: list[dict[str, str]]) -> str:
    return '<br>'.join(
        [link(item['label'], item['id'], external=True) for item in values])
