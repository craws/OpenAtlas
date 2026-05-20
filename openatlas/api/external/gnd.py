from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class GND(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        info: dict[str, object] = {}
        try:
            data = requests.get(
                f'{system.resolver_url}{id_}.json',
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return info

        def print_values(values: list[dict[str, str]]) -> str:
            return '<br>'.join(
                [link(i['label'], i['id'], external=True) for i in values])

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
