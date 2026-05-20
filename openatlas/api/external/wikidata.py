import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class Wikidata(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        def add_resolver_url(wikidata_id: str) -> str:
            return link(
                f'Q{wikidata_id}',
                f'{system.resolver_url}Q{wikidata_id}',
                external=True)

        params = {
            'action': 'wbgetentities',
            'ids': id_,
            'format': 'json',
            'languages': 'en'}
        info = {}
        try:
            data = requests.get(
                'https://www.wikidata.org/w/api.php',
                headers=app.config['USER_AGENT'],
                params=params,
                proxies=app.config['PROXIES'],
                timeout=10).json()
        except Exception:  # pragma: no cover
            return {}
        try:
            info['title'] = data['entities'][id_]['labels']['en']['value']
        except KeyError:  # pragma: no cover
            pass
        try:
            info['aliases'] = [
                ' ' + v['value']
                for v in data['entities'][id_]['aliases']['en']]
        except KeyError:  # pragma: no cover
            pass
        try:
            info['description'] = \
                data['entities'][id_]['descriptions']['en']['value']
        except KeyError:  # pragma: no cover
            pass
        try:
            info['founded by'] = [
                add_resolver_url(
                    v['mainsnak']['datavalue']['value']['numeric-id'])
                for v in data['entities'][id_]['claims']['P112']]
        except KeyError:  # pragma: no cover
            pass
        try:
            info['nick names'] = [
                v['mainsnak']['datavalue']['value']['text']
                for v in data['entities'][id_]['claims']['P1449']]
        except KeyError:
            pass
        try:
            info['official websites'] = [
                ' ' + link(
                    v['mainsnak']['datavalue']['value'],
                    v['mainsnak']['datavalue']['value'],
                    external=True)
                for v in data['entities'][id_]['claims']['P856']]
        except KeyError:  # pragma: no cover
            pass
        try:
            info['categories'] = [
                add_resolver_url(
                    v['mainsnak']['datavalue']['value']['numeric-id'])
                for v in data['entities'][id_]['claims']['P910']]
        except KeyError:  # pragma: no cover
            pass
        try:
            info['inception'] = \
                data['entities'][id_]['claims']['P571'][0]['mainsnak'][
                    'datavalue']['value']['time']
        except KeyError:  # pragma: no cover
            pass
        try:
            info['latitude'] = \
                data['entities'][id_]['claims']['P625'][0]['mainsnak'][
                    'datavalue']['value']['latitude']
            info['longitude'] = \
                data['entities'][id_]['claims']['P625'][0]['mainsnak'][
                    'datavalue']['value']['longitude']
        except KeyError:  # pragma: no cover
            pass
        return info
