from typing import Any

import requests
from flask import g


def add_resolver_url(id_: str) -> str:
    from openatlas.display.util import link
    return link(
        f'Q{id_}',
        f'{g.reference_systems[g.wikidata.id].resolver_url}Q{id_}',
        external=True)


def fetch_wikidata(id_: str) -> dict[str, Any]:
    from openatlas.display.util import link
    url = 'https://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbgetentities',
        'ids': id_,
        'format': 'json',
        'languages': 'en'}
    info = {}
    try:
        data = requests.get(url, params=params).json()
    except:
        return {}
    try:
        info['title'] = data['entities'][id_]['labels']['en']['value']
    except:
        pass
    try:
        info['aliases'] = [
            ' ' + v['value'] for v in data['entities'][id_]['aliases']['en']]
    except:
        pass
    try:
        info['description'] = \
            data['entities'][id_]['descriptions']['en']['value']
    except:
        pass

    info['founded_by'] = [
        add_resolver_url(v['mainsnak']['datavalue']['value']['numeric-id'])
        for v in data['entities'][id_]['claims']['P112']]

    try:
        info['nick_names'] = [
            v['mainsnak']['datavalue']['value']['text']
            for v in data['entities'][id_]['claims']['P1449']]
    except:
        pass
    try:
        info['official_websites'] = [
            ' ' + link(
                v['mainsnak']['datavalue']['value'],
                v['mainsnak']['datavalue']['value'],
                external=True)
            for v in data['entities'][id_]['claims']['P856']]
    except:
        pass
    try:
        info['categories'] = [
            add_resolver_url(v['mainsnak']['datavalue']['value']['numeric-id'])
            for v in data['entities'][id_]['claims']['P910']]
    except:
        pass

    try:
        info['inception'] = \
            data['entities'][id_]['claims']['P571'][0]['mainsnak'][
                'datavalue']['value']['time']
    except:
        pass

    try:
        info['latitude'] = \
            data['entities'][id_]['claims']['P625'][0]['mainsnak'][
                'datavalue']['value']['latitude']
        info['longitude'] = \
            data['entities'][id_]['claims']['P625'][0]['mainsnak'][
                'datavalue']['value']['longitude']
    except:
        pass
    return info
