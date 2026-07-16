from __future__ import annotations

from typing import Any

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class GettyAAT(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:

        info: dict[str, object] = {}
        try:
            response = requests.get(
                f'https://vocab.getty.edu/aat/{id_}.json',
                headers={
                    'Accept': 'application/json',
                    **app.config['USER_AGENT']
                },
                proxies=app.config['PROXIES'],
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except Exception:  # pragma: no cover
            return info

        if label := data.get('_label'):
            info['title'] = label

        if broader := GettyAAT.get_links(data.get('broader')):
            info['broader'] = broader

        if equivalent := GettyAAT.get_links(data.get('equivalent')):
            info['equivalent'] = equivalent

        if scope_note := GettyAAT.get_scope_note(data.get('subject_of')):
            info['scope note'] = scope_note

        return info

    @staticmethod
    def get_links(items: Any) -> list[str]:
        links = []
        for item in items or []:
            if (id_ := item.get('id')) and (label := item.get('_label')):
                links.append(link(label, id_, external=True))
        return links

    @staticmethod
    def get_scope_note(items: Any) -> str:
        for item in items or []:
            languages = [
                lang.get('_label') for lang in item.get('language', [])]
            if 'en' in languages and (content := item.get('content')):
                return content
        return ''  # pragma: no cover
