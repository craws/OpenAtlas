import requests
from shapely.geometry import shape

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class Cadaster(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        endpoint = 'gst/' if '/' in id_ else 'kgnr/'
        try:
            data = requests.get(
                f'https://kataster.bev.gv.at/api/{endpoint}{id_}',
                headers=app.config['USER_AGENT'],
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return {}

        info: dict[str, object] = {}

        if error_msg := data.get('message'):
            info['Error'] = error_msg
            return info

        properties = data.get('properties', {})

        if kg := properties.get('kg'):
            info['katestralgemeinde'] = kg

        if bl := properties.get('bl'):
            info['bundesland'] = bl  # pragma: no cover

        if gnr := properties.get('gnr'):
            info['grundstücksnummer'] = gnr

        if ez := properties.get('ez'):
            info['einlagezahl'] = ez

        if rstatus := properties.get('rstatus'):
            info['rstatus'] = rstatus

        if nutzungen := properties.get('nutzungen'):
            info['nutzungen'] = [
                f'Allocation: {usage.get("nutzung", "")}, ' \
                f'Area: {usage.get("fl", "")}m²'
                for usage in nutzungen]

        if geometry_data := data.get('geometry'):
            try:
                geom = shape(geometry_data).centroid
                zoom = '18.1' if '/' in id_ else '12.9'
                url = f'https://kataster.bev.gv.at/#/center/' \
                      f'{geom.x},{geom.y}/zoom/{zoom}/vermv/0.6'
                info['geometry'] = link(url, url, external=True)
            except Exception:  # pragma: no cover
                pass

        return info
