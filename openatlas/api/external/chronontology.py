from __future__ import annotations

from typing import Any

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class ChronOntology(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        info: dict[str, object] = {}

        try:
            response = requests.get(
                f'https://chronontology.dainst.org/data/period/{id_}',
                headers={
                    'Accept': 'application/json',
                    **app.config['USER_AGENT']},
                proxies=app.config['PROXIES'],
                timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception:  # pragma: no cover
            return info

        resource = data.get('resource', {})

        names = resource.get('names', {})
        title = None
        if 'en' in names and names['en']:
            title = names['en'][0]
        elif 'de' in names and names['de']:  # pragma: no cover
            title = names['de'][0]

        info['title'] = title or f"ChronOntology Period {id_}"

        info['definition'] = resource.get('definition')

        timespans = resource.get('hasTimespan', [])
        if timespans and isinstance(timespans, list):
            info['timespan'] = timespans[0]['timeOriginal']

        types = resource.get('types', [])
        if types:
            info['period types'] = ', '.join(types)

        if gazetteer := ChronOntology.get_gazetteer_links(data.get('related')):
            info['gazetteer'] = gazetteer

        return info

    @staticmethod
    def get_gazetteer_links(related: Any) -> list[str]:
        links: list[str] = []
        if not isinstance(related, dict):
            return links  # pragma: no cover

        for key, place in related.items():
            if 'gazetteer.dainst.org/place/' not in str(key):
                continue  # pragma: no cover
            if not isinstance(place, dict):
                continue  # pragma: no cover

            english_name = ''
            for name in place.get('names', []):
                if not isinstance(name, dict):
                    continue  # pragma: no cover
                if name.get('language') == 'eng' and name.get('title'):
                    english_name = str(name['title'])
                    break

            if not english_name \
                    and isinstance(place.get('prefName'), dict) \
                    and place['prefName'].get('language') == 'eng' \
                    and place['prefName'].get('title'):
                english_name = str(place['prefName']['title'])

            if not english_name:
                continue  # pragma: no cover

            place_id = str(key).rstrip('/').rsplit('/', maxsplit=1)[-1]
            if not place_id:
                continue  # pragma: no cover

            links.append(link(
                english_name,
                f'https://gazetteer.dainst.org/place/{place_id}',
                external=True))

        return links
