import mimetypes
from collections import defaultdict
from typing import Any, Optional

from flask import g, url_for

from openatlas import app
from openatlas.api.resources.util import (
    date_to_str, get_crm_code, get_crm_relation, get_iiif_manifest_and_path,
    get_license_type, get_license_url, remove_spaces_dashes, to_camel_case)
from openatlas.display.util import get_file_path
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis
from openatlas.models.type import Type


def get_loud_entities(data: dict[str, Any], loud: dict[str, str]) -> Any:
    def base_entity_dict() -> dict[str, Any]:
        timespan = {'timespan': get_loud_timespan(data['entity'])}
        if remove_spaces_dashes(
                data['entity'].cidoc_class.i18n['en']) == 'Person':
            born, death = {}, {}
            if data["entity"].begin_from:
                born = {'born': {
                    'type': 'Birth',
                    '_label': f'Birth of {data["entity"].name}',
                    'timespan':
                        {'type': 'TimeSpan'} |
                        get_loud_begin_dates(data['entity'])}}
            if data["entity"].end_from:
                death = {'death_of': {
                    'type': 'Death',
                    '_label': f'Death of {data["entity"].name}',
                    'timespan':
                        {'type': 'TimeSpan'} |
                        get_loud_end_dates(data['entity'])}}
            timespan = born | death
        return {
            'id': url_for(
                'api.entity',
                id_=data['entity'].id,
                format='loud',
                _external=True),
            'type': remove_spaces_dashes(
                data['entity'].cidoc_class.i18n['en']),
            '_label': data['entity'].name,
            'content': data['entity'].description,
            'identified_by': [{
                "type": "Name",
                "content": data['entity'].name}]} | timespan

    def get_range_links() -> dict[str, Any]:
        property_ = {
            'id': url_for(
                'api.entity',
                id_=link_.range.id,
                format='loud',
                _external=True),
            'type': loud[get_crm_code(link_).replace(' ', '_')],
            '_label': link_.range.name}
        if link_.begin_from or link_.end_from:
            property_['timespan'] = get_loud_timespan(link_)
        code_ = link_.property.code
        if code_ == 'P2':
            if link_.description:
                property_['value'] = link_.description
                property_['unit'] = {
                    'type': "MeasurementUnit",
                    '_label': link_.range.description}
            super_type = g.types[g.types[link_.range.id].root[-1]]
            property_['part_of'] = [get_type_property(super_type)]
        elif link_.type:
            property_['classified_as'] = [
                get_type_property(g.types[link_.type.id])]
        if code_ == 'P67' and link_.description:
            property_['content'] = link_.description
            if link_.domain.cidoc_class.code == 'E32':
                system = g.reference_systems[link_.domain.id]
                match_case = to_camel_case(
                    g.types[link_.type.id].name).replace(' ', '_')
                link_url = f"{system.resolver_url or ''}{link_.description}"
                property_[f"skos:{match_case}"] = link_url
        if code_ == 'OA7':
            property_ = [{
                'type': 'Event',
                '_label':
                    f'Relationship between '
                    f'{link_.domain.name} and {link_.range.name}',
                'classified_as': [get_type_property(g.types[link_.type.id])],
                'had_participant': [property_]}]
        if code_ in ['OA8', 'OA9']:
            property_ = {
                'type': 'BeginningOfExistence'
                if code_ == 'OA8' else 'EndOfExistence',
                '_label':
                    ('Birth of ' if code_ == 'OA8' else 'Death of ') +
                    link_.domain.name,
                'took_place_at': [property_]}
        return property_

    def get_domain_links() -> dict[str, Any]:
        property_ = {
            'id': url_for(
                'api.entity',
                id_=link_.domain.id,
                format='loud',
                _external=True),
            'type': loud[get_crm_code(link_, True).replace(' ', '_')],
            '_label': link_.domain.name}
        if link_.begin_from or link_.end_from:
            property_['timespan'] = get_loud_timespan(link_)
        code_ = link_.property.code
        if code_ == 'P2':
            if link_.description:
                property_['value'] = link_.description
                property_['unit'] = {
                    'type': "MeasurementUnit",
                    '_label': link_.domain.description}
        elif link_.type:
            property_['classified_as'] = [
                get_type_property(g.types[link_.type.id])]
        if code_ == 'P67' and link_.description:
            property_['content'] = link_.description
            if link_.domain.cidoc_class.code == 'E32':
                system = g.reference_systems[link_.domain.id]
                match_case = to_camel_case(
                    g.types[link_.type.id].name).replace(' ', '_')
                link_url = f"{system.resolver_url or ''}{link_.description}"
                property_[f"skos:{match_case}"] = link_url
        if code_ == 'OA7':
            relationship = {
                'type': 'Event',
                '_label':
                    f'Relationship between '
                    f'{link_.range.name} and {link_.domain.name}',
                'classified_as': [get_type_property(g.types[link_.type.id])],
                'had_participant': [property_]}
            property_ = [relationship]
        if code_ in ['OA8', 'OA9']:
            property_ = {
                'type': 'BeginningOfExistence'
                if code_ == 'OA8' else 'EndOfExistence',
                '_label':
                    ('Birth of ' if code_ == 'OA8' else 'Death of ') +
                    link_.domain.name,
                'took_place_at': [property_]}
        return property_

    properties_set = defaultdict(list)
    for link_ in data['links']:
        if link_.property.code in ['OA8', 'OA9']:
            property_name = 'brought_into_existence_by'
        elif link_.property.code == 'OA7':
            property_name = 'participated_in'
        else:
            property_name = get_loud_property_name(loud, link_)

        if link_.property.code == 'P53':
            for geom in Gis.get_wkt_by_id(link_.range.id):
                base_property = get_range_links() | geom
                properties_set[property_name].append(base_property)
        else:
            base_property = get_range_links()
            properties_set[property_name].append(base_property)

    image_links = []
    for link_ in data['links_inverse']:
        if link_.property.code in ['OA8', 'OA9']:
            property_name = 'brought_into_existence_by'
            if link_.property.code == 'OA9':
                property_name = 'taken_out_of_existence_by'
        elif link_.property.code == 'OA7':
            property_name = 'participated_in'
        elif link_.domain.class_.name == 'file' and g.files.get(link_.domain.id):
            image_links.append(link_)
            continue
        else:
            property_name = get_loud_property_name(loud, link_, inverse=True)

        if link_.property.code == 'P53':
            for geom in Gis.get_wkt_by_id(link_.range.id):
                base_property = get_domain_links() | geom
                properties_set[property_name].append(base_property)
        else:
            base_property = get_domain_links()
            properties_set[property_name].append(base_property)

    if image_links:
        properties_set.update(get_loud_images(data['entity'], image_links))

    return ({'@context': app.config['API_CONTEXT']['LOUD']} |
            base_entity_dict() |
            properties_set)


def get_loud_property_name(
        loud: dict[str, str],
        link_: Link,
        inverse: bool = False) -> str:
    name = 'part' if inverse else 'part_of'
    if not link_.property.code == 'P127':
        name = loud[get_crm_relation(link_, inverse).replace(' ', '_')]
    return name


def get_loud_images(entity: Entity, image_links: list[Link]) -> dict[str, Any]:
    profile_image = Entity.get_profile_image_id(entity)
    representation = []
    subject_of = []
    for link_ in image_links:
        id_ = link_.domain.id
        mime_type, _ = mimetypes.guess_type(g.files[id_])
        if not mime_type:
            continue  # pragma: no cover
        file_ = get_file_path(id_)
        image = {
            'id': url_for(
                'api.entity',
                id_=id_,
                format='loud',
                _external=True),
            '_label': link_.domain.name,
            'type': 'DigitalObject',
            'format': mime_type,
            'right_held_by': [{
                '_label': link_.domain.license_holder,
                'type': 'Actor'}],
            'created_by': [{
                '_label': f'Creation of {link_.domain.name}',
                'type': 'Creation',
                'carried_out_by': [{
                    '_label': link_.domain.creator,
                    'type': 'Actor'}]}],
            "classified_as": [{
                "id": "https://vocab.getty.edu/aat/300215302",
                "type": "Type",
                "_label": "Digital Image"}],
            'access_point': [{
                'id': url_for(
                    'api.display',
                    filename=file_.stem if file_ else '',
                    _external=True),
                'type': 'DigitalObject',
                '_label': 'ProfileImage' if id_ == profile_image else ''}]}
        if license_ := get_license_type(link_.domain):
            image['subject_to'] = [{
                'type': "Right",
                '_label': f'License of {link_.domain.name}',
                "identified_by": [{
                    'id': url_for(
                        'api.entity',
                        id_=license_.id,
                        format='loud',
                        _external=True),
                    "type": "Name",
                    "content": license_.name}],
                "classified_as": [{
                    "id": get_license_url(link_.domain),
                    "type": "Type",
                    "_label": license_.name}]}]
        representation.append({
            'type': 'VisualItem',
            'digitally_shown_by': [image]})
        if iiif := get_iiif_manifest_and_path(link_.domain.id):
            subject_of.append({
                "type": "LinguisticObject",
                "digitally_carried_by": [{
                    "type": "DigitalObject",
                    "access_point": [{
                        "id": iiif['IIIFManifest'],
                        "type": "DigitalObject"}],
                    "conforms_to": [{
                        "id": "https://iiif.io/api/presentation/2.0/",
                        "type": "InformationObject"}],
                    "format":
                        "application/ld+json;profile='https://iiif.io/api"
                        "/presentation/2/context.json'"}]})
    return {
        'representation': representation,
        'subject_of': subject_of}


def get_loud_timespan(entity: Entity) -> dict[str, Any]:
    return ({'type': 'TimeSpan'} |
            get_loud_begin_dates(entity) |
            get_loud_end_dates(entity))


def get_loud_begin_dates(entity: Entity) -> dict[str, Any]:
    return {
        'begin_of_the_begin': date_to_str(entity.begin_from),
        'end_of_the_begin': date_to_str(entity.begin_to),
        'beginning_is_qualified_by': entity.begin_comment}


def get_loud_end_dates(entity: Entity) -> dict[str, Any]:
    return {
        'begin_of_the_end': date_to_str(entity.end_from),
        'end_of_the_end': date_to_str(entity.end_to),
        'end_is_qualified_by': entity.end_comment}


def get_type_property(type_: Type) -> dict[str, Any]:
    property_ = {
        'id': url_for(
            'api.entity',
            id_=type_.id,
            format='loud',
            _external=True),
        'type': remove_spaces_dashes(type_.cidoc_class.i18n['en']),
        '_label': type_.name}
    if type_.begin_from or type_.end_from:
        property_['timespan'] = get_loud_timespan(type_)
    for super_type in [g.types[root] for root in type_.root]:
        property_['part_of'] = [get_type_property(super_type)]
    return property_


def get_standard_type_loud(types: dict[Type, Any]) -> Optional[Type]:
    standard = None
    for type_ in types:
        if type_.category == 'standard':
            standard = type_
    return standard
