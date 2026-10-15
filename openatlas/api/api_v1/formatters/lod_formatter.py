from typing import Any, Final

from flask import url_for

from openatlas.api.api_v1.formatters.la_helpers import (
    date_to_utc_iso_str,
    is_float,
)
from openatlas.api.api_v1.formatters.util import (
    EntityLinks,
    entity_uri,
    get_links_for_entities,
    get_type_references,
)
from openatlas.models.dates import Dates
from openatlas.models.entity import Entity, Link

LOD_CLASS_MAP: Final[dict[str, str]] = {
    'acquisition': 'Acquisition',
    'activity': 'Activity',
    'modification': 'Modification',
    'move': 'Move',
    'production': 'Production',
    'creation': 'Creation',
    'administrative_unit': 'Place',
    'object_location': 'Place',
    'place': 'Place',
    'artifact': 'HumanMadeObject',
    'feature': 'Feature',
    'human_remains': 'BiologicalObject',
    'stratigraphic_unit': 'StratigraphicUnit',
    'file': 'Document',
    'person': 'Person',
    'group': 'Group',
    'bibliography': 'Document',
    'edition': 'Document',
    'external_reference': 'Document',
    'reference_system': 'Document',
    'source': 'LinguisticObject',
    'text': 'LinguisticObject',
    'type': 'Type',
    'type_tools': 'Type',
    'alias': 'Appellation',
}


def lod_type(entity: Entity) -> str:
    return LOD_CLASS_MAP.get(entity.class_.name, 'HumanMadeObject')


def format_datetime(value: Any, end_of_day: bool = False) -> str | None:
    date = date_to_utc_iso_str(value)
    if date is None or 'T' in date:
        return date
    return f'{date}T23:59:59Z' if end_of_day else f'{date}T00:00:00Z'


def get_lod_timespan(dates: Dates, label: str) -> dict[str, Any] | None:
    if not dates.dates_available():
        return None
    data: dict[str, Any] = {
        'type': 'TimeSpan',
        'label': label}
    if dates.begin_from:
        data['begin_of_the_begin'] = format_datetime(dates.begin_from)
    if dates.begin_to:
        data['end_of_the_begin'] = format_datetime(dates.begin_to, True)
    if dates.end_from:
        data['begin_of_the_end'] = format_datetime(dates.end_from)
    if dates.end_to:
        data['end_of_the_end'] = format_datetime(dates.end_to, True)
    if dates.begin_comment:
        data['begin_comment'] = dates.begin_comment
    if dates.end_comment:
        data['end_comment'] = dates.end_comment
    return data


def lod_append(record: dict[str, Any], key: str, value: Any) -> None:
    record.setdefault(key, []).append(value)


class LodFormatter:
    def __init__(
            self,
            type_references: dict[int, list[Link]] | None = None) -> None:
        self.type_refs = (
            type_references if type_references is not None
            else get_type_references())
        self.entity: Entity
        self.geometries: dict[int, Any] = {}
        self.handlers = {
            'P1': self._p1,
            'P2': self._p2,
            'P7': self._p7,
            'P9': self._p9,
            'P11': self._p11,
            'P14': self._p14,
            'P22': self._p22,
            'P23': self._p23,
            'P24': self._p24,
            'P25': self._p25,
            'P26': self._p26,
            'P27': self._p27,
            'P31': self._p31,
            'P46': self._p46,
            'P52': self._p52,
            'P53': self._p53,
            'P67': self._p67,
            'P73': self._p73,
            'P74': self._p74,
            'P89': self._p89,
            'P94': self._p94,
            'P107': self._p107,
            'P108': self._p108,
            'P127': self._p127,
            'P128': self._p128,
            'P134': self._p134,
            'OA7': self._oa7,
            'OA8': self._oa8,
            'OA9': self._oa9}

    def format_entity(self, data: EntityLinks) -> dict[str, Any]:
        self.entity = entity = data.entity
        self.geometries = data.geometries
        record: dict[str, Any] = {
            'id': entity_uri(entity),
            'type': lod_type(entity),
            'label': entity.name}

        if entity.description:
            record['description'] = entity.description

        if timespan := get_lod_timespan(
                entity.dates,
                f'Timespan of {entity.name}'):
            record['has_time_span'] = timespan

        if geometry := self.geometries.get(entity.id):
            record['has_geometry'] = {
                'type': 'Geometry',
                'as_wkt': geometry}

        for link_ in data.links:
            if handler := self.handlers.get(link_.property.code):
                handler(link_, record, False)

        for link_ in data.links_inverse:
            if handler := self.handlers.get(link_.property.code):
                handler(link_, record, True)

        return record

    def _ref(self, entity: Entity) -> dict[str, Any]:
        ref: dict[str, Any] = {
            'id': entity_uri(entity),
            'type': lod_type(entity),
            'label': entity.name}
        if geom := self.geometries.get(entity.id):
            ref['has_geometry'] = {
                'type': 'Geometry',
                'as_wkt': geom}
        return ref

    def _type_ref(self, type_: Entity) -> dict[str, Any]:
        ref: dict[str, Any] = {
            'id': entity_uri(type_),
            'type': 'Type',
            'label': type_.name}
        return ref

    def _p1(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            lod_append(record, 'identified_by', {
                'id': entity_uri(link_.range),
                'type': 'Appellation',
                'label': link_.range.name})

    def _p2(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            return
        type_ = link_.range
        if link_.description and is_float(link_.description):
            unit = type_.description or 'unit'
            lod_append(record, 'has_dimension', {
                'type': 'Dimension',
                'label': f'{type_.name}: {link_.description} {unit}',
                'value': float(link_.description),
                'unit': unit,
                'has_type': [self._type_ref(type_)]})
        else:
            lod_append(record, 'has_type', self._type_ref(type_))

    def _p46(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            record['forms_part_of'] = self._ref(link_.domain)
        else:
            lod_append(record, 'is_composed_of', self._ref(link_.range))

    def _p53(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'is_location_of', self._ref(link_.domain))
        else:
            ref = self._ref(link_.range)
            if geom := self.geometries.get(link_.range.id):
                ref['has_geometry'] = {
                    'type': 'Geometry',
                    'as_wkt': geom}
            record['has_location'] = ref

    def _p89(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'contains_place', self._ref(link_.domain))
        else:
            lod_append(record, 'falls_within', self._ref(link_.range))

    def _p7(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            record['took_place_at'] = self._ref(link_.range)

    def _p9(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            record['forms_part_of'] = self._ref(link_.domain)
        else:
            lod_append(record, 'is_composed_of', self._ref(link_.range))

    def _p11(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'participated_in', self._ref(link_.domain))
        else:
            lod_append(record, 'had_participant', self._ref(link_.range))

    def _p14(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'performed', self._ref(link_.domain))
        else:
            lod_append(record, 'carried_out_by', self._ref(link_.range))

    def _p22(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            lod_append(record, 'transferred_title_to', self._ref(link_.range))

    def _p23(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            lod_append(record, 'transferred_title_from', self._ref(link_.range))

    def _p24(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            record['title_transferred_through'] = self._ref(link_.domain)
        else:
            lod_append(record, 'transferred_title_of', self._ref(link_.range))

    def _p25(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            lod_append(record, 'moved', self._ref(link_.range))

    def _p26(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            record['moved_to'] = self._ref(link_.range)

    def _p27(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            record['moved_from'] = self._ref(link_.range)

    def _p31(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'was_modified_by', self._ref(link_.domain))
        else:
            lod_append(record, 'has_modified', self._ref(link_.range))

    def _p52(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            lod_append(record, 'current_owner', self._ref(link_.range))

    def _p67(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'is_referred_to_by', self._ref(link_.domain))
        else:
            lod_append(record, 'refers_to', self._ref(link_.range))

    def _p73(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'is_translation_of', self._ref(link_.domain))
        else:
            lod_append(record, 'has_translation', self._ref(link_.range))

    def _p74(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            lod_append(record, 'residence', self._ref(link_.range))

    def _p94(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            record['was_created_by'] = self._ref(link_.domain)
        else:
            lod_append(record, 'has_created', self._ref(link_.range))

    def _p107(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'member_of', self._ref(link_.domain))
        else:
            lod_append(record, 'has_member', self._ref(link_.range))

    def _p108(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            record['was_produced_by'] = self._ref(link_.domain)
        else:
            lod_append(record, 'has_produced', self._ref(link_.range))

    def _p127(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            lod_append(record, 'has_broader_term', self._type_ref(link_.range))

    def _p128(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'is_carried_by', self._ref(link_.domain))
        else:
            lod_append(record, 'carries', self._ref(link_.range))

    def _p134(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            lod_append(record, 'was_continued_by', self._ref(link_.domain))
        else:
            lod_append(record, 'continued', self._ref(link_.range))

    def _oa7(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        other = link_.domain if inverse else link_.range
        rel_ref = self._ref(other)
        if link_.type and link_.type.name:
            rel_ref['relation_type'] = link_.type.name
        lod_append(record, 'has_relationship_to', rel_ref)

    def _oa8(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            record['begins_in'] = self._ref(link_.range)

    def _oa9(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            record['ends_in'] = self._ref(link_.range)


def get_context_url() -> str:
    try:
        return url_for('api_v1_lod.get_context', _external=True)
    except RuntimeError:
        return 'https://openatlas.eu/ns/v1/context.json'


def format_lod_entity(entity: Entity) -> dict[str, Any]:
    links_data = get_links_for_entities([entity])
    item = links_data[entity.id]
    formatter = LodFormatter()
    record = formatter.format_entity(item)
    return {'@context': get_context_url()} | record


def format_lod_entities(
        entities: list[Entity],
        pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    context_url = get_context_url()
    if not entities and pagination is None:
        return {
            '@context': context_url,
            'type': 'OrderedCollection',
            'totalItems': 0,
            'orderedItems': []}
    links_data = get_links_for_entities(entities) if entities else {}
    formatter = LodFormatter()
    items = [formatter.format_entity(item) for item in links_data.values()]
    if pagination is None:
        return {
            '@context': context_url,
            'type': 'OrderedCollection',
            'totalItems': len(items),
            'orderedItems': items}
    result: dict[str, Any] = {
        '@context': context_url,
        'id': pagination['id'],
        'type': 'OrderedCollectionPage',
        'partOf': {
            'id': pagination['collection_url'],
            'type': 'OrderedCollection',
            'totalItems': pagination['total_items'],
            'first': {
                'id': pagination['first'],
                'type': 'OrderedCollectionPage'},
            'last': {
                'id': pagination['last'],
                'type': 'OrderedCollectionPage'}},
        'startIndex': pagination['start_index'],
        'orderedItems': items}
    if 'previous' in pagination:
        result['prev'] = {
            'id': pagination['previous'],
            'type': 'OrderedCollectionPage'}
    if 'next' in pagination:
        result['next'] = {
            'id': pagination['next'],
            'type': 'OrderedCollectionPage'}
    return result
