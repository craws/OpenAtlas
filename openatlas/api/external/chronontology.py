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
            return {}

        info: dict[str, object] = {}
        resource = data.get('resource', {})

        names = resource.get('names', {})
        if en_names := names.get('en'):
            info['title'] = en_names[0]
        elif de_names := names.get('de'):  # pragma: no cover
            info['title'] = de_names[0]
        else:
            info['title'] = f"ChronOntology Period {id_}"  # pragma: no cover

        if definition := resource.get('definition'):
            info['definition'] = definition

        if (timespans := resource.get('hasTimespan')) \
                and isinstance(timespans, list):
            if time_orig := timespans[0].get('timeOriginal'):
                info['timespan'] = time_orig

        if types := resource.get('types'):
            info['period types'] = ', '.join(types) \
                if isinstance(types,list) else str(types)

        if gazetteer := ChronOntology.get_gazetteer_links(data.get('related')):
            info['gazetteer'] = gazetteer

        return info

    @staticmethod
    def get_gazetteer_links(related: Any) -> list[str]:
        if not isinstance(related, dict):
            return []  # pragma: no cover

        links: list[str] = []
        for key, place in related.items():
            if 'gazetteer.dainst.org/place/' not in str(key) \
                    or not isinstance(place, dict):
                continue  # pragma: no cover

            english_name = ''

            for name in place.get('names', []):
                if isinstance(name, dict) \
                        and name.get('language') == 'eng' \
                        and (title := name.get('title')):
                    english_name = str(title)
                    break

            if not english_name:
                pref = place.get('prefName', {})
                if isinstance(pref, dict) \
                        and pref.get('language') == 'eng' \
                        and (title := pref.get('title')):
                    english_name = str(title)

            if not english_name:
                continue  # pragma: no cover

            place_id = str(key).rstrip('/').rsplit('/', maxsplit=1)[-1]
            if place_id:
                links.append(link(
                    english_name,
                    f'https://gazetteer.dainst.org/place/{place_id}',
                    external=True))

        return links
