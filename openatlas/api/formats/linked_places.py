from __future__ import annotations

import mimetypes
from typing import Any, Optional

from flask import g, url_for

from openatlas.api.endpoints.parser import Parser
from openatlas.api.resources.util import (
    date_to_str, get_crm_relation, get_crm_relation_label_x,
    get_crm_relation_x, get_iiif_manifest_and_path, get_license_name,
    to_camel_case)
from openatlas.display.util import get_file_path
from openatlas.models.entity import Entity, Link


def link_dict(link_: Link, inverse: bool = False) -> dict[str, Any]:
    return {
        'label': link_.domain.name if inverse else link_.range.name,
        'relationTo':
            url_for(
                'api.entity',
                id_=link_.domain.id if inverse else link_.range.id,
                _external=True),
        'relationType': get_crm_relation(link_, inverse),
        'relationSystemClass':
            link_.domain.class_.name if inverse else link_.range.class_.name,
        'type': to_camel_case(link_.type.name) if link_.type else None,
        'relationDescription': link_.description,
        'when': {'timespans': [get_lp_time(link_)]}}


def link_dict_x(link_: Link, inverse: bool = False) -> dict[str, Any]:
    return {
        'label': link_.domain.name if inverse else link_.range.name,
        'relationTo':
            url_for(
                'api.entity',
                id_=link_.domain.id if inverse else link_.range.id,
                _external=True),
        'relationType': get_crm_relation_x(link_, inverse),
        'relationTypeLabel': get_crm_relation_label_x(link_, inverse),
        'relationSystemClass':
            link_.domain.class_.name if inverse else link_.range.class_.name,
        'type': to_camel_case(link_.type.name) if link_.type else None,
        'relationDescription': link_.description,
        'when': {'timespans': [get_lp_time(link_)]}}


def get_lp_links(
        links: list[Link],
        links_inverse: list[Link],
        parser: Parser) -> list[dict[str, str]]:
    properties = parser.relation_type or list(g.properties)
    out = []
    for link_ in links:
        if link_.property.code in properties:
            out.append(
                link_dict_x(link_) if parser.format == 'lpx'
                else link_dict(link_))
    for link_ in links_inverse:
        if link_.property.code in properties:
            out.append(
                link_dict_x(link_, inverse=True) if parser.format == 'lpx'
                else link_dict(link_, inverse=True))
    return out


def get_lp_time(entity: Entity | Link) -> Optional[dict[str, Any]]:
    return {
        'start': {
            'earliest': date_to_str(entity.dates.begin_from),
            'latest': date_to_str(entity.dates.begin_to),
            'comment': entity.dates.begin_comment},
        'end': {
            'earliest': date_to_str(entity.dates.end_from),
            'latest': date_to_str(entity.dates.end_to),
            'comment': entity.dates.end_comment}}


def get_lp_file(file: Entity) -> dict[str, Any]:
    url = 'N/A'
    mime_type = None
    if path := get_file_path(file.id):
        url = url_for('api.display', filename=path.stem, _external=True)
        mime_type, _ = mimetypes.guess_type(path)
    data = {
        '@id': url_for('api.entity', id_=file.id, _external=True),
        'title': file.name,
        'license': get_license_name(file),
        'creator': file.creator,
        'licenseHolder': file.license_holder,
        'publicShareable': file.public,
        'mimetype': mime_type,
        'url': url}
    data.update(get_iiif_manifest_and_path(file.id))
    return data
