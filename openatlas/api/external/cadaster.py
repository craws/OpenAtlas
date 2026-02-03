from typing import Any

import requests
from shapely.geometry import shape

from openatlas import app
from openatlas.display.util import link


def fetch_cadaster(id_: str) -> dict[str, Any]:
    endpoint = 'gst/' if '/' in id_ else 'kgnr/'
    info = {}
    try:
        data = requests.get(
            f'{app.config['API_CADASTER']}{endpoint}{id_}',
            headers=app.config['USER_AGENT'],
            proxies=app.config['PROXIES'],
            timeout=10).json()
    except Exception:  # pragma: no cover
        return {}
    try:
        info['katestralgemeinde'] = data['properties']['kg']
    except KeyError:  # pragma: no cover
        pass
    try:
        info['bundesland'] = data['properties']['bl']
    except KeyError:  # pragma: no cover
        pass
    try:
        info['grundstücksnummer'] = data['properties']['gnr']
    except KeyError:  # pragma: no cover
        pass
    try:
        info['einlagezahl'] = data['properties']['ez']
    except KeyError:  # pragma: no cover
        pass
    try:
        info['rstatus'] = data['properties']['rstatus']
    except KeyError:  # pragma: no cover
        pass
    try:
        info['nutzungen'] = [
            f'Allocation: {usage['nutzung']}, Area: {usage['fl']}m²'
            for usage in data['properties']['nutzungen']]
    except KeyError:  # pragma: no cover
        pass
    try:
        geometry = shape(data['geometry']).centroid
        zoom = '18.1' if '/' in id_ else '12.9'
        url = f'https://kataster.bev.gv.at/#/center/' \
              f'{geometry.x},{geometry.y}/zoom/{zoom}/vermv/0.6'
        info['geometry'] = link(url, url, external=True)
    except KeyError:  # pragma: no cover
        pass
    try:
        info['Error'] = data['message']
    except KeyError:  # pragma: no cover
        pass
    return info
