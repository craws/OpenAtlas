from __future__ import annotations

from typing import Any

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class Kulturpool(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        info: dict[str, object] = {}
        try:
            response = requests.get(
                f'https://api.kulturpool.at/object/?id={id_}',
                headers=app.config['USER_AGENT'],
                proxies=app.config['PROXIES'],
                timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception:  # pragma: no cover
            return info

        metadata = data.get('metadata', {})
        agg_data = metadata.get('aggregatedCHO', {})

        def get_value(field_data: Any) -> str | None:
            if isinstance(field_data, list) and field_data:
                field_data = field_data[0]
            if isinstance(field_data, dict):
                return field_data.get('@value')
            return str(field_data) if field_data else None

        title = get_value(agg_data.get('title'))
        if title:
            info['title'] = title

        creators = agg_data.get('creator', [])
        if creators:
            creator_names = []
            for creator in creators:
                if isinstance(creator, dict):
                    name = get_value(creator.get('prefLabel'))
                    if name:
                        creator_names.append(name)
                elif isinstance(creator, str):  #pragma: no cover
                    creator_names.append(creator)
            if creator_names:
                info['creators'] = '; '.join(creator_names)

        date = get_value(agg_data.get('temporal')) \
               or get_value(agg_data.get('created'))
        if date:
            info['date'] = date

        if description := get_value(agg_data.get('description')):
            info['description'] = description

        obj_type = agg_data.get('edmType') or get_value(agg_data.get('dcType'))
        if obj_type:
            info['type'] = obj_type

        provider = get_value(metadata.get('dataProvider')) or \
            get_value(metadata.get('provider'))
        if provider:
            info['provider'] = provider

        info['Kulturpool'] = link(
            id_,
            f'https://kulturpool.at/objekte/{id_}',
            uc_first_=False,
            external=True)

        publisher = get_value(agg_data.get('publisher'))
        if publisher:
            info['publisher'] = publisher

        return info
