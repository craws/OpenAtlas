from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class DOI(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        try:
            data = requests.get(
                f'https://doi.org/{id_}',
                headers={
                    'Accept': 'application/vnd.citationstyles.csl+json',
                    **app.config['USER_AGENT']},
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return {}

        info: dict[str, object] = {}

        if title := data.get('title'):
            info['title'] = title

        if raw_authors := data.get('author', []):
            authors = []
            for author in raw_authors:
                name = []
                if family := author.get('family'):
                    name.append(family)
                if given := author.get('given'):
                    name.append(given)
                elif literal := author.get('literal'):  # pragma: no cover
                    name.append(literal)
                if name:
                    authors.append(', '.join(name))
            if authors:
                info['authors'] = '; '.join(authors)

        if container := data.get('container-title'):
            info['container'] = container

        if publisher := data.get('publisher'):
            info['publisher'] = publisher

        for date_field in [
                'issued', 'published-print', 'published-online', 'published']:
            if date_obj := data.get(date_field):
                parts = date_obj.get('date-parts', [])
                if parts and isinstance(parts[0], list) and parts[0]:
                    if year := parts[0][0]:
                        info['year'] = year
                        break

        if doi := data.get('DOI'):
            info['DOI'] = link(doi, f'https://doi.org/{doi}', external=True)

        if doc_type := data.get('type'):
            info['type'] = doc_type.replace('-', ' ').title()

        if page := data.get('page'):
            info['page'] = page

        if volume := data.get('volume'):
            info['volume'] = volume

        if issue := data.get('issue'):
            info['issue'] = issue

        return info
