import mimetypes
from collections import defaultdict
from typing import Any, Optional

from flask import url_for, g

from openatlas import app
from openatlas.api.resources.util import (
    remove_spaces_dashes, date_to_str, get_crm_relation, get_crm_code)
from openatlas.display.util import get_file_path
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.type import Type


def get_loud_entities(data: dict[str, Any], loud: dict[str, str]) -> Any:
    properties_set = defaultdict(list)

    def base_entity_dict() -> dict[str, Any]:
        return {
            'id': url_for('view', id_=data['entity'].id, _external=True),
            'type': remove_spaces_dashes(
                data['entity'].cidoc_class.i18n['en']),
            '_label': data['entity'].name,
            'content': data['entity'].description,
            'timespan': get_loud_timespan(data['entity']),
            'identified_by': [{
                "type": "Name",
                "content": data['entity'].name}]}

    def get_range_links() -> dict[str, Any]:
        return {
            'id': url_for('api.entity', id_=link_.range.id, _external=True),
            'type': loud[get_crm_code(link_).replace(' ', '_')],
            '_label': link_.range.name}

    def get_domain_links() -> dict[str, Any]:
        property_ = {
            'id': url_for('api.entity', id_=link_.domain.id, _external=True),
            'type': loud[get_crm_code(link_, True).replace(' ', '_')],
            '_label': link_.domain.name}
        if standard_type := get_standard_type_loud(link_.domain.types):
            property_['classified_as'] = get_type_property(standard_type)
        return property_

    for link_ in data['links']:
        if link_.property.code in ['OA7', 'OA8', 'OA9']:
            continue
        if link_.property.code == 'P127':
            property_name = 'broader'
        else:
            property_name = loud[get_crm_relation(link_).replace(' ', '_')]
        if link_.property.code == 'P53':
            for geom in Gis.get_wkt_by_id(link_.range.id):
                base_property = get_range_links() | geom
                properties_set[property_name].append(base_property)
        else:
            base_property = get_range_links()
            properties_set[property_name].append(base_property)

    image_links = []
    for link_ in data['links_inverse']:
        if link_.property.code in ['OA7', 'OA8', 'OA9']:
            continue
        if link_.property.code == 'P127':
            property_name = 'broader'
        else:
            property_name = \
                loud[get_crm_relation(link_, True).replace(' ', '_')]

        if link_.property.code == 'P53':
            for geom in Gis.get_wkt_by_id(link_.range.id):
                base_property = get_domain_links() | geom
                properties_set[property_name].append(base_property)
        else:
            base_property = get_domain_links()
            properties_set[property_name].append(base_property)

        if link_.domain.class_.name == 'file' and g.files.get(link_.domain.id):
            image_links.append(link_)

    if image_links:
        profile_image = Entity.get_profile_image_id(data['entity'])
        representation = {"type": "VisualItem", "digitally_shown_by": []}
        for link_ in image_links:
            id_ = link_.domain.id
            mime_type, _ = mimetypes.guess_type(g.files[id_])
            if not mime_type:
                continue  # pragma: no cover
            image = {
                "id": url_for('api.entity', id_=id_, _external=True),
                "_label": link_.domain.name,
                "type": "DigitalObject",
                "format": mime_type,
                "access_point": [{
                    "id": url_for(
                        'api.display',
                        filename=get_file_path(id_).stem,
                        _external=True),
                    "type": "DigitalObject",
                    "_label": "ProfileImage" if id_ == profile_image else ''}]}
            if type_ := get_standard_type_loud(link_.domain.types):
                image['classified_as'] = get_type_property(type_)
            representation['digitally_shown_by'].append(image)
        properties_set['representation'].append(representation)
    return {'@context': app.config['API_CONTEXT']['LOUD']} | \
        base_entity_dict() | properties_set


def get_loud_timespan(entity: Entity) -> dict[str, Any]:
    return {
        'type': 'TimeSpan',
        'begin_of_the_begin': date_to_str(entity.begin_from),
        'end_of_the_begin': date_to_str(entity.begin_to),
        'begin_of_the_end': date_to_str(entity.end_from),
        'end_of_the_end': date_to_str(entity.end_to)}


def get_type_property(type_: Type) -> dict[str, Any]:
    return {
        'id': url_for('api.entity', id_=type_.id, _external=True),
        'type': remove_spaces_dashes(type_.cidoc_class.i18n['en']),
        '_label': type_.name}


def get_standard_type_loud(types: dict[Type, Any]) -> Optional[Type]:
    standard = None
    for type_ in types:
        if type_.category == 'standard':
            standard = type_
    return standard
