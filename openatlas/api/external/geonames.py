import requests
import xmltodict
from flask import g

from openatlas import app


def fetch_geonames(id_: str) -> dict[str, object]:
    params = {
        'geonameId': {id_},
        'username': {g.settings['geonames_username']}}
    try:
        data = requests.get(
            app.config['API_GEONAMES'],
            params=params,
            proxies=app.config['PROXIES'],
            timeout=10).content
        data_dict = xmltodict.parse(data)['geoname']
    except Exception:  # pragma: no cover
        return {}
    info: dict[str, object] = {}
    for key, value in data_dict.items():
        if key == 'alternateNames' and value:
            info[key] = '<br>'.join(value.split(','))
        elif isinstance(value, str):
            info[key] = value
    return info
