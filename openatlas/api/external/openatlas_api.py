from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.models.entity import Entity


class OpenAtlas(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        try:
            api_url = f'{system.website_url}/api/entity_presentation_view/'
            data = requests.get(
                # f'{g.openatlas.resolver_url}{id_}',
                f'{api_url}/{id_}',
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return {}

        info: dict[str, object] = {}

        if title := data.get('title'):
            info['name'] = title

        if sys_class := data.get('systemClass'):
            info['OpenAtlas class'] = sys_class

        if aliases := data.get('aliases'):
            info['aliases'] = '<br>'.join(aliases)  # pragma: no cover

        for type_ in data.get('types', []):
            if type_.get('isStandard') and type_.get('title'):
                info['type'] = type_['title']
                break

        if when := data.get('when', {}):
            start = when.get('start', {})
            if earliest := start.get('earliest'):
                info['begin from'] = earliest
            if latest := start.get('latest'):
                info['begin to'] = latest  # pragma: no cover
            if comment := start.get('comment'):
                info['begin comment'] = comment

            end = when.get('end', {})
            if earliest := end.get('earliest'):
                info['end from'] = earliest
            if latest := end.get('latest'):
                info['end to'] = latest  # pragma: no cover
            if comment := end.get('comment'):
                info['end comment'] = comment  # pragma: no cover

        if desc := data.get('description'):
            info['description'] = desc  # pragma: no cover

        return info
