from typing import Any

import requests
from flask import g

from openatlas import app
from openatlas.display.util import link


def add_resolver_url(id_: str) -> str:
    return link(f'Q{id_}', f'{g.wikidata.resolver_url}Q{id_}', external=True)


def fetch_wikidata(id_: str) -> dict[str, Any]:
    params = {
        'action': 'wbgetentities',
        'ids': id_,
        'format': 'json',
        'languages': 'en'}
    info = {}
    try:
        data = requests.get(
            app.config['API_WIKIDATA'],
            params=params,
            proxies=app.config['PROXIES'],
            timeout=10).json()
    except Exception:  # pragma: no cover
        return {}
    try:
        info['title'] = data['entities'][id_]['labels']['en']['value']
    except Exception:  # pragma: no cover
        pass
    try:
        info['aliases'] = [
            ' ' + v['value'] for v in data['entities'][id_]['aliases']['en']]
    except Exception:  # pragma: no cover
        pass
    try:
        info['description'] = \
            data['entities'][id_]['descriptions']['en']['value']
    except Exception:  # pragma: no cover
        pass
    try:
        info['founded by'] = [
            add_resolver_url(v['mainsnak']['datavalue']['value']['numeric-id'])
            for v in data['entities'][id_]['claims']['P112']]
    except Exception:
        pass
    try:
        info['nick names'] = [
            v['mainsnak']['datavalue']['value']['text']
            for v in data['entities'][id_]['claims']['P1449']]
    except Exception:
        pass
    try:
        info['official websites'] = [
            ' ' + link(
                v['mainsnak']['datavalue']['value'],
                v['mainsnak']['datavalue']['value'],
                external=True)
            for v in data['entities'][id_]['claims']['P856']]
    except Exception:  # pragma: no cover
        pass
    try:
        info['categories'] = [
            add_resolver_url(v['mainsnak']['datavalue']['value']['numeric-id'])
            for v in data['entities'][id_]['claims']['P910']]
    except Exception:  # pragma: no cover
        pass
    try:
        info['inception'] = \
            data['entities'][id_]['claims']['P571'][0]['mainsnak'][
                'datavalue']['value']['time']
    except Exception:  # pragma: no cover
        pass
    try:
        info['latitude'] = \
            data['entities'][id_]['claims']['P625'][0]['mainsnak'][
                'datavalue']['value']['latitude']
        info['longitude'] = \
            data['entities'][id_]['claims']['P625'][0]['mainsnak'][
                'datavalue']['value']['longitude']
    except Exception:  # pragma: no cover
        pass
    return info
