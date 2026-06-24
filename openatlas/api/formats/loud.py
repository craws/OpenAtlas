import ast
import hashlib
import mimetypes
from collections import defaultdict
from typing import Any

import validators
from flask import g, url_for

from openatlas import app
from openatlas.api.resources.util import (
    date_to_utc_iso_str,
    get_iiif_manifest_and_path,
    get_license_type, is_float, remove_spaces_dashes)
from openatlas.database.gis import get_wkt_by_id
from openatlas.display.util2 import get_file_path
from openatlas.models.annotation import AnnotationText
from openatlas.models.entity import Entity, Link

LANGUAGES: dict[str, dict[str, Any]] = {
    'en': {
        'id': 'https://vocab.getty.edu/aat/300388277',
        'type': 'Language',
        '_label': 'English'},
    'de': {
        'id': 'https://vocab.getty.edu/aat/300388344',
        'type': 'Language',
        '_label': 'German'},
    'fr': {
        'id': 'https://vocab.getty.edu/aat/300388306',
        'type': 'Language',
        '_label': 'French'},
    'it': {
        'id': 'https://vocab.getty.edu/aat/300388474',
        'type': 'Language',
        '_label': 'Italian'},
    'es': {
        'id': 'https://vocab.getty.edu/aat/300389311',
        'type': 'Language',
        '_label': 'Spanish'},
    'sr': {
        'id': 'https://vocab.getty.edu/aat/300389248',
        'type': 'Language',
        '_label': 'Serbian'},
    'sl': {
        'id': 'https://vocab.getty.edu/aat/300389291',
        'type': 'Language',
        '_label': 'Slovenian'},
    'cs': {
        'id': 'https://vocab.getty.edu/aat/300388191',
        'type': 'Language',
        '_label': 'Czech'},
    'sk': {
        'id': 'https://vocab.getty.edu/aat/300389290',
        'type': 'Language',
        '_label': 'Slovak'}}

UNIT_MAP = {
    'B': 'bytes',
    'KB': 'kilobytes',
    'MB': 'megabytes',
    'GB': 'gigabytes',
    'TB': 'terabytes'}

TYPE_OVERWRITES = {
    'file': 'DigitalObject',
    'human_remains': 'BiologicalObject',
    'place': 'Site',
    'feature': 'HumanMadeFeature',
    'stratigraphic_unit':
        'https://www.cidoc-crm.org/extensions/crmarchaeo/'
        'A8_Stratigraphic_Unit'}


def aat_type(id_: str, label: str) -> dict[str, str]:
    return {
        'id': f'https://vocab.getty.edu/aat/{id_}',
        'type': 'Type',
        '_label': label}


ARCHAEOLOGY_AAT: dict[str, dict[str, str]] = {
    'artifact': aat_type('300117127', 'artifacts'),
    'human_remains': aat_type('300379896', 'human remains')}

MIME_CLASSIFICATIONS: dict[str, list[dict[str, str]]] = {
    'image/': [aat_type('300215302', 'Digital image')],
    'application/pdf': [aat_type('300424602', 'Digital documents')],
    'model/': [
        aat_type('300266011', 'Digital File Format'), {
            'id': 'https://www.wikidata.org/wiki/Q3859833',
            'type': 'Type',
            '_label': '3D Model'}]}

BIBLIOGRAPHY_AAT: dict[str, dict[str, str]] = {
    'bibliography': aat_type('300026497', 'bibliography'),
    'edition': aat_type('300121294', 'edition')}


def get_language() -> dict[str, Any]:
    code = app.config.get('ARCHE_METADATA', {}).get('language', 'en')
    return LANGUAGES.get(code, LANGUAGES['en'])


def category_aat(id_: str, label: str) -> dict[str, Any]:
    return aat_type(id_, label) \
        | {'classified_as': [aat_type('300137954', 'documents (by form)')]}


def primary_name(
        content: str,
        label: str | None = None,
        id_: str | None = None) -> dict[str, Any]:
    name: dict[str, Any] = {
        'type': 'Name',
        '_label': label or content,
        'content': content,
        'classified_as': [aat_type('300404670', 'primary name')],
        'language': [get_language()]}
    if id_:
        name = {'id': id_} | name
    return name


def entity_uri(entity: Entity) -> str:
    return url_for('api.entity_uuid', uuid=entity.uuid, _external=True)


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


def close_match_attribution(
        skolem_id: str,
        assigned: dict[str, Any]) -> dict[str, Any]:
    return {
        'id': skolem_id,
        'type': 'AttributeAssignment',
        '_label': 'Close Match assignment',
        'classified_as': [{
            'id': 'http://www.w3.org/2004/02/skos/core#closeMatch',
            'type': 'Type',
            '_label': 'Close Match'}],
        'assigned': assigned}


class LoudFormatter:
    def __init__(
            self,
            loud_context: dict[str, str],
            type_references: dict[int, list[Link]]) -> None:
        self.loud = loud_context
        self.type_refs = type_references
        self.handlers: dict[str, Any] = {
            'P1': self._handle_p1,
            'P2': self._handle_p2,
            'P67': self._handle_p67,
            'P73': self._handle_p73,
            'OA7': self._handle_oa7}

    def _loud_relation(self, link_: Link, is_inverse: bool) -> str:
        return self.loud[
            get_loud_crm_relation(link_, is_inverse).replace(' ', '_')]

    def get_property_key(self, link_: Link, is_inverse: bool) -> str:
        code = link_.property.code
        if code == 'OA7':
            return 'participated_in'
        if is_inverse and link_.domain.class_.name == 'external_reference':
            return 'subject_of'
        if not is_inverse and code == 'P67':
            if link_.domain.class_.name == 'file':
                return 'digitally_carries'
            return 'refers_to'
        if not is_inverse and code == 'P73':
            return 'referred_to_by'
        if code == 'P53' and link_.domain.class_.name == 'artifact':
            return 'current_location'
        if code == 'P2' and link_.description:
            return 'dimension'
        if code == 'P127':
            return 'part' if is_inverse else 'part_of'
        if code == 'P46':
            classes = {
                link_.domain.class_.name,
                link_.range.class_.name}
            if classes & {'artifact', 'human_remains'}:
                return 'occupies' if is_inverse else 'occupied_by'
        return self._loud_relation(link_, is_inverse)

    def format_link(self, link_: Link, is_domain: bool) -> dict[str, Any]:
        target = link_.domain if is_domain else link_.range
        property_: dict[str, Any] = {
            'id': entity_uri(target),
            'type': self._resolve_type(target),
            '_label': target.name,
            'identified_by': self._inline_identifiers(target)}
        if link_.dates.begin_from or link_.dates.end_from:
            property_ = property_ | self.get_loud_timespan(link_)
        code_ = link_.property.code
        if code_ != 'P2' and link_.type:
            property_['classified_as'] = [
                self._format_type_property(g.types[link_.type.id])]
        if code_ == 'P67' and link_.domain.class_.name == 'file':
            property_ = {
                'id': self.generate_skolem_id(link_.domain.id, 'visual_item'),
                "type": "VisualItem",
                "_label": f"Visual content of {link_.domain.name}",
                "represents": [property_]}
        self._prepend_archaeology_classification(target, property_)
        if handler := self.handlers.get(code_):
            return handler(property_, link_, is_domain)
        return property_

    @staticmethod
    def _prepend_archaeology_classification(
            entity: Entity,
            property_: dict[str, Any]) -> None:
        if aat := ARCHAEOLOGY_AAT.get(entity.class_.name):
            property_['classified_as'] = (
                    [aat] + property_.get('classified_as', []))

    @staticmethod
    def base_entity_dict(entity: Entity) -> dict[str, Any]:
        result: dict[str, Any] = {
            'id': entity_uri(entity),
            'type': LoudFormatter._resolve_type(entity),
            '_label': entity.name}
        LoudFormatter._prepend_archaeology_classification(entity, result)
        return result

    @staticmethod
    def _resolve_type(entity: Entity) -> str:
        return TYPE_OVERWRITES.get(
            entity.class_.name,
            remove_spaces_dashes(entity.cidoc_class.i18n['en']))

    @staticmethod
    def get_file_dimensions(entity: Entity) -> dict[str, Any]:
        file_size = entity.get_file_size()
        value, unit = file_size.split()
        return {'dimension': [{
            'id': LoudFormatter.generate_skolem_id(entity.id, 'file_size'),
            "type": "Dimension",
            "_label": file_size,
            "classified_as": [aat_type('300265863', 'File Size')],
            "value": int(value),
            "unit": {
                "id": "https://vocab.getty.edu/aat/300265870",
                "type": "MeasurementUnit",
                "_label": UNIT_MAP[unit]}}]}

    def get_digital_object_details(
            self,
            entity: Entity,
            mime_type: str | None = None) -> dict[str, Any]:
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(g.files[entity.id])
        digital_object: dict[str, Any] = {'format': mime_type}
        for prefix, classification in MIME_CLASSIFICATIONS.items():
            if mime_type and prefix in mime_type:
                digital_object['classified_as'] = classification
        file_ = get_file_path(entity.id)
        if file_ and file_.stem:
            digital_object['access_point'] = [{
                "id": url_for(
                    'api.display', filename=file_.stem, _external=True),
                "type": "DigitalObject",
                "_label": file_.stem}]
        digital_object['right_held_by'] = []
        for license_holder in entity.license_holder or []:
            license_holder.uuid = self.generate_skolem_id(
                license_holder.id,
                'rights_holder')
            digital_object['right_held_by'].append({
                'id': license_holder.uuid,
                '_label': license_holder.name,
                'type': (license_holder.class_ or 'Actor').capitalize(),
                'identified_by': self._inline_identifiers(license_holder)})
        carried_out_by = []
        for creator in entity.creator or []:
            creator.uuid = self.generate_skolem_id(
                creator.id,
                'rights_holder')
            carried_out_by.append({
                'id': creator.uuid,
                '_label': creator.name,
                'type': (creator.class_ or 'Actor').capitalize(),
                'identified_by': self._inline_identifiers(creator)})
        digital_object['created_by'] = {
            'id': self.generate_skolem_id(
                entity.id, f'{entity.id}_creation'),
            '_label': f'Creation of {entity.name}',
            'type': 'Creation',
            'carried_out_by': carried_out_by}
        if license_ := get_license_type(entity):
            digital_object['referred_to_by'] = [
                self._build_license(license_, entity.name)]
        return digital_object

    def _build_license(
            self, license_: Entity, entity_name: str) -> dict[str, Any]:
        classified_as: list[dict[str, Any]] = [
            aat_type('300435434', 'copyright/licensing statement')]
        classified_as.extend(
            {
                "id": reference_url(type_link),
                "type": "Type",
                "_label": license_.name}
            for type_link in self.type_refs.get(license_.id, []))
        return {
            'id': self.generate_skolem_id(license_.id, 'license'),
            'type': 'LinguisticObject',
            '_label': f'License of {entity_name}',
            'classified_as': classified_as,
            'language': [get_language()],
            'identified_by': [
                primary_name(license_.name, id_=entity_uri(license_))]}

    @staticmethod
    def handle_radiocarbon(
            link_: Link, properties_set: dict[str, Any]) -> None:
        data = ast.literal_eval(link_.description)
        year = int(data['radiocarbonYear'])
        rng = int(data['range'])
        scale = data['timeScale']
        lab_id = data['labId']
        spec_id = data['specId']
        skolem = LoudFormatter.generate_skolem_id
        dating = aat_type('300054717', 'Radiocarbon Dating')
        properties_set['attributed_by'].append({
            'id': skolem(link_.id, 'radiocarbon'),
            "type": "AttributeAssignment",
            "_label": "Radiocarbon Dating",
            "classified_as": [dating],
            "assigned": [{
                'id': skolem(link_.id, 'radiocarbon_dimension'),
                "type": "Dimension",
                "_label": f'{year} +/- {rng} {scale}',
                "classified_as": [dating],
                "value": year,
                "lower_value_limit": year - rng,
                "upper_value_limit": year + rng,
                "unit": {
                    "id": "https://vocab.getty.edu/aat/300379244",
                    "type": "MeasurementUnit",
                    "_label": f"years {scale}"},
                "referred_to_by": [{
                    'id': skolem(link_.id, 'radiocarbon_error'),
                    "type": "LinguisticObject",
                    "content": str(rng),
                    "_label": "Laboratory Error Range",
                    "language": [get_language()],
                    "classified_as": [category_aat(
                        '300417273',
                        'error (measure of uncertainty)')]}]}],
            "identified_by": [{
                'id': skolem(link_.id, 'laboratory'),
                "type": "Identifier",
                "content": f"{lab_id}-{spec_id}",
                "_label": "Laboratory ID",
                "classified_as": [aat_type(
                    '300460217', 'Laboratory Identifiers')]}, {
                'id': skolem(link_.id, 'specimen'),
                "type": "Identifier",
                "content": str(spec_id),
                "_label": "Specimen ID",
                "classified_as": [aat_type(
                    '300404626', 'Identification Numbers')]}],
            "carried_out_by": [{
                'id': skolem(link_.id, 'radio_group'),
                "type": "Group",
                "_label": lab_id,
                "identified_by": [primary_name(lab_id)]}]})

    @staticmethod
    def _handle_p1(
            property_: dict[str, Any],
            link_: Link,
            is_domain: bool) -> dict[str, Any]:
        target = link_.domain if is_domain else link_.range
        property_['id'] = LoudFormatter.generate_skolem_id(
            link_.id, 'appellation')
        property_['content'] = target.name
        return property_

    def _handle_p2(
            self,
            property_: dict[str, Any],
            link_: Link,
            is_domain: bool) -> dict[str, Any]:
        target = link_.domain if is_domain else link_.range
        if link_.description and is_float(link_.description):
            property_['id'] = LoudFormatter.generate_skolem_id(
                link_.id,
                'dimension')
            property_['type'] = 'Dimension'
            property_['value'] = float(link_.description)
            property_['unit'] = {
                "id": "https://vocab.getty.edu/aat/300226816",
                'type': "MeasurementUnit",
                '_label': target.description}
            property_['classified_as'] = [{
                "id": "https://vocab.getty.edu/aat/300379096",
                'type': "Type",
                '_label': target.description}]
            return property_
        self._append_type_references(property_, target)
        return property_

    def _append_type_references(
            self,
            property_: dict[str, Any],
            type_entity: Entity) -> None:
        equivalents: list[dict[str, Any]] = []
        attributed_by: list[dict[str, Any]] = []
        for type_link in self.type_refs.get(type_entity.id, []):
            url = reference_url(type_link)
            if not validators.url(url):  # pragma: no cover
                continue
            ref = {
                'id': url,
                'type': 'Type',
                '_label': type_entity.name}
            if is_close_match(type_link):  # pragma: no cover
                attributed_by.append(close_match_attribution(
                    self.generate_skolem_id(type_link.id, 'close_match'),
                    ref))
            else:
                equivalents.append(ref)
        if equivalents:
            property_['equivalent'] = equivalents
        if attributed_by:  # pragma: no cover
            property_['attributed_by'] = attributed_by

    def _handle_p73(
            self,
            property_: dict[str, Any],
            link_: Link,
            is_domain: bool) -> dict[str, Any]:
        if is_domain:
            return property_
        property_['content'] = link_.range.description
        if link_.range.standard_type:
            property_['classified_as'] = [self._format_type_property(
                g.types[link_.range.standard_type.id])]
        return property_

    def _handle_p67(
            self,
            property_: dict[str, Any],
            link_: Link,
            is_domain: bool) -> dict[str, Any]:
        if not is_domain:
            if link_.description:
                property_['content'] = link_.description
            return property_
        domain = link_.domain
        property_['classified_as'] = []
        property_['type'] = (
            'DigitalObject' if domain.class_.name == 'file'
            else 'LinguisticObject')
        if standard_type := domain.standard_type:
            property_['classified_as'].append(
                self._format_type_property(standard_type))
        if link_.description:
            pagination = primary_name(
                link_.description,
                id_=self.generate_skolem_id(link_.id, 'pagination'))
            pagination['classified_as'] = (
                    [aat_type('300200294', 'pagination')]
                    + pagination['classified_as'])
            property_['identified_by'] = [pagination]
        if aat := BIBLIOGRAPHY_AAT.get(domain.class_.name):
            property_['classified_as'].append(aat)
            property_['classified_as'].append(category_aat(
                '300311705',
                'citations (bibliographic references)'))
        if property_['type'] == 'LinguisticObject':
            property_['language'] = [get_language()]
        if domain.class_.name == 'source':
            property_['classified_as'].append(category_aat(
                '300435428',
                'historical/cultural context'))
        if domain.class_.name == 'external_reference':
            web_page = category_aat('300264578', 'web page')
            description = category_aat('300435416', 'description')
            property_ = {
                "id": entity_uri(domain),
                "_label": domain.name,
                "classified_as": [web_page, description],
                "type": "LinguisticObject",
                "language": [get_language()],
                "digitally_carried_by": [{
                    "id": self.generate_skolem_id(
                        domain.id, 'web_digital_object'),
                    "type": "DigitalObject",
                    "_label": domain.name,
                    "classified_as": [web_page],
                    "format": "text/html",
                    "access_point": [{
                        "id": domain.name,
                        "_label": domain.name,
                        "type": "DigitalObject"}]}]}
        if domain.description:  # pragma: no cover
            property_['content'] = domain.description
        return property_

    def _handle_oa7(
            self,
            property_: dict[str, Any],
            link_: Link,
            is_domain: bool) -> Any:
        first, second = (link_.range, link_.domain) \
            if is_domain else (link_.domain, link_.range)
        relationship: dict[str, Any] = {
            'id': self.generate_skolem_id(link_.id, 'relationship'),
            'type': 'Event',
            '_label': f'Relationship between {first.name} and {second.name}',
            'had_participant': [property_]}
        if link_.type:
            relationship['classified_as'] = [
                self._format_type_property(g.types[link_.type.id])]
        return [relationship] if is_domain else relationship

    def _format_type_property(self, type_: Entity) -> dict[str, Any]:
        property_: dict[str, Any] = {
            'id': entity_uri(type_),
            'type': self._resolve_type(type_),
            '_label': type_.name}
        if type_.dates.begin_from or type_.dates.end_from:
            property_ = property_ | self.get_loud_timespan(type_)
        equivalents: list[dict[str, Any]] = []
        attributed_by: list[dict[str, Any]] = []
        for type_link in self.type_refs.get(type_.id, []):
            url = reference_url(type_link)
            if not validators.url(url):  # pragma: no cover
                continue
            ref = {
                "id": url,
                "type": "Type",
                "_label": type_.name}
            if is_close_match(type_link):  # pragma: no cover
                attributed_by.append(close_match_attribution(
                    self.generate_skolem_id(type_link.id, 'close_match'),
                    ref))
            else:
                equivalents.append(ref)
        if equivalents:
            property_['equivalent'] = equivalents
        if attributed_by:  # pragma: no cover
            property_['attributed_by'] = attributed_by
        return property_

    @staticmethod
    def generate_skolem_id(id_: int, type_name: str) -> str:
        seed = f"{id_}_{type_name}".encode('utf-8')
        identifier_hash = hashlib.sha256(seed).hexdigest()[:16]
        return url_for(
            "api.skolem_proxy",
            subpath=f'{type_name.lower()}/{identifier_hash}',
            _external=True)

    LIFE_EVENT_CONFIG: dict[str, dict[str, Any]] = {
        'person': {
            'begin_key': 'born',
            'begin_type': 'Birth',
            'end_key': 'died_in',
            'end_type': 'Death',
            'inner_ts_id': False},
        'group': {
            'begin_key': 'formed_by',
            'begin_type': 'Formation',
            'end_key': 'dissolved_by',
            'end_type': 'Dissolution',
            'inner_ts_id': True}}

    def get_loud_timespan(
            self,
            entity: Entity | Link,
            links_: list[Link] | None = None) -> dict[str, Any]:
        if not isinstance(entity, Link) \
                and entity.class_.name in self.LIFE_EVENT_CONFIG:
            return self._get_life_event_timespan(entity, links_)
        if not entity.dates.dates_available():
            return {}
        name = entity.name if isinstance(entity, Entity) \
            else entity.domain.name
        return {'timespan':
                    {'id': self.generate_skolem_id(entity.id, 'timespan'),
                     'type': 'TimeSpan',
                     '_label': f'Timespan of {name}'}
                    | self._get_loud_begin_dates(entity)
                    | self._get_loud_end_dates(entity)}

    def _make_life_event(
            self,
            entity: Entity,
            event_type: str,
            dates: dict[str, Any],
            has_dates: bool) -> dict[str, Any]:
        skolem_key = event_type.lower()
        event: dict[str, Any] = {
            'id': self.generate_skolem_id(entity.id, skolem_key),
            'type': event_type,
            '_label': f'{event_type} of {entity.name}'}
        if has_dates:
            ts_key = 'begin' if event_type in {'Birth', 'Formation'} \
                else 'end'
            timespan: dict[str, Any] = {
                'id': self.generate_skolem_id(entity.id, ts_key),
                'type': 'TimeSpan',
                '_label': f'Timespan of {event_type} of {entity.name}'}
            event['timespan'] = timespan | dates
        return event

    def _get_life_event_timespan(
            self,
            entity: Entity,
            links_: list[Link] | None) -> dict[str, Any]:
        config = self.LIFE_EVENT_CONFIG[entity.class_.name]
        has_begin = bool(entity.dates.begin_from or entity.dates.begin_to)
        has_end = bool(entity.dates.end_from or entity.dates.end_to)
        begin_dates = self._get_loud_begin_dates(entity)
        if 'end_of_the_begin' in begin_dates:
            begin_dates['end_of_the_end'] = begin_dates.pop('end_of_the_begin')
        elif 'begin_of_the_begin' in begin_dates:
            begin_dates['end_of_the_end'] = begin_dates['begin_of_the_begin']
        begin_event = self._make_life_event(
            entity, config['begin_type'],
            begin_dates,
            has_begin)
        end_dates = self._get_loud_end_dates(entity)
        if 'begin_of_the_end' in end_dates:
            end_dates['begin_of_the_begin'] = end_dates.pop('begin_of_the_end')
        elif 'end_of_the_end' in end_dates:  # pragma: no cover
            end_dates['begin_of_the_begin'] = end_dates['end_of_the_end']
        end_event = self._make_life_event(
            entity, config['end_type'],
            end_dates,
            has_end)
        for link_ in links_ or []:
            place = {
                'id': entity_uri(link_.range),
                'type': 'Place',
                '_label': link_.range.name,
                'identified_by': self._inline_identifiers(link_.range)}
            if link_.property.code == 'OA8':
                begin_event['took_place_at'] = [place]
                has_begin = True
            elif link_.property.code == 'OA9':
                end_event['took_place_at'] = [place]
                has_end = True
        result: dict[str, Any] = {}
        if has_begin:
            result[config['begin_key']] = begin_event
        if has_end:
            result[config['end_key']] = end_event
        return result

    @staticmethod
    def _get_loud_begin_dates(entity: Entity | Link) -> dict[str, Any]:
        data = {
            'begin_of_the_begin':
                date_to_utc_iso_str(entity.dates.begin_from),
            'end_of_the_begin': date_to_utc_iso_str(entity.dates.begin_to),
            'beginning_is_qualified_by': entity.dates.begin_comment}
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def _get_loud_end_dates(entity: Entity | Link) -> dict[str, Any]:
        begin_of_the_end = date_to_utc_iso_str(entity.dates.end_from)
        end_of_the_end = date_to_utc_iso_str(entity.dates.end_to)
        if end_of_the_end is None:
            end_of_the_end = begin_of_the_end \
                             or date_to_utc_iso_str(entity.dates.begin_to) \
                             or date_to_utc_iso_str(entity.dates.begin_from)
        data = {
            'begin_of_the_end': begin_of_the_end,
            'end_of_the_end': end_of_the_end,
            'end_is_qualified_by': entity.dates.end_comment}
        return {k: v for k, v in data.items() if v is not None}

    def get_loud_representations(
            self,
            image_links: list[Link],
            properties_set: dict[str, Any]) -> None:
        representation = []
        subject_of = []
        for link_ in image_links:
            entity = link_.domain
            mime_type, _ = mimetypes.guess_type(g.files[entity.id])
            image = {
                'id': entity_uri(entity),
                '_label': entity.name,
                'type': 'VisualWorks'}
            image.update(self.get_digital_object_details(entity, mime_type))
            if mime_type == 'application/pdf':  # pragma: no cover
                subject_of.append({
                    'id': self.generate_skolem_id(entity.id, 'pdf_subject'),
                    'type': 'LinguisticObject',
                    '_label': entity.name,
                    "language": [get_language()],
                    "classified_as": [
                        category_aat('300424602', 'Digital documents')],
                    'digitally_carried_by': [image]})
            else:
                representation.append(image)
        properties_set['representation'].append({
            'id': self.generate_skolem_id(0, 'visual_representation'),
            'type': 'VisualItem',
            "_label": "Visual Representations",
            'digitally_shown_by': representation})
        if subject_of:  # pragma: no cover
            properties_set['subject_of'].extend(subject_of)

    @staticmethod
    def get_iiif_subject_of(image_links: list[Link]) -> list[dict[str, Any]]:
        subject_of = []
        skolem = LoudFormatter.generate_skolem_id
        for link_ in image_links:
            manifest_path = get_iiif_manifest_and_path(link_.domain.id)
            if not (manifest_path.get('IIIFManifest')
                    and manifest_path.get('IIIFBasePath')):
                continue  # pragma: no cover
            label = f'IIIF manifest of {link_.domain.name}'
            subject_of.append({
                'id': skolem(link_.id, 'iif_manifest'),
                "type": "LinguisticObject",
                "_label": label,
                "classified_as": [
                    category_aat('300266076', 'metadata (descriptive)')],
                "language": [get_language()],
                "digitally_carried_by": [{
                    'id': skolem(link_.id, 'DigitalObject'),
                    "type": "DigitalObject",
                    "_label": label,
                    "access_point": [{
                        "id": manifest_path['IIIFManifest'],
                        "_label": label,
                        "type": "DigitalObject"}],
                    "conforms_to": [{
                        "id": "https://iiif.io/api/presentation/2.0/",
                        "type": "InformationObject",
                        "_label": "IIIF Presentation API 2.0"}],
                    "format":
                        "application/ld+json;profile='https://iiif.io"
                        "/api/presentation/2/context.json'"}]})
        return subject_of

    @staticmethod
    def handle_authority_reference(
            link_: Link,
            properties_set: dict[str, Any],
            entity: Entity) -> None:
        system = g.reference_systems[link_.domain.id]
        skolem = LoudFormatter.generate_skolem_id
        match_reference = {
            "id": f'{system.resolver_url or ''}{link_.description}',
            "type": LoudFormatter._resolve_type(entity),
            "_label": entity.name}
        if is_close_match(link_):
            properties_set['attributed_by'].append(
                close_match_attribution(
                    skolem(link_.id, 'close_match'),
                    match_reference))
        else:
            properties_set['equivalent'].append(match_reference)
        properties_set['identified_by'].append({
            'id': skolem(link_.id, 'identifier'),
            "type": "Identifier",
            "content": link_.description,
            "_label": f"{link_.domain.name} Identifier",
            "classified_as": [
                aat_type('300404626', 'Authority Control Number')],
            "attributed_by": [{
                "id": skolem(link_.id, 'authority'),
                "type": "AttributeAssignment",
                "_label": f"Authority assignment by {link_.domain.name}",
                "carried_out_by": [{
                    "id":
                        system.website_url
                        or skolem(link_.id, 'group'),
                    "type": "Group",
                    "_label": link_.domain.name,
                    "identified_by":
                        LoudFormatter._inline_identifiers(link_.domain)}]}]})

    def handle_membership(
            self,
            link_: Link,
            properties_set: dict[str, Any]) -> None:
        domain = link_.domain
        group_ref = {
            'id': entity_uri(domain),
            'type': self._resolve_type(domain),
            '_label': domain.name,
            'identified_by': self._inline_identifiers(domain)}
        properties_set['member_of'].append(group_ref)
        if not (link_.type or link_.dates.dates_available()):
            return  # pragma: no cover
        carried_out: dict[str, Any] = {
            'id': self.generate_skolem_id(link_.id, 'membership'),
            "type": "Activity",
            '_label': f"Membership in {domain.name}",
            "carried_out_on_behalf_of": [dict(group_ref)]}
        if link_.type:
            if type_ := g.types.get(link_.type.id):
                carried_out['_label'] = (
                    f"Role as {type_.name} at {domain.name}")
                carried_out['classified_as'] = [
                    self._format_type_property(type_)]
        if link_.dates.dates_available():
            carried_out = carried_out | self.get_loud_timespan(link_)
        properties_set['carried_out'].append(carried_out)

    def process_link(
            self,
            link_: Link,
            properties_set: dict[str, Any],
            is_inverse: bool,
            root_entity: Entity) -> None:
        code = link_.property.code
        is_domain = is_inverse
        if code == 'P53':
            base_property = self.format_link(link_, is_domain=is_domain)
            key = self.get_property_key(link_, is_inverse)
            if not is_inverse:
                if geometry := get_wkt_by_id(link_.range.id):
                    base_property['defined_by'] = geometry
                properties_set[key] = base_property
            else:
                properties_set[key].append(base_property)
            return
        if is_inverse and code == 'P67' \
                and link_.domain.cidoc_class.code == 'E32':
            self.handle_authority_reference(link_, properties_set, root_entity)
            return
        if is_inverse and code == 'P107':
            self.handle_membership(link_, properties_set)
            return
        if code == 'P2' and link_.range.name == 'Radiocarbon':
            self.handle_radiocarbon(link_, properties_set)
            return
        property_name = self.get_property_key(link_, is_inverse)
        formatted = self.format_link(link_, is_domain=is_domain)
        properties_set[property_name].append(formatted)

    def process_media_links(
            self,
            file_links: list[Link],
            properties_set: dict[str, Any],
            entity: Entity) -> None:
        if file_links:
            self.get_loud_representations(file_links, properties_set)
            if iiif := self.get_iiif_subject_of(file_links):
                properties_set['subject_of'].extend(iiif)
        if entity.class_.name == 'file' and g.files.get(entity.id):
            properties_set.update(self.get_file_dimensions(entity))
            details = self.get_digital_object_details(entity)
            if referred := details.pop('referred_to_by', None):
                properties_set['referred_to_by'].extend(referred)
            properties_set.update(details)

    @staticmethod
    def handle_description(
            entity: Entity,
            properties_set: dict[str, Any]) -> None:
        description: dict[str, Any] = {
            'id': LoudFormatter.generate_skolem_id(entity.id, 'description'),
            "type": "LinguisticObject",
            "_label": "Description",
            "content": entity.description,
            "language": [get_language()],
            "classified_as": [category_aat('300435416', 'description')]}
        annotations = AnnotationText.get_by_source_id(entity.id) or []
        part = [
            LoudFormatter._build_annotation(annotation, entity)
            for annotation in annotations]
        if part:  # pragma: no cover
            description['part'] = part
        properties_set['referred_to_by'].append(description)

    @staticmethod
    def _build_annotation(
            annotation: AnnotationText,
            entity: Entity) -> dict[str, Any]:  # pragma: no cover
        skolem = LoudFormatter.generate_skolem_id
        text = entity.description or ''
        inner_text = text[annotation.link_start:annotation.link_end]
        selector = aat_type('300055590', 'Selectors')
        annotation_dict: dict[str, Any] = {
            'id': skolem(annotation.id, 'annotation'),
            "type": "LinguisticObject",
            "_label": f"Annotation: {inner_text}",
            "content": inner_text,
            "language": [get_language()],
            "classified_as": [category_aat('300026100', 'Annotation')],
            "digitally_carried_by": [{
                'id': skolem(annotation.id, 'annotation_digital_object'),
                "type": "DigitalObject",
                "_label": f"Annotation selector: {inner_text}",
                "classified_as": [selector],
                "referred_to_by": [{
                    "id": skolem(annotation.id, 'annotation_text'),
                    "type": "LinguisticObject",
                    "_label": "Text Position Selector",
                    "content": f'{annotation.text}',
                    "language": [get_language()],
                    "classified_as": [category_aat(
                        '300055590', 'Text Position Selector')],
                    "identified_by": [{
                        "id": skolem(annotation.id, 'link_start'),
                        "type": "Identifier",
                        "_label": "start",
                        "content": f'{annotation.link_start}'}, {
                        "id": skolem(annotation.id, 'link_end'),
                        "type": "Identifier",
                        "_label": "end",
                        "content": f'{annotation.link_end}'}]}]}]}
        if annotation.entity_id:
            linked = Entity.get_by_id(annotation.entity_id)
            annotation_dict['about'] = [{
                'id': entity_uri(linked),
                'type': LoudFormatter._resolve_type(linked),
                '_label': linked.name,
                'identified_by': [
                    primary_name(linked.name), {
                        'id': LoudFormatter.generate_skolem_id(
                            linked.id, 'system_identifier'),
                        "type": "Identifier",
                        "_label": "System Identifier",
                        "content": entity_uri(linked)}]}]
        if annotation.text:
            annotation_dict['referred_to_by'] = [{
                "id": skolem(annotation.id, 'annotation_text'),
                "type": "LinguisticObject",
                "_label": annotation.text,
                "content": annotation.text,
                "language": [get_language()],
                "classified_as": [category_aat('300027200', 'Note')]}]
        return annotation_dict

    @staticmethod
    def _inline_identifiers(entity: Entity) -> list[dict[str, Any]]:
        skolem = LoudFormatter.generate_skolem_id
        internal_id = url_for(
            'api.entity',
            id_=entity.id,
            _external=True,
            format='loud')
        return [
            primary_name(
                entity.name, id_=skolem(entity.id, 'appellation')), {
                'id': internal_id,
                "type": "Identifier",
                "_label": "Internal Database ID",
                "content": internal_id,
                "classified_as": [aat_type('300404629', 'local URI')]}, {
                'id': skolem(entity.id, 'unique_identifier'),
                "type": "Identifier",
                "_label": "Unique Identifier",
                "content": entity_uri(entity),
                "classified_as": [
                    aat_type('300404012', 'unique identifier')]}]

    @staticmethod
    def add_core_metadata(
            entity: Entity,
            properties_set: dict[str, Any]) -> None:
        skolem = LoudFormatter.generate_skolem_id
        identifiers = LoudFormatter._inline_identifiers(entity)
        identifiers[0] = primary_name(
            entity.name,
            id_=skolem(entity.id, 'primary_name'))
        properties_set['identified_by'].extend(identifiers)
        if entity.class_.name == 'object_location':
            if geometry := get_wkt_by_id(entity.id):
                properties_set['defined_by'] = geometry

    def finalize_output(
            self,
            entity: Entity,
            properties_set: dict[str, Any],
            links_data: list[Link]) -> dict[str, Any]:
        self.add_core_metadata(entity, properties_set)
        if entity.description:
            self.handle_description(entity, properties_set)
        return ({'@context': app.config['API_CONTEXT']['LOUD']} |
                self.base_entity_dict(entity) |
                self.get_loud_timespan(entity, links_data) |
                properties_set)


def get_loud_entities(
        data: dict[str, Any],
        loud: dict[str, str],
        type_references: dict[int, list[Link]]) -> Any:
    entity = data['entity']
    formatter = LoudFormatter(loud, type_references)
    properties_set: dict[str, Any] = defaultdict(list)
    skipped = {'OA8', 'OA9'}
    for link_ in data['links']:
        if link_.property.code not in skipped:
            formatter.process_link(
                link_, properties_set, is_inverse=False, root_entity=entity)
    file_links = []
    for link_ in data['links_inverse']:
        if link_.property.code in skipped:
            continue
        domain = link_.domain
        if domain.class_.name == 'file' and g.files.get(domain.id):
            file_links.append(link_)
            continue
        formatter.process_link(
            link_, properties_set, is_inverse=True, root_entity=entity)
    formatter.process_media_links(file_links, properties_set, entity)
    return formatter.finalize_output(entity, properties_set, data['links'])


def get_loud_crm_relation(link_: Link, inverse: bool = False) -> str:
    property_ = f' {link_.property.i18n['en']}'
    if inverse and link_.property.i18n_inverse['en']:
        property_ = f'i {link_.property.i18n_inverse['en']}'
    return f'crm:{link_.property.code}{property_}'
