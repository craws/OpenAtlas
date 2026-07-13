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
        def as_list(value: Any) -> list[Any]:
            if value is None:
                return []
            if isinstance(value, list):
                return value
            return [value]

        def get_item_link(item: Any) -> str | None:
            if isinstance(item, dict):
                uri = item.get('id') or item.get('@id')
                if not uri:
                    return None
                return link(item.get('_label') or uri, uri, external=True)
            if isinstance(item, str) and item.startswith('http'):
                return link(item, item, external=True)
            return None

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

        if notes := data.get('subject_of'):
            for note in as_list(notes):
                if isinstance(note, dict):
                    if note.get('language')[0]['_label'] == 'en':
                        info['note'] = note.get('content')
                        break
                    elif 'content' in note:
                        info['note'] = note['content']

        broader_links = [
            value for value in (
                get_item_link(item)
                for item in as_list(data.get('broader')))
            if value]
        if broader_links:
            info['broader terms'] = broader_links

        equivalent_links = [
            value for value in (
                get_item_link(item)
                for item in as_list(data.get('equivalent')))
            if value]
        if equivalent_links:
            info['equivalent terms'] = equivalent_links

        info['Getty AAT'] = link(
            id_,
            f'https://vocab.getty.edu/page/aat/{id_}',
            external=True)

        return info
