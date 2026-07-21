from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class VIAF(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        info: dict[str, object] = {}
        try:
            data = requests.get(
                f'https://viaf.org/viaf/{id_}',
                headers={
                    'Accept': 'application/json',
                    **app.config['USER_AGENT']},
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return info

        if 'ns1:VIAFCluster' in data:
            viaf_data = data['ns1:VIAFCluster']

            if 'ns1:viafID' in viaf_data:
                viaf_id = str(viaf_data['ns1:viafID'])
                info['VIAF ID'] = link(
                    viaf_id,
                    f'https://viaf.org/viaf/{str(viaf_data['ns1:viafID'])}',
                    external=True)

            headings = viaf_data.get(
                'ns1:mainHeadings', {}).get('ns1:data', [])
            if isinstance(headings, list) and headings:
                info['title'] = headings[0].get('ns1:text', '')
            elif isinstance(headings, dict):  # pragma: no cover
                info['title'] = headings.get('ns1:text', '')

            if 'ns1:nameType' in viaf_data:
                info['type'] = viaf_data['ns1:nameType']

            if 'ns1:birthDate' in viaf_data \
                    and str(viaf_data['ns1:birthDate']) != '0':
                info['birth date'] = str(viaf_data['ns1:birthDate'])
            if 'ns1:deathDate' in viaf_data \
                    and str(viaf_data['ns1:deathDate']) != '0':
                info['death date'] = str(viaf_data['ns1:deathDate'])


        return info
