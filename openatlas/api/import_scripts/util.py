from typing import Any, Optional

import requests
from flask import g

from openatlas import app
from openatlas.models.entity import Entity, insert


def get_or_create_type(hierarchy: Any, type_name: str) -> Entity:
    if type_ := get_type_by_name(type_name):
        if type_.root[0] == hierarchy.id:
            return type_
    type_entity = insert({'openatlas_class_name': 'type', 'name': type_name})
    type_entity.link('P127', hierarchy)
    return type_entity


def get_type_by_name(type_name: str) -> Optional[Entity]:
    type_ = None
    for type_id in g.types:
        if g.types[type_id].name == type_name:
            type_ = g.types[type_id]
            break
    return type_


def get_reference_system_by_name(name: str) -> Optional[Entity]:
    reference_system = None
    name = name.lower().replace('_', ' ')
    for id_ in g.reference_systems:
        if g.reference_systems[id_].name.lower().replace('_', ' ') == name:
            reference_system = g.reference_systems[id_]
            break
    return reference_system


def get_exact_match() -> Entity:
    return get_or_create_type(g.reference_match_type, 'exact match')


def get_match_types() -> dict[str, Entity]:
    match_dictionary = {}
    for match in [g.types[match] for match in g.reference_match_type.subs]:
        match match.name:
            case 'exact match':
                match_dictionary['exact_match'] = match
            case 'close match':
                match_dictionary['close_match'] = match
    return match_dictionary


def vocabs_requests(
        id_: Optional[str] = '',
        endpoint: Optional[str] = '',
        parameter: Optional[dict[str, str]] = None) -> dict[str, Any]:
    req = requests.get(
        f"{g.settings['vocabs_base_url']}{g.settings['vocabs_endpoint']}{id_}/"
        f"{endpoint}",
        params=parameter or '',
        timeout=60,
        auth=(g.settings['vocabs_user'], app.config['VOCABS_PASS']))
    return req.json()


def request_arche_metadata(id_: int) -> dict[str, Any]:
    req = requests.get(
        f"{app.config['ARCHE']['url']}/api/{id_}/metadata",
        headers={
            'Accept': 'application/ld+json',
            'X-METADATA-READ-MODE': '1_1_0_0'},
        timeout=60)
    return req.json()
