from typing import Any
import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class Wikidata(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        params = {
            'action': 'wbgetentities',
            'ids': id_,
            'format': 'json',
            'languages': 'en'}
        try:
            data = requests.get(
                'https://www.wikidata.org/w/api.php',
                headers=app.config['USER_AGENT'],
                params=params,
                proxies=app.config['PROXIES'],
                timeout=10).json()
            wiki = data['entities'][id_]
        except Exception:  # pragma: no cover
            return {}

        def add_resolver_url(numeric_id: int | str) -> str:
            return link(
                f'Q{numeric_id}',
                f'{system.resolver_url}Q{numeric_id}',
                external=True)

        def claim_values(property_: str) -> list[Any]:
            values = []
            claims = wiki.get('claims', {}).get(property_, [])
            for claim in claims:
                if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                    values.append(claim['mainsnak']['datavalue']['value'])
            return values

        info: dict[str, object] = {}

        if label := wiki.get('labels', {}).get('en', {}).get('value'):
            info['title'] = label
        if aliases := [
                a['value'] for a in wiki.get('aliases', {}).get('en', [])]:
            info['aliases'] = [f' {a}' for a in aliases]
        if desc := wiki.get('descriptions', {}).get('en', {}).get('value'):
            info['description'] = desc
        if founders := claim_values('P112'):
            info['founded by'] = [
                add_resolver_url(f['numeric-id']) for f in founders]
        if nicknames := claim_values('P1449'):  # pragma: no cover
            info['nick names'] = [n['text'] for n in nicknames]
        if websites := claim_values('P856'):
            info['official websites'] = [
                f' {link(w, w, external=True)}' for w in websites]
        if categories := claim_values('P910'):
            info['categories'] = [
                add_resolver_url(c['numeric-id']) for c in categories]
        if inception := claim_values('P571'):
            info['inception'] = inception[0]['time']
        if coords := claim_values('P625'):
            info['latitude'] = coords[0]['latitude']
            info['longitude'] = coords[0]['longitude']

        return info