import ast
import hashlib
import mimetypes
from typing import Any

import validators
from flask import g, url_for

from openatlas.api.api_v1.entity import get_entity_by_id
from openatlas.api.api_v1.formatters.loud_helpers import (
    ACTORS, BIBLIOGRAPHY_AAT, CLASS_TYPES, DIMENSION_ROOTS,
    MIME_CLASSIFICATIONS, UNIT_MAP, alias_name, aat_type, category_aat,
    get_language, identifier, la_type, primary_name, statement,
    unique_identifier)
from openatlas.api.api_v1.formatters.lod_util import (
    EntityLinks, date_to_utc_iso_str, entity_uri, get_iiif_manifest_and_path,
    get_license_type, get_type_references, is_float)
from openatlas.display.util2 import get_file_path
from openatlas.models.annotation import AnnotationText
from openatlas.models.dates import Dates
from openatlas.models.entity import Entity, Link

CLOSE_MATCH = {
    'id': 'http://www.w3.org/2004/02/skos/core#closeMatch',
    'type': 'Type',
    '_label': 'Close Match'}

# Property code -> (key if the root is the activity,
#                   key if the root is the actor)
ACTOR_EVENT_KEYS = {
    'P11': ('participant', 'participated_in'),
    'P14': ('carried_out_by', 'carried_out'),
    'P22': ('participant', 'participated_in'),
    'P23': ('participant', 'participated_in')}

# Property code -> (key, embedded event type, multiple) for objects
OBJECT_EVENT_KEYS = {
    'P24': ('changed_ownership_through', 'Acquisition', True),
    'P31': ('modified_by', 'Modification', True),
    'P108': ('produced_by', 'Production', False)}

LIFE_EVENTS = {
    'person': {
        'begin_key': 'born',
        'begin_type': 'Birth',
        'end_key': 'died',
        'end_type': 'Death'},
    'group': {
        'begin_key': 'formed_by',
        'begin_type': 'Formation',
        'end_key': 'dissolved_by',
        'end_type': 'Dissolution'}}
OBJECT_LIFE_EVENTS = {
    'begin_key': 'produced_by',
    'begin_type': 'Production',
    'end_key': 'destroyed_by',
    'end_type': 'Destruction'}
LIFE_EVENTS |= dict.fromkeys(
    ['artifact', 'feature', 'human_remains', 'place', 'stratigraphic_unit'],
    OBJECT_LIFE_EVENTS)

# Property code -> key of the Move part
MOVE_KEYS = {'P25': 'moved', 'P26': 'moved_to', 'P27': 'moved_from'}


def reference_url(type_link: Link) -> str:
    if type_link.domain.class_.name == 'reference_system':
        system = g.reference_systems[type_link.domain.id]
        return f'{system.resolver_url or ''}{type_link.description}'
    return type_link.domain.name


def is_close_match(link_: Link) -> bool:
    return bool(
        link_.type
        and g.types.get(link_.type.id)
        and 'close' in g.types[link_.type.id].name)


def generate_skolem_id(id_: int, type_name: str) -> str:
    seed = f"{id_}_{type_name}".encode('utf-8')
    identifier_hash = hashlib.sha256(seed).hexdigest()[:16]
    base = getattr(g, 'skolem_base_url', None)
    if base is None:
        base = url_for("api.skolem_proxy", subpath='', _external=True)
        g.skolem_base_url = base
    return f"{base}{type_name.lower()}/{identifier_hash}"


def append(record: dict[str, Any], key: str, value: Any) -> None:
    record.setdefault(key, []).append(value)


def format_datetime(value: Any, end_of_day: bool = False) -> str | None:
    date = date_to_utc_iso_str(value)
    if date is None or 'T' in date:
        return date
    return f'{date}T23:59:59Z' if end_of_day else f'{date}T00:00:00Z'


def get_begin_span(dates: Dates) -> dict[str, Any]:
    span = {
        'begin_of_the_begin': format_datetime(dates.begin_from),
        'end_of_the_end': format_datetime(dates.begin_to, True)}
    if span['end_of_the_end'] is None:
        span['end_of_the_end'] = format_datetime(dates.begin_from, True)
    return {k: v for k, v in span.items() if v is not None}


def get_end_span(dates: Dates) -> dict[str, Any]:
    span = {
        'begin_of_the_begin': format_datetime(dates.end_from),
        'end_of_the_end': format_datetime(dates.end_to, True)}
    if span['begin_of_the_begin'] is None:
        span['begin_of_the_begin'] = format_datetime(dates.end_to)
    if span['end_of_the_end'] is None:
        span['end_of_the_end'] = format_datetime(dates.end_from, True)
    return {k: v for k, v in span.items() if v is not None}


def get_timespan(dates: Dates, label: str) -> dict[str, Any] | None:
    if not dates.dates_available():
        return None
    data = {
        'begin_of_the_begin': format_datetime(dates.begin_from),
        'end_of_the_begin': format_datetime(dates.begin_to, True),
        'begin_of_the_end': format_datetime(dates.end_from),
        'end_of_the_end': format_datetime(dates.end_to, True)}
    if data['end_of_the_end'] is None:
        data['end_of_the_end'] = (
            format_datetime(dates.end_from, True)
            or format_datetime(dates.begin_to, True)
            or format_datetime(dates.begin_from, True))
    return {'type': 'TimeSpan', '_label': label} \
        | {k: v for k, v in data.items() if v is not None}


def get_date_notes(dates: Dates) -> list[dict[str, Any]]:
    note = category_aat('300027200', 'Note')
    return [
        statement(comment, label, [note])
        for label, comment in (
            ('Begin comment', dates.begin_comment),
            ('End comment', dates.end_comment))
        if comment]


class LoudFormatter:
    def __init__(
            self,
            type_references: dict[int, list[Link]] | None = None) -> None:
        self.type_refs = (
            type_references if type_references is not None
            else get_type_references())
        self.entity: Entity
        self.geometries: dict[int, Any] = {}
        self.handlers: dict[str, Any] = {
            'P1': self._p1,
            'P2': self._p2,
            'P7': self._p7,
            'P9': self._p9,
            'P11': self._actor_event,
            'P14': self._actor_event,
            'P22': self._actor_event,
            'P23': self._actor_event,
            'P24': self._object_event,
            'P25': self._move,
            'P26': self._move,
            'P27': self._move,
            'P31': self._object_event,
            'P46': self._p46,
            'P52': self._p52,
            'P53': self._p53,
            'P67': self._p67,
            'P73': self._p73,
            'P74': self._p74,
            'P107': self._p107,
            'P108': self._object_event,
            'P127': self._p127,
            'P134': self._p134,
            'OA7': self._oa7}

    def format_entity(self, data: EntityLinks) -> dict[str, Any]:
        self.entity = entity = data.entity
        self.geometries = data.geometries
        record: dict[str, Any] = {
            'id': entity_uri(entity),
            'type': la_type(entity),
            '_label': entity.name}
        if class_types := CLASS_TYPES.get(entity.class_.name):
            record['classified_as'] = list(class_types)
        record['identified_by'] = [
            primary_name(entity.name),
            identifier(
                url_for('api.entity', id_=entity.id, _external=True),
                'Internal Database ID',
                aat_type('300417447', 'internal identification')),
            unique_identifier(entity_uri(entity))]
        if entity.class_.name == 'object_location' \
                and (geometry := self.geometries.get(entity.id)):
            record['defined_by'] = geometry
        for link_ in data.links:
            self._process_link(link_, record, False)
        file_links = []
        for link_ in data.links_inverse:
            if link_.property.code == 'P67' \
                    and link_.domain.class_.name == 'file':
                if g.files.get(link_.domain.id):
                    file_links.append(link_)
                continue
            self._process_link(link_, record, True)
        self._add_media(file_links, record)
        self._add_dates(data.links, record)
        self._finalize_move(record)
        if entity.description:
            self._add_description(record)
        return record

    def _process_link(
            self,
            link_: Link,
            record: dict[str, Any],
            inverse: bool) -> None:
        if handler := self.handlers.get(link_.property.code):
            handler(link_, record, inverse)

    @staticmethod
    def _ref(entity: Entity) -> dict[str, Any]:
        return {
            'id': entity_uri(entity),
            'type': la_type(entity),
            '_label': entity.name}

    def _typed_ref(
            self,
            entity: Entity,
            allowed: set[str]) -> dict[str, Any] | None:
        ref = self._ref(entity)
        return ref if ref['type'] in allowed else None

    def _type_ref(self, type_: Entity) -> dict[str, Any]:
        ref: dict[str, Any] = {
            'id': entity_uri(type_),
            'type': 'Type',
            '_label': type_.name}
        equivalents = []
        for type_link in self.type_refs.get(type_.id, []):
            url = reference_url(type_link)
            if is_close_match(type_link) or not validators.url(url):
                continue
            equivalents.append(
                {'id': url, 'type': 'Type', '_label': type_.name})
        if equivalents:
            ref['equivalent'] = equivalents
        return ref

    def _embedded_event(
            self,
            event: Entity,
            type_name: str,
            link_: Link | None = None) -> dict[str, Any]:
        dates = event.dates
        if link_ and link_.dates.dates_available():
            dates = link_.dates
        node: dict[str, Any] = {
            'type': type_name,
            '_label': event.name,
            'identified_by': [unique_identifier(entity_uri(event))]}
        if link_ and link_.type and (type_ := g.types.get(link_.type.id)):
            node['classified_as'] = [self._type_ref(type_)]
        if timespan := get_timespan(dates, f'Timespan of {event.name}'):
            node['timespan'] = timespan
        if notes := get_date_notes(dates):
            node['referred_to_by'] = notes
        return node

    def _p1(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse:
            append(record, 'identified_by', alias_name(link_.range.name))

    def _p2(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            return
        type_ = link_.range
        if type_.name == 'Radiocarbon' and link_.description:
            self._radiocarbon(link_, record)
        elif link_.description and is_float(link_.description):
            self._dimension(link_, record)
        else:
            append(record, 'classified_as', self._type_ref(type_))

    def _dimension(self, link_: Link, record: dict[str, Any]) -> None:
        type_ = link_.range
        unit = type_.description or 'unit'
        if record['type'] in DIMENSION_ROOTS:
            append(record, 'dimension', {
                'type': 'Dimension',
                '_label': f'{type_.name}: {link_.description} {unit}',
                'classified_as': [self._type_ref(type_)],
                'value': float(link_.description),
                'unit': {
                    'id': 'https://vocab.getty.edu/aat/300226816',
                    'type': 'MeasurementUnit',
                    '_label': unit}})
        else:
            append(record, 'referred_to_by', statement(
                f'{link_.description} {unit}',
                type_.name,
                [self._type_ref(type_)]))

    @staticmethod
    def _radiocarbon(link_: Link, record: dict[str, Any]) -> None:
        data = ast.literal_eval(link_.description)
        year = int(data['radiocarbonYear'])
        range_ = int(data['range'])
        scale = data['timeScale']
        lab_id = data['labId']
        specimen_id = data['specId']
        dating = aat_type('300054717', 'Radiocarbon Dating')
        append(record, 'attributed_by', {
            'type': 'AttributeAssignment',
            '_label': 'Radiocarbon Dating',
            'classified_as': [dating],
            'assigned': [{
                'type': 'Dimension',
                '_label': f'{year} +/- {range_} {scale}',
                'classified_as': [dating],
                'value': year,
                'lower_value_limit': year - range_,
                'upper_value_limit': year + range_,
                'unit': {
                    'id': 'https://vocab.getty.edu/aat/300379244',
                    'type': 'MeasurementUnit',
                    '_label': f'years {scale}'},
                'identified_by': [identifier(
                    str(range_),
                    'Laboratory Error Range',
                    aat_type('300417273', 'error (measure of uncertainty)'))
                ]}],
            'identified_by': [
                identifier(
                    f'{lab_id}-{specimen_id}',
                    'Laboratory ID',
                    aat_type('300460217', 'Laboratory Identifiers')),
                identifier(
                    str(specimen_id),
                    'Specimen ID',
                    aat_type('300404626', 'Identification Numbers'))],
            'carried_out_by': [{
                'id': generate_skolem_id(link_.id, 'radio_group'),
                'type': 'Group',
                '_label': lab_id}]})

    def _p7(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse and record['type'] == 'Activity' \
                and (ref := self._typed_ref(link_.range, {'Place'})):
            append(record, 'took_place_at', ref)

    def _p9(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse and record['type'] == 'Activity' \
                and (ref := self._typed_ref(link_.domain, {'Activity'})):
            record.setdefault('part_of', ref)

    def _p134(
            self,
            link_: Link,
            record: dict[str, Any],
            inverse: bool) -> None:
        if record['type'] == 'Activity' and (ref := self._typed_ref(
                link_.domain if inverse else link_.range, {'Activity'})):
            append(record, 'before' if inverse else 'after', ref)

    def _actor_event(
            self,
            link_: Link,
            record: dict[str, Any],
            inverse: bool) -> None:
        event_key, actor_key = ACTOR_EVENT_KEYS[link_.property.code]
        if not inverse:
            if record['type'] == 'Activity' \
                    and (ref := self._typed_ref(link_.range, ACTORS)):
                append(record, event_key, ref)
        elif record['type'] in ACTORS:
            append(
                record,
                actor_key,
                self._embedded_event(link_.domain, 'Activity', link_))

    def _object_event(
            self,
            link_: Link,
            record: dict[str, Any],
            inverse: bool) -> None:
        if not inverse or record['type'] != 'HumanMadeObject':
            return
        key, type_name, multiple = OBJECT_EVENT_KEYS[link_.property.code]
        node = self._embedded_event(link_.domain, type_name)
        if multiple:
            append(record, key, node)
        else:
            record.setdefault(key, node)

    def _move(
            self,
            link_: Link,
            record: dict[str, Any],
            inverse: bool) -> None:
        if inverse or self.entity.class_.name != 'move':
            return
        part = record.setdefault('part', [{
            'type': 'Move',
            '_label': f'Move of {self.entity.name}'}])[0]
        key = MOVE_KEYS[link_.property.code]
        if key == 'moved':
            if ref := self._typed_ref(link_.range, {'HumanMadeObject'}):
                append(part, key, ref)
        elif ref := self._typed_ref(link_.range, {'Place'}):
            part.setdefault(key, ref)

    @staticmethod
    def _finalize_move(record: dict[str, Any]) -> None:
        if 'part' not in record:
            return
        if 'moved' not in record['part'][0]:
            del record['part']  # A Move without moved objects is invalid
        elif 'participant' in record:
            # Records with parts have no participant property
            for ref in record.pop('participant'):
                append(record, 'influenced_by', ref)

    def _p46(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse and record['type'] == 'HumanMadeObject' \
                and (ref := self._typed_ref(
                    link_.domain, {'HumanMadeObject'})):
            record.setdefault('part_of', ref)

    def _p52(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse and record['type'] == 'HumanMadeObject' \
                and (ref := self._typed_ref(link_.range, ACTORS)):
            append(record, 'current_owner', ref)

    def _p53(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            return
        if record['type'] == 'HumanMadeObject' \
                and (ref := self._typed_ref(link_.range, {'Place'})):
            record.setdefault('current_location', ref)
        elif record['type'] == 'Place' \
                and (geometry := self.geometries.get(link_.range.id)):
            record.setdefault('defined_by', geometry)

    def _p74(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if not inverse and record['type'] in ACTORS \
                and (ref := self._typed_ref(link_.range, {'Place'})):
            append(record, 'residence', ref)

    def _p127(
            self,
            link_: Link,
            record: dict[str, Any],
            inverse: bool) -> None:
        if not inverse and record['type'] == 'Type':
            append(record, 'broader', self._ref(link_.range))

    def _p73(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        translation = link_.range
        if inverse or not translation.description:
            return
        classified_as = []
        if standard_type := translation.standard_type:
            classified_as.append(self._type_ref(standard_type))
        append(record, 'referred_to_by', statement(
            translation.description,
            translation.name,
            classified_as,
            [unique_identifier(entity_uri(translation))]))

    def _p107(
            self,
            link_: Link,
            record: dict[str, Any],
            inverse: bool) -> None:
        if not inverse or record['type'] not in ACTORS:
            return
        group = link_.domain
        group_ref = self._typed_ref(group, {'Group'})
        if not group_ref:
            return
        append(record, 'member_of', group_ref)
        if not (link_.type or link_.dates.dates_available()):
            return  # pragma: no cover
        activity: dict[str, Any] = {
            'type': 'Activity',
            '_label': f'Membership in {group.name}',
            'influenced_by': [group_ref]}
        if link_.type and (type_ := g.types.get(link_.type.id)):
            activity['_label'] = f'Role as {type_.name} at {group.name}'
            activity['classified_as'] = [self._type_ref(type_)]
        if timespan := get_timespan(link_.dates, f'Timespan of {group.name}'):
            activity['timespan'] = timespan
        if notes := get_date_notes(link_.dates):  # pragma: no cover
            activity['referred_to_by'] = notes
        append(record, 'carried_out', activity)

    def _oa7(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if record['type'] not in ACTORS:
            return
        other = link_.domain if inverse else link_.range
        if not (ref := self._typed_ref(other, ACTORS)):
            return  # pragma: no cover
        activity: dict[str, Any] = {
            'type': 'Activity',
            '_label':
                f'Relationship between {link_.domain.name} '
                f'and {link_.range.name}',
            'carried_out_by': [ref]}
        if link_.type and (type_ := g.types.get(link_.type.id)):
            activity['classified_as'] = [self._type_ref(type_)]
        if timespan := get_timespan(
                link_.dates,
                f'Timespan of relationship with {other.name}'):
            activity['timespan'] = timespan  # pragma: no cover
        append(record, 'participated_in', activity)

    def _p67(self, link_: Link, record: dict[str, Any], inverse: bool) -> None:
        if inverse:
            self._referenced_by(link_, record)
        else:
            self._refers_to(link_, record)

    def _referenced_by(self, link_: Link, record: dict[str, Any]) -> None:
        domain = link_.domain
        if domain.cidoc_class.code == 'E32':
            self._authority_reference(link_, record)
        elif domain.class_.name == 'external_reference':
            append(record, 'subject_of', self._web_page(domain))
        else:
            append(record, 'referred_to_by', self._citation(link_))

    def _refers_to(self, link_: Link, record: dict[str, Any]) -> None:
        target = link_.range
        if record['type'] == 'DigitalObject':
            append(record, 'digitally_shows', {
                'id': generate_skolem_id(link_.id, 'visual_item'),
                'type': 'VisualItem',
                '_label': f'Visual content of {self.entity.name}'
                          f' ({target.name})'})
        elif record['type'] == 'LinguisticObject' \
                and self.entity.class_.name != 'reference_system':
            append(record, 'about', self._ref(target))
            if link_.description:
                append(record, 'referred_to_by', statement(
                    link_.description,
                    f'Reference to {target.name}',
                    [aat_type('300200294', 'pagination')],
                    [unique_identifier(entity_uri(target))]))

    def _citation(self, link_: Link) -> dict[str, Any]:
        domain = link_.domain
        classified_as = []
        if standard_type := domain.standard_type:
            classified_as.append(self._type_ref(standard_type))
        if aat := BIBLIOGRAPHY_AAT.get(domain.class_.name):
            classified_as.append(aat)
            classified_as.append(category_aat(
                '300311705',
                'citations (bibliographic references)'))
        if domain.class_.name == 'source':
            classified_as.append(category_aat(
                '300435428',
                'historical/cultural context'))
        identified_by = [unique_identifier(entity_uri(domain))]
        if link_.description:
            pagination = alias_name(link_.description)
            pagination['classified_as'] = [
                aat_type('300200294', 'pagination')]
            identified_by.insert(0, pagination)
        return statement(
            domain.description or domain.name,
            domain.name,
            classified_as,
            identified_by)

    @staticmethod
    def _web_page(domain: Entity) -> dict[str, Any]:
        web_page = category_aat('300264578', 'web page')
        page: dict[str, Any] = {
            'type': 'LinguisticObject',
            '_label': domain.name,
            'classified_as': [
                web_page,
                category_aat('300435416', 'description')],
            'language': [get_language()],
            'identified_by': [unique_identifier(entity_uri(domain))],
            'digitally_carried_by': [{
                'type': 'DigitalObject',
                '_label': domain.name,
                'classified_as': [web_page],
                'format': 'text/html',
                'access_point': [{
                    'id': domain.name,
                    'type': 'DigitalObject',
                    '_label': domain.name}]}]}
        if domain.description:  # pragma: no cover
            page['referred_to_by'] = [
                statement(domain.description, 'Description')]
        return page

    def _authority_reference(
            self,
            link_: Link,
            record: dict[str, Any]) -> None:
        if not link_.description:
            return  # pragma: no cover
        system = g.reference_systems[link_.domain.id]
        url = f'{system.resolver_url or ''}{link_.description}'
        if validators.url(url):
            match = {
                'id': url,
                'type': record['type'],
                '_label': record['_label']}
            if is_close_match(link_):
                append(record, 'attributed_by', {
                    'type': 'AttributeAssignment',
                    '_label': 'Close Match assignment',
                    'classified_as': [CLOSE_MATCH],
                    'assigned': [match]})
            else:
                append(record, 'equivalent', match)
        authority = identifier(
            link_.description,
            f'{link_.domain.name} Identifier',
            aat_type('300404626', 'Authority Control Number'))
        authority['assigned_by'] = [{
            'type': 'AttributeAssignment',
            '_label': f'Authority assignment by {link_.domain.name}',
            'carried_out_by': [{
                'id':
                    system.website_url
                    or generate_skolem_id(link_.id, 'group'),
                'type': 'Group',
                '_label': link_.domain.name}]}]
        append(record, 'identified_by', authority)

    def _add_media(
            self,
            file_links: list[Link],
            record: dict[str, Any]) -> None:
        entity = self.entity
        if file_links:
            shown_by = []
            for link_ in file_links:
                file_ = link_.domain
                mime_type, _ = mimetypes.guess_type(g.files[file_.id])
                digital_object = {
                    'type': 'DigitalObject',
                    '_label': file_.name,
                    'identified_by': [unique_identifier(entity_uri(file_))]
                } | self._digital_details(file_, mime_type)
                if mime_type == 'application/pdf':  # pragma: no cover
                    append(record, 'subject_of', {
                        'type': 'LinguisticObject',
                        '_label': file_.name,
                        'language': [get_language()],
                        'classified_as': [
                            category_aat('300424602', 'Digital documents')],
                        'digitally_carried_by': [digital_object]})
                else:
                    shown_by.append(digital_object)
            if shown_by:
                append(record, 'representation', {
                    'type': 'VisualItem',
                    '_label': 'Visual Representations',
                    'digitally_shown_by': shown_by})
            for item in self._iiif_subject_of(file_links):
                append(record, 'subject_of', item)
        if entity.class_.name == 'file' and g.files.get(entity.id):
            self._add_file_details(record)

    def _digital_details(
            self,
            file_: Entity,
            mime_type: str | None) -> dict[str, Any]:
        details: dict[str, Any] = {}
        if mime_type:
            details['format'] = mime_type
            for prefix, classification in MIME_CLASSIFICATIONS.items():
                if prefix in mime_type:
                    details['classified_as'] = list(classification)
        file_path = get_file_path(file_.id)
        if file_path and file_path.stem:
            details['access_point'] = [{
                'id': url_for(
                    'api.display', filename=file_path.stem, _external=True),
                'type': 'DigitalObject',
                '_label': file_path.stem}]
        referred_to_by = []
        if license_ := get_license_type(file_):
            referred_to_by.append(self._license(license_, file_.name))
        copyright_ = aat_type('300435434', 'copyright/licensing statement')
        referred_to_by.extend(
            statement(holder.name, 'Rights holder', [copyright_])
            for holder in file_.license_holder or [])
        if referred_to_by:
            details['referred_to_by'] = referred_to_by
        return details

    def _license(self, license_: Entity, file_name: str) -> dict[str, Any]:
        classified_as: list[dict[str, Any]] = [
            aat_type('300435434', 'copyright/licensing statement')]
        classified_as.extend(
            {'id': reference_url(type_link),
             'type': 'Type',
             '_label': license_.name}
            for type_link in self.type_refs.get(license_.id, []))
        return statement(
            license_.name,
            f'License of {file_name}',
            classified_as,
            [primary_name(license_.name), unique_identifier(
                entity_uri(license_))])

    def _add_file_details(self, record: dict[str, Any]) -> None:
        entity = self.entity
        file_size = entity.get_file_size()
        value, unit = file_size.split()
        number = float(value)
        append(record, 'dimension', {
            'type': 'Dimension',
            '_label': file_size,
            'classified_as': [aat_type('300265863', 'File Size')],
            'value': int(number) if number.is_integer() else number,
            'unit': {
                'id': 'https://vocab.getty.edu/aat/300265870',
                'type': 'MeasurementUnit',
                '_label': UNIT_MAP[unit]}})
        mime_type, _ = mimetypes.guess_type(g.files[entity.id])
        details = self._digital_details(entity, mime_type)
        for key in ('classified_as', 'referred_to_by'):
            for item in details.pop(key, []):
                append(record, key, item)
        record.update(details)
        if creators := entity.creator:
            record['created_by'] = {
                'type': 'Creation',
                '_label': f'Creation of {entity.name}',
                'carried_out_by': [{
                    'id': generate_skolem_id(creator.id, 'rights_holder'),
                    'type':
                        'Person' if creator.class_ == 'person' else 'Group',
                    '_label': creator.name} for creator in creators]}

    @staticmethod
    def _iiif_subject_of(file_links: list[Link]) -> list[dict[str, Any]]:
        subject_of = []
        for link_ in file_links:
            manifest_path = get_iiif_manifest_and_path(link_.domain.id)
            if not (manifest_path.get('IIIFManifest')
                    and manifest_path.get('IIIFBasePath')):
                continue  # pragma: no cover
            label = f'IIIF manifest of {link_.domain.name}'
            subject_of.append({
                'type': 'LinguisticObject',
                '_label': label,
                'classified_as': [
                    category_aat('300266076', 'metadata (descriptive)')],
                'language': [get_language()],
                'digitally_carried_by': [{
                    'type': 'DigitalObject',
                    '_label': label,
                    'access_point': [{
                        'id': manifest_path['IIIFManifest'],
                        'type': 'DigitalObject',
                        '_label': label}],
                    'conforms_to': [{
                        'id': 'https://iiif.io/api/presentation/2.0/',
                        'type': 'InformationObject',
                        '_label': 'IIIF Presentation API 2.0'}],
                    'format':
                        "application/ld+json;profile='https://iiif.io"
                        "/api/presentation/2/context.json'"}]})
        return subject_of

    def _add_dates(self, links: list[Link], record: dict[str, Any]) -> None:
        entity = self.entity
        if record['type'] == 'Activity':
            if timespan := get_timespan(
                    entity.dates,
                    f'Timespan of {entity.name}'):
                record['timespan'] = timespan
            for note in get_date_notes(entity.dates):
                append(record, 'referred_to_by', note)
        elif config := LIFE_EVENTS.get(entity.class_.name):
            self._add_life_events(links, record, config)

    def _add_life_events(
            self,
            links: list[Link],
            record: dict[str, Any],
            config: dict[str, str]) -> None:
        entity = self.entity
        dates = entity.dates
        for key, type_name, span, code, comment in (
                (config['begin_key'], config['begin_type'],
                 get_begin_span(dates), 'OA8', dates.begin_comment),
                (config['end_key'], config['end_type'],
                 get_end_span(dates), 'OA9', dates.end_comment)):
            event: dict[str, Any] = {
                'type': type_name,
                '_label': f'{type_name} of {entity.name}'}
            if span:
                event['timespan'] = {
                    'type': 'TimeSpan',
                    '_label': f'Timespan of {type_name} of {entity.name}'
                } | span
            for link_ in links:
                if link_.property.code == code \
                        and (ref := self._typed_ref(link_.range, {'Place'})):
                    append(event, 'took_place_at', ref)
            if comment:
                event['referred_to_by'] = [statement(
                    comment,
                    f'{type_name} comment',
                    [category_aat('300027200', 'Note')])]
            if not (span or 'took_place_at' in event):
                continue
            if existing := record.get(key):
                for name, value in event.items():
                    existing.setdefault(name, value)
            else:
                record[key] = event

    def _add_description(self, record: dict[str, Any]) -> None:
        entity = self.entity
        append(record, 'referred_to_by', statement(
            entity.description,
            'Description',
            [category_aat('300435416', 'description')]))
        for annotation in AnnotationText.get_by_source_id(entity.id) or []:
            append(record, 'referred_to_by', self._annotation(annotation))

    def _annotation(
            self,
            annotation: AnnotationText) -> dict[str, Any]:  # pragma: no cover
        text = self.entity.description or ''
        inner_text = text[annotation.link_start:annotation.link_end]
        result = statement(
            inner_text,
            f'Annotation: {inner_text}',
            [category_aat('300026100', 'Annotation')],
            [identifier(
                f'{annotation.link_start}-{annotation.link_end}',
                'Text position',
                aat_type('300055590', 'Selectors'))])
        if annotation.entity_id:
            linked = get_entity_by_id(annotation.entity_id)
            result['identified_by'].append(
                identifier(entity_uri(linked), f'Annotated: {linked.name}'))
        if annotation.text:
            result['referred_to_by'] = [statement(
                annotation.text,
                annotation.text,
                [category_aat('300027200', 'Note')])]
        return result
