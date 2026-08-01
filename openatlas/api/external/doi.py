from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class DOI(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        info: dict[str, object] = {}
        try:
            data = requests.get(
                f'https://doi.org/{id_}',
                headers={
                    'Accept': 'application/vnd.citationstyles.csl+json',
                    **app.config['USER_AGENT']},
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return info

        if 'title' in data and data['title']:
            info['title'] = data['title']

        if 'author' in data:
            authors = []
            for author in data['author']:
                name = []
                if 'family' in author:
                    name.append(author['family'])
                if 'given' in author:
                    name.append(author['given'])
                elif 'literal' in author:  # pragma: no cover
                    name.append(author['literal'])
                authors.append(', '.join(name))
            info['authors'] = '; '.join(authors)

        if 'container-title' in data and data['container-title']:
            info['container'] = data['container-title']

        if 'publisher' in data:
            info['publisher'] = data['publisher']

        year = None
        for date_field in [
            'issued', 'published-print', 'published-online', 'published']:
            if date_field in data and 'date-parts' in data[date_field]:
                try:
                    year = data[date_field]['date-parts'][0][0]
                    if year:
                        break
                except (IndexError, TypeError):  # pragma: no cover
                    continue
        if year:
            info['year'] = year

        if 'DOI' in data:
            info['DOI'] = link(
                data['DOI'],
                f'https://doi.org/{data["DOI"]}',
                external=True)

        if 'type' in data:
            info['type'] = data['type'].replace('-', ' ').title()

        if 'page' in data:
            info['page'] = data['page']

        if 'volume' in data:
            info['volume'] = data['volume']

        if 'issue' in data:
            info['issue'] = data['issue']

        return info
