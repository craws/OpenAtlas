from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.models.entity import Entity


class OpenAtlas(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        info: dict[str, object] = {}
        try:
            api_url = f'{system.website_url}/api/entity_presentation_view/'
            data = requests.get(
                # f'{g.openatlas.resolver_url}{id_}',
                f'{api_url}/{id_}',
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return info

        info['name'] = data.get('title')
        info['OpenAtlas class'] = data.get('systemClass')
        info['aliases'] = '<br>'.join(data.get('aliases'))
        for type_ in data.get('types', []):
            if type_.get('isStandard'):
                info['type'] = type_.get('title')
        info['begin from'] = data['when']['start'].get('earliest')
        info['begin to'] = data['when']['start'].get('latest')
        info['begin comment'] = data['when']['start'].get('comment')
        info['end from'] = data['when']['end'].get('earliest')
        info['end to'] = data['when']['end'].get('latest')
        info['end comment'] = data['when']['end'].get('comment')
        info['description'] = data.get('description')

        return info
