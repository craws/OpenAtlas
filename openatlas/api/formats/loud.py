import mimetypes
from collections import defaultdict
from typing import Any, Optional

from flask import g, url_for

from openatlas import app
from openatlas.api.resources.util import (
    date_to_str, get_crm_code, get_crm_relation, get_iiif_manifest_and_path,
    get_license_type, remove_spaces_dashes, to_camel_case)
from openatlas.display.util import get_file_path
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis
from openatlas.models.type import Type

unit_map = {
    'B': 'bytes',
    'KB': 'kilobytes',
    'MB': 'megabytes',
    'GB': 'gigabytes',
    'TB': 'terabytes'}


def get_file_dimensions(entity: Entity) -> dict[str, Any]:
    file_size = entity.get_file_size()
    return {'dimension': [{
        "type": "Dimension",
        "_label": file_size,
        "classified_as": [{
            "id": "https://vocab.getty.edu/aat/300265863",
            "type": "Type",
            "_label": "File Size"}],
        "value": int(file_size.split()[0]),
        "unit": {
            "id": "https://vocab.getty.edu/aat/300265870",
            "type": "MeasurementUnit",
            "_label": unit_map[file_size.split()[1]]}}]}


def get_digital_object_details(
        entity: Entity,
        license_url: dict[int, str]) -> dict[str, Any]:
    mime_type, _ = mimetypes.guess_type(g.files[entity.id])
    file_ = get_file_path(entity.id)
    digital_object: dict[str, Any] = {
        'format': mime_type,
        "classified_as": [{
            "id": "https://vocab.getty.edu/aat/300215302",
            "type": "Type",
            "_label": "Digital Image"}]}
    if file_ and file_.stem:
        digital_object.update({"access_point": [{
            "id": url_for(
                'api.display',
                filename=file_.stem if file_ else '',
                _external=True),
            "type": "DigitalObject"}]})
    if entity.license_holder:
        digital_object.update({
            'right_held_by': [{
                '_label': entity.license_holder,
                'type': 'Actor'}]})
    if entity.creator:
        digital_object.update({'created_by': [{
            '_label': f'Creation of {entity.name}',
            'type': 'Creation',
            'carried_out_by': [{
                '_label': entity.creator,
                'type': 'Actor'}]}]})
    if license_ := get_license_type(entity):
        subject_to: dict[str, Any] = {
            'type': "Right",
            '_label': f'License of {entity.name}',
            "identified_by": [{
                'id': url_for(
                    'api.entity',
                    id_=license_.id,
                    _external=True),
                "type": "Name",
                "content": license_.name}]}
        if url := license_url.get(license_.id):
            subject_to['classified_as'] = [{
                "id": url,
                "type": "Type",
                "_label": license_.name}]
        digital_object.update({'subject_to': [subject_to]})
    return digital_object


def get_loud_entities(
        data: dict[str, Any],
        loud: dict[str, str],
        license_url: dict[int, str]) -> Any:
    entity = data['entity']

    def get_range_links() -> dict[str, Any]:
        property_: Any = {
            'id': url_for(
                'api.entity',
                id_=link_.range.id,
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
            relationship = {
                'type': 'Event',
                '_label':
                    f'Relationship between '
                    f'{link_.domain.name} and {link_.range.name}',
                'had_participant': [property_]}
            if link_.type:
                relationship['classified_as'] = [
                    get_type_property(g.types[link_.type.id])]
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

    def get_domain_links() -> dict[str, Any]:
        property_: Any = {
            'id': url_for(
                'api.entity',
                id_=link_.domain.id,
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
            super_type = g.types[g.types[link_.range.id].root[-1]]
            property_['part_of'] = [get_type_property(super_type)]
        elif link_.type:
            property_['classified_as'] = [
                get_type_property(g.types[link_.type.id])]
        if code_ == 'P67':
            if link_.domain.class_.name == 'file':
                property_['type'] = 'DigitalObject'
            if standard_type := get_standard_type_loud(link_.domain.types):
                property_['classified_as'] = get_type_property(standard_type)
            if link_.description:
                property_['content'] = link_.description
                if link_.domain.cidoc_class.code == 'E32':
                    system = g.reference_systems[link_.domain.id]
                    match_case = to_camel_case(
                        g.types[link_.type.id].name).replace(' ', '_')
                    link_url = \
                        f"{system.resolver_url or ''}{link_.description}"
                    property_[f"skos:{match_case}"] = link_url
            if link_.domain.class_.name == 'external_reference':
                property_ = {
                    "type": "LinguisticObject",
                    "digitally_carried_by": [{
                        "type": "DigitalObject",
                        "classified_as": [{
                            "id": "https://vocab.getty.edu/aat/300264578",
                            "type": "Type",
                            "_label": "Web Page"}],
                        "format": "text/html",
                        "_label": link_.description,
                        "access_point": [{
                            "id":
                                link_.domain.name,
                            "type": "DigitalObject"}]}]}
        if code_ == 'OA7':
            relationship = {
                'type': 'Event',
                '_label':
                    f'Relationship between '
                    f'{link_.range.name} and {link_.domain.name}',
                'had_participant': [property_]}
            if link_.type:
                relationship['classified_as'] = [
                    get_type_property(g.types[link_.type.id])]
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
        elif link_.property.code == 'P67':
            property_name = 'refers_to'
            if link_.domain.class_.name == 'file':
                property_name = 'digitally_carries'
        else:
            property_name = get_loud_property_name(loud, link_)

        if link_.property.code == 'P53':
            for geom in Gis.get_wkt_by_id(link_.range.id):
                base_property = get_range_links() | geom
                properties_set[property_name].append(base_property)
        else:
            base_property = get_range_links()
            properties_set[property_name].append(base_property)

    file_links = []
    for link_ in data['links_inverse']:
        if link_.property.code in ['OA8', 'OA9']:
            property_name = 'brought_into_existence_by'
            if link_.property.code == 'OA9':
                property_name = 'taken_out_of_existence_by'
        elif link_.property.code == 'OA7':
            property_name = 'participated_in'
        elif link_.domain.class_.name == 'external_reference':
            property_name = 'subject_of'
        elif link_.domain.class_.name == 'file' and g.files.get(
                link_.domain.id):
            file_links.append(link_)
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

    if file_links:
        properties_set['representation'].extend(
            get_loud_representations(file_links, license_url))
        properties_set['subject_of'].extend(
            get_loud_iiif_subject_of(file_links))

    if entity.class_.name == 'file' and g.files.get(entity.id):
        properties_set.update(get_file_dimensions(entity))
        properties_set.update(get_digital_object_details(entity, license_url))

    return ({'@context': app.config['API_CONTEXT']['LOUD']} |
            base_entity_dict(entity) |
            properties_set)


def base_entity_dict(entity: Entity) -> dict[str, Any]:
    timespan = get_loud_timespan(entity) \
        if entity.first or entity.last else {}
    type_ = remove_spaces_dashes(entity.cidoc_class.i18n['en'])
    if entity.class_.name == 'file':
        type_ = 'DigitalObject'
    return {
        'id': url_for(
            'api.entity',
            id_=entity.id,
            _external=True),
        'type': type_,
        '_label': entity.name,
        'content': entity.description,
        'identified_by': [{
            "type": "Name",
            "content": entity.name}]} | timespan


def get_loud_property_name(
        loud: dict[str, str],
        link_: Link,
        inverse: bool = False) -> str:
    name = 'part' if inverse else 'part_of'
    if not link_.property.code == 'P127':
        name = loud[get_crm_relation(link_, inverse).replace(' ', '_')]
    return name


def get_loud_representations(
        image_links: list[Link],
        license_url: dict[int, str]) -> list[dict[str, Any]]:
    representation = []
    for link_ in image_links:
        entity = link_.domain
        image = {
            'id': url_for(
                'api.entity',
                id_=entity.id,
                _external=True),
            '_label': entity.name,
            'type': 'DigitalObject'}
        image.update(get_digital_object_details(entity, license_url))
        representation.append({
            'type': 'VisualItem',
            'digitally_shown_by': [image]})

    return representation


def get_loud_iiif_subject_of(image_links: list[Link]) -> list[dict[str, Any]]:
    subject_of = []
    for link_ in image_links:
        entity = link_.domain
        if iiif := get_iiif_manifest_and_path(entity.id):
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
    return subject_of


def get_loud_timespan(entity: Entity) -> dict[str, Any]:
    timespan = {'timespan': (
            {'type': 'TimeSpan'} |
            get_loud_begin_dates(entity) |
            get_loud_end_dates(entity))}
    if not isinstance(entity, Link) and \
            remove_spaces_dashes(entity.cidoc_class.i18n['en']) == 'Person':
        born, death = {}, {}
        if entity.begin_from:
            born = {'born': {
                'type': 'Birth',
                '_label': f'Birth of {entity.name}',
                'timespan':
                    {'type': 'TimeSpan'} |
                    get_loud_begin_dates(entity)}}
        if entity.end_from:
            death = {'death_of': {
                'type': 'Death',
                '_label': f'Death of {entity.name}',
                'timespan':
                    {'type': 'TimeSpan'} |
                    get_loud_end_dates(entity)}}
        timespan = born | death
    return timespan


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
