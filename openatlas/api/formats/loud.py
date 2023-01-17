from collections import defaultdict
from typing import Any

from flask import url_for

from openatlas.api.formats.linked_places import relation_type
from openatlas.api.resources.util import remove_spaces_dashes
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.type import Type


def get_loud_entities(
        data: dict[str, Any],
        parser: dict[str, Any],
        loud: dict[str, str]) -> Any:
    properties_dict = defaultdict(list)
    # Set name to properties
    properties_dict['identified_by'] = [{
        "type": "Name",
        "content": data['entity'].name}]
    for link_ in data['links']:
        if link_.property.code in ['OA7', 'OA8', 'OA9']:
            continue
        property_name = loud[relation_type(link_).replace(' ', '_')]
        base_property = get_base_property(link_)
        properties_dict[property_name].append(base_property)

    for link_ in data['links_inverse']:
        if link_.property.code in ['OA7', 'OA8', 'OA9']:
            continue
        property_name = loud[relation_type(link_, True).replace(' ', '_')]
        base_property = get_base_property_inverse(link_)
        properties_dict[property_name].append(base_property)

    dict_ = {
        '@context': "https://linked.art/ns/v1/linked-art.json",
        'id': url_for('view', id_=data['entity'].id, _external=True),
        'type': remove_spaces_dashes(data['entity'].cidoc_class.i18n['en']),
        '_label': data['entity'].name,
        'content': data['entity'].description,
        'timespan': get_loud_timespan(data['entity']),
    }

    return dict_ | properties_dict


def get_loud_timespan(entity: Entity) -> dict[str, Any]:
    return {
        'type': 'TimeSpan',
        'begin_of_the_begin': date_to_str(entity.begin_from),
        'end_of_the_begin': date_to_str(entity.begin_to),
        'begin_of_the_end': date_to_str(entity.end_from),
        'end_of_the_end': date_to_str(entity.end_to)}


# can be removed if correctly mapped
def date_to_str(date: Any) -> str:
    return str(date) if date else None


def get_base_property(link_: Link) -> dict[str, Any]:
    property_ = {
        'id': url_for('view', id_=link_.range.id, _external=True),
        'type': remove_spaces_dashes(link_.range.cidoc_class.i18n['en']),
        '_label': link_.range.name}
    if type_ := get_standard_type_loud(link_.range.types):
        property_['classified_as'] = get_type_property(type_)
    return property_


def get_base_property_inverse(link_: Link) -> dict[str, Any]:
    property_ = {
        'id': url_for('view', id_=link_.domain.id, _external=True),
        'type': remove_spaces_dashes(link_.domain.cidoc_class.i18n['en']),
        '_label': link_.domain.name, }
    if type_ := get_standard_type_loud(link_.domain.types):
        property_['classified_as'] = get_type_property(type_)
    return property_


def get_type_property(type_: Type) -> dict[str, Any]:
    return {
        'id': url_for('view', id_=type_.id, _external=True),
        'type': remove_spaces_dashes(type_.cidoc_class.i18n['en']),
        '_label': type_.name}


def get_standard_type_loud(types: dict[Type, Any]) -> Type:
    standard = None
    for type_ in types:
        if type_.category == 'standard':
            standard = type_
    return standard
