from __future__ import annotations

import re
import threading
import time

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


_token: str | None = None
_expires = 0.0
_credentials: tuple[str, str] | None = None
_lock = threading.Lock()


def _get_token() -> str:
    global _token, _expires, _credentials  # pylint: disable=global-statement
    credentials = (
        app.config.get('ORCID_CLIENT_ID', ''),
        app.config.get('ORCID_CLIENT_SECRET', ''))
    if not all(credentials):
        raise ValueError('ORCID client credentials are not configured')
    with _lock:
        if _token and _credentials == credentials and time.monotonic() < _expires:
            return _token
        response = requests.post(
            'https://orcid.org/oauth/token',
            data={
                'client_id': credentials[0],
                'client_secret': credentials[1],
                'grant_type': 'client_credentials',
                'scope': '/read-public'},
            headers={'Accept': 'application/json', **app.config['USER_AGENT']},
            proxies=app.config['PROXIES'],
            timeout=10)
        response.raise_for_status()
        data = response.json()
        token = data['access_token']
        _expires = time.monotonic() + max(0, int(data.get('expires_in', 3600)) - 60)
        _token = token
        _credentials = credentials
        return token


def _request(path: str, params: dict[str, object] | None = None) -> object:
    global _token, _expires  # pylint: disable=global-statement
    for attempt in range(2):
        token = _get_token()
        response = requests.get(
            f'https://pub.orcid.org/v3.0/{path}',
            params=params,
            headers={
                **app.config['USER_AGENT'],
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'},
            proxies=app.config['PROXIES'],
            timeout=10)
        if response.status_code == 401 and not attempt:
            with _lock:
                if _token == token:
                    _token = None
                    _expires = 0.0
            continue
        response.raise_for_status()
        return response.json()
    raise RuntimeError('ORCID request failed')  # pragma: no cover


def search(query: str) -> list[dict[str, str]]:
    terms = [re.sub(r'[^\w]', '', word, flags=re.UNICODE).replace('_', '')
             for word in query.strip().split()]
    terms = [term for term in terms if term]
    if not terms:
        return []
    try:
        data = _request(
            'expanded-search/',
            {'q': ' AND '.join(
                f'(given-names:{term}* OR family-names:{term}* OR '
                f'credit-name:{term}*)' for term in terms),
             'rows': 15})
    except (requests.RequestException, ValueError):
        return []
    if not isinstance(data, dict):
        return []
    results = []
    for item in data.get('expanded-result') or []:
        if not isinstance(item, dict) or not item.get('orcid-id'):
            continue
        identifier = item['orcid-id']
        name = ' '.join(filter(None, [
            item.get('given-names'), item.get('family-names')]))
        institutions = item.get('institution-name') or []
        label = name or item.get('credit-name') or identifier
        if institutions:
            label += f" ({', '.join(institutions[:2])})"
        results.append({
            'id': identifier,
            'label': label,
            'info': '',
            'detail': ''})
    return results


class ORCID(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        if not re.fullmatch(r'\d{4}-\d{4}-\d{4}-\d{3}[\dX]', id_):
            return {}
        try:
            data = _request(f'{id_}/person')
            if not isinstance(data, dict):
                return {}
            name = data.get('name') or {}
            given = (name.get('given-names') or {}).get('value', '')
            family = (name.get('family-name') or {}).get('value', '')
            title = ' '.join(filter(None, [given, family]))
            info: dict[str, object] = {
                'ORCID ID': link(id_, f'https://orcid.org/{id_}', external=True)}
            if title:
                info['title'] = title
            return info
        except (requests.RequestException, ValueError, KeyError, TypeError):
            return {}