from __future__ import annotations

from html import escape
from typing import Any
from urllib.parse import quote

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class ORCID(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def search(term: str) -> list[dict[str, object]]:
        response = requests.get(
            'https://pub.orcid.org/v3.0/expanded-search/',
            params={'q': term, 'rows': 15},
            headers={
                'Accept': 'application/json',
                **app.config['USER_AGENT']},
            proxies=app.config['PROXIES'],
            timeout=10)
        response.raise_for_status()

        results: list[dict[str, object]] = []
        for item in (response.json().get('expanded-result') or [])[:15]:
            identifier = item.get('orcid-id', '')
            if not identifier:  # pragma: no cover
                continue

            given = item.get('given-names') or ''
            family = item.get('family-names') or ''
            full_name = ' '.join(filter(None, [given, family]))
            if not full_name:  # pragma: no cover
                full_name = item.get('credit-name') or ''

            institutions = item.get('institution-name') or []
            other_names = item.get('other-name') or []
            results.append({
                'id': identifier,
                'name': full_name or identifier,
                'other_names':
                    other_names if isinstance(other_names, list) else [],
                'institutions':
                    institutions[:3] if isinstance(institutions, list) else [],
                'url': f'https://orcid.org/{identifier}'})
        return results

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        try:
            response = requests.get(
                f'https://pub.orcid.org/v3.0/{quote(id_, safe="")}/person',
                headers={
                    'Accept': 'application/json',
                    **app.config['USER_AGENT']},
                proxies=app.config['PROXIES'],
                timeout=10)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        except requests.exceptions.RequestException:
            return {}

        name = data.get('name') or {}
        given = (name.get('given-names') or {}).get('value', '')
        family = (name.get('family-name') or {}).get('value', '')
        display_name = ' '.join(filter(None, [given, family]))
        if not display_name:  # pragma: no cover
            display_name = (name.get('credit-name') or {}).get('value', '')

        info: dict[str, object] = {}
        info['ORCID ID'] = link(
            escape(id_),
            f'{system.resolver_url}{quote(id_, safe="")}',
            uc_first_=False,
            external=True)
        if display_name:
            info['name'] = escape(display_name)

        emails = (data.get('emails') or {}).get('email') or []
        if emails and (email := emails[0].get('email')):
            info['email'] = escape(email)

        addresses = (data.get('addresses') or {}).get('address') or []
        if addresses and (
                country := (addresses[0].get('country') or {}).get('value')):
            info['country'] = escape(country)

        return info
