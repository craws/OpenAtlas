from __future__ import annotations

from html import escape
from typing import Any
from urllib.parse import quote

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class ROR(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def search(term: str) -> list[dict[str, object]]:
        response = requests.get(
            'https://api.ror.org/v2/organizations',
            params={'query': term},
            headers=app.config['USER_AGENT'],
            proxies=app.config['PROXIES'],
            timeout=10)
        response.raise_for_status()

        results = []
        for item in response.json().get('items', [])[:15]:
            names = item.get('names') or []
            display_name = next((
                name.get('value') for name in names
                if 'ror_display' in (name.get('types') or [])
                and name.get('value')), '')
            if not display_name and names:  # pragma: no cover
                display_name = names[0].get('value', '')

            full_id = item.get('id', '')
            identifier = full_id.rsplit('/', 1)[-1] if full_id else ''
            if not identifier:  # pragma: no cover
                continue

            acronym = next((
                name.get('value') for name in names
                if 'acronym' in (name.get('types') or [])
                and name.get('value')), '')
            locations = item.get('locations') or []
            geonames_details = (locations[0].get('geonames_details') or {}) \
                if locations else {}
            types = item.get('types') or []
            results.append({
                'id': identifier,
                'name': display_name or identifier,
                'acronym': acronym,
                'city': geonames_details.get('name', ''),
                'country': geonames_details.get('country_name', ''),
                'types': types if isinstance(types, list) else [],
                'url': f'https://ror.org/{identifier}'})
        return results

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        try:
            response = requests.get(
                f'https://api.ror.org/v2/organizations/{quote(id_, safe="")}',
                headers=app.config['USER_AGENT'],
                proxies=app.config['PROXIES'],
                timeout=10)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        except requests.exceptions.RequestException:
            return {}

        names = data.get('names') or []
        display_name = next((
            name.get('value') for name in names
            if 'ror_display' in (name.get('types') or [])
            and name.get('value')), '')
        if not display_name and names:  # pragma: no cover
            display_name = names[0].get('value', '')

        info: dict[str, object] = {}
        info['ROR ID'] = link(
            escape(id_),
            f'{system.resolver_url}{quote(id_, safe="")}',
            uc_first_=False,
            external=True)
        if display_name:
            info['name'] = display_name
        if acronym := next((
                name.get('value') for name in names
                if 'acronym' in (name.get('types') or [])
                and name.get('value')), ''):
            info['acronym'] = acronym

        locations = data.get('locations') or []
        if locations:
            details = locations[0].get('geonames_details') or {}
            location = ', '.join(filter(None, [
                details.get('name'), details.get('country_name')]))
            if location:
                info['location'] = location

        if types := data.get('types'):
            info['type'] = ', '.join(types)
        return info
