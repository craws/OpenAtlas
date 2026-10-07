from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class VIAF(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        try:
            data = requests.get(
                f'https://viaf.org/viaf/{id_}',
                headers={
                    'Accept': 'application/json',
                    **app.config['USER_AGENT']},
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return {}

        viaf_data = data.get('ns1:VIAFCluster', {})
        if not viaf_data:
            return {}  # pragma: no cover

        info: dict[str, object] = {}

        if viaf_id := viaf_data.get('ns1:viafID'):
            info['VIAF ID'] = link(
                str(viaf_id),
                f'https://viaf.org/viaf/{viaf_id}',
                external=True)

        headings = viaf_data.get('ns1:mainHeadings', {}).get('ns1:data', [])
        if isinstance(headings, list) and headings:
            if text := headings[0].get('ns1:text'):
                info['title'] = text
        elif isinstance(headings, dict):  # pragma: no cover
            if text := headings.get('ns1:text'):
                info['title'] = text

        if name_type := viaf_data.get('ns1:nameType'):
            info['type'] = name_type

        if (birth_date := viaf_data.get('ns1:birthDate')) is not None \
                and str(birth_date) != '0':
            info['birth date'] = str(birth_date)

        if (death_date := viaf_data.get('ns1:deathDate')) is not None \
                and str(death_date) != '0':
            info['death date'] = str(death_date)

        return info
