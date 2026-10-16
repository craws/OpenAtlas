from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class GND(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        try:
            data = requests.get(
                f'{system.resolver_url}{id_}.json',
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return {}

        def print_values(values: list[dict[str, str]]) -> str:
            return '<br>'.join(
                [link(i['label'], i['id'], external=True) for i in values])

        info: dict[str, object] = {}

        if pref_name := data.get('preferredName'):
            info['preferred name'] = pref_name

        if gender := data.get('gender'):
            info['gender'] = print_values(gender)

        if dob := data.get('dateOfBirth'):
            info['date of birth'] = dob

        if pob := data.get('placeOfBirth'):
            info['place of birth'] = print_values(pob)

        if dod := data.get('dateOfDeath'):
            info['date of death'] = dod

        if pod := data.get('placeOfDeath'):
            info['place of death'] = print_values(pod)

        if types := data.get('type'):
            info['type'] = '<br>'.join(types) \
                if isinstance(types, list) else str(types)

        return info
