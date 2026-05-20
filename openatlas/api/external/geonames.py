import requests
import xmltodict
from flask import g

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.models.entity import Entity


class GeoNames(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        params = {
            'geonameId': {id_},
            'username': {g.settings['geonames_username']}}
        try:
            data = requests.get(
                'http://api.geonames.org/get',
                params=params,
                proxies=app.config['PROXIES'],
                timeout=10).content
            data_dict = xmltodict.parse(data)['geoname']
        except Exception:  # pragma: no cover
            return {}
        info: dict[str, object] = {}
        for key, value in data_dict.items():
            if key == 'alternateNames' and value:
                info[key] = '<br>'.join(value.split(','))
            elif isinstance(value, str):
                info[key] = value
        return info
