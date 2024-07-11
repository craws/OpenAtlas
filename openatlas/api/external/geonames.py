from typing import Any

import requests
import xmltodict
from flask import g


def fetch_geonames(id_: str) -> dict[str, Any]:
    url = f"http://api.geonames.org/get"
    params = {
        'geonameId': {id_},
        'username': {g.settings['geonames_username']}}
    try:
        data = requests.get(url, params, timeout=10).content
        data_dict = xmltodict.parse(data)['geoname']
    except Exception:  # pragma: no cover
        return {}
    info = {}
    for key, value in data_dict.items():
        if key == 'alternateNames':
            info[key] = '<br>'.join(value.split(','))
        elif isinstance(value, str):
            info[key] = value
    return info
