from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.models.entity import Entity


class APIS(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        info: dict[str, object] = {}
        # // leads to problems in Django
        base_url = system.resolver_url.rstrip('/')
        data = {}
        try:
            response = requests.get(
                f'{base_url}/{id_}',
                headers={
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0"},
                proxies=app.config['PROXIES'],
                timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException:  # pragma: no cover
            pass

        info['forename'] = data.get('forename')
        info['surname'] = data.get('surname')
        info['url'] = f'<a href="{data.get('url')}" ' \
                      f'target="_blank" rel="noopener noreferrer">' \
                      f'{data.get('url')}</a>'
        return info
