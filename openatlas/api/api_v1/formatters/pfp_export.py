import re
from typing import Any, Final

from flask import g
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef, XSD

from openatlas.api.api_v1.entity import resolve_type_ids
from openatlas.api.api_v1.formatters.la_helpers import is_float
from openatlas.api.api_v1.formatters.util import (
    EntityLinks, entity_uri, get_links_for_entities)
from openatlas.api.api_v1.models.lod import PfpExportQuery
from openatlas.database.api import get_wkts_by_ids, search_entities_api
from openatlas.models.dates import Dates
from openatlas.models.entity import Entity, Link

CRM = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
FRBROO = Namespace('http://iflastandards.info/ns/fr/frbr/frbroo/')
LRMOO = Namespace('http://iflastandards.info/ns/lrm/lrmoo/')
PFP = Namespace('https://pfp-schema.acdh.oeaw.ac.at/#')
PFPG = Namespace('https://pfp-schema.acdh.oeaw.ac.at/types/gender/#')
GEO = Namespace('http://www.opengis.net/ont/geosparql#')
PFPSH = Namespace('https://pfp-schema.acdh.oeaw.ac.at/shacl/')

EVENT_CLASS_MAP: Final[dict[str, URIRef]] = {
    'activity': CRM.E7_Activity,
    'acquisition': CRM.E8_Acquisition,
    'move': CRM.E9_Move,
    'modification': CRM.E11_Modification,
    'production': CRM.E12_Production,
    'creation': CRM.E65_Creation}

ACTOR_EVENT_PROPERTIES: Final[dict[str, tuple[URIRef, URIRef]]] = {
    'P11': (CRM.P11_had_participant, CRM.P11i_participated_in),
    'P14': (CRM.P14_carried_out_by, CRM.P14i_performed),
    'P22': (CRM.P22_transferred_title_to, CRM.P22i_acquired_title_through),
    'P23': (
        CRM.P23_transferred_title_from,
        CRM.P23i_surrendered_title_through)}

PFP_CLASSES: Final[list[str]] = [
    'person',
    'group',
    'place',
    'bibliography',
    'edition',
    *EVENT_CLASS_MAP.keys()]

GENDER_MAP: Final[dict[str, tuple[URIRef, str, str]]] = {
    'male': (PFPG.male, 'male', 'männlich'),
    'männlich': (PFPG.male, 'male', 'männlich'),
    'female': (PFPG.female, 'female', 'weiblich'),
    'weiblich': (PFPG.female, 'female', 'weiblich'),
    'non-binary': (PFPG['non-binary'], 'non-binary', 'divers'),
    'nonbinary': (PFPG['non-binary'], 'non-binary', 'divers'),
    'divers': (PFPG['non-binary'], 'non-binary', 'divers'),
    'unknown': (PFPG.unknown, 'unknown', 'unbekannt'),
    'unbekannt': (PFPG.unknown, 'unknown', 'unbekannt'),
    'not-applicable': (
        PFPG['not-applicable'], 'not applicable', 'nicht zutreffend'),
    'not applicable': (
        PFPG['not-applicable'], 'not applicable', 'nicht zutreffend')}

DATE_RE: Final = re.compile(r'^(-?\d{4,}-\d{2}-\d{2})')


def _to_xsd_date(value: Any) -> str | None:
    if not value:
        return None
    if match := DATE_RE.match(str(value)):
        return match.group(1)
    return None  # pragma: no cover


def _get_begin_bounds(dates: Dates) -> tuple[str | None, str | None]:
    earliest = _to_xsd_date(dates.begin_from) or _to_xsd_date(dates.begin_to)
    latest = _to_xsd_date(dates.begin_to) or earliest
    return earliest, latest


def _get_end_bounds(dates: Dates) -> tuple[str | None, str | None]:
    earliest = _to_xsd_date(dates.end_from) or _to_xsd_date(dates.end_to)
    latest = _to_xsd_date(dates.end_to) or earliest
    return earliest, latest


def _get_full_bounds(dates: Dates) -> tuple[str | None, str | None]:
    b_start, b_end = _get_begin_bounds(dates)
    e_start, e_end = _get_end_bounds(dates)
    return b_start or e_start, e_end or b_end


def _is_sex_type(type_entity: Entity) -> bool:
    root_ids = getattr(type_entity, 'root', [])
    if root_ids and (root_type := g.types.get(root_ids[0])):
        if root_type.name.lower() in ('sex', 'gender', 'geschlecht'):
            return True
    return type_entity.name.strip().lower() in GENDER_MAP


class PfpFormatter:
    def __init__(
            self,
            geometries: dict[int, str] | None = None,
            event_links: dict[int, EntityLinks] | None = None) -> None:
        self.graph = Graph()
        self.graph.bind('crm', CRM)
        self.graph.bind('frbroo', FRBROO)
        self.graph.bind('lrmoo', LRMOO)
        self.graph.bind('pfp', PFP)
        self.graph.bind('pfpg', PFPG)
        self.graph.bind('rdfs', RDFS)
        self.graph.bind('xsd', XSD)
        self.graph.bind('geo', GEO)
        self.graph.bind('sh', Namespace('http://www.w3.org/ns/shacl#'))
        self.graph.bind('pfpsh', PFPSH)
        self.geometries: dict[int, str] = geometries or {}
        self.event_links: dict[int, EntityLinks] = event_links or {}

    def format_entities(self, items: list[EntityLinks]) -> Graph:
        for item in items:
            self.add_entity_data(item)
        return self.graph

    def add_entity_data(self, data: EntityLinks) -> None:
        entity = data.entity
        if data.geometries:
            self.geometries.update(data.geometries)

        if entity.class_.name in EVENT_CLASS_MAP:
            self._format_event(data)
            return

        match entity.class_.name:
            case 'person':
                self._format_person(data)
            case 'group':
                self._format_group(data)
            case 'place':
                self._format_place(data)
            case 'bibliography' | 'edition':
                self._format_manifestation(data)

    def _add_base_entity(
            self,
            entity: Entity,
            crm_class: URIRef,
            links: list[Link] | None = None,
            links_inverse: list[Link] | None = None) -> URIRef:
        uri = URIRef(entity_uri(entity))
        self.graph.add((uri, RDF.type, crm_class))
        self.graph.add((uri, RDFS.label, Literal(entity.name)))

        app_uri = URIRef(f'{uri}/appellation')
        self.graph.add((uri, CRM.P1_is_identified_by, app_uri))
        self.graph.add((app_uri, RDF.type, CRM.E33_E41_Linguistic_Appellation))
        self.graph.add((app_uri, RDFS.label, Literal(entity.name)))

        id_uri = URIRef(f'{uri}/identifier')
        self.graph.add((uri, CRM.P1_is_identified_by, id_uri))
        self.graph.add((id_uri, RDF.type, CRM.E42_Identifier))
        self.graph.add((id_uri, RDFS.label, Literal(str(uri))))

        for link_ in links or []:
            if link_.property.code == 'P1':
                alias_uri = URIRef(entity_uri(link_.range))
                self.graph.add((uri, CRM.P1_is_identified_by, alias_uri))
                self.graph.add((
                    alias_uri,
                    RDF.type,
                    CRM.E33_E41_Linguistic_Appellation))
                self.graph.add((
                    alias_uri,
                    RDFS.label,
                    Literal(link_.range.name)))

        for link_ in links_inverse or []:
            if (link_.property.code == 'P67'
                    and link_.domain.class_.name == 'reference_system'
                    and link_.description):
                ext_uri = URIRef(f'{uri}/identifier/{link_.id}')
                system = g.reference_systems.get(link_.domain.id)
                ref_val = (
                    f"{system.resolver_url or ''}{link_.description}"
                    if system else link_.description)
                self.graph.add((uri, CRM.P1_is_identified_by, ext_uri))
                self.graph.add((ext_uri, RDF.type, CRM.E42_Identifier))
                self.graph.add((ext_uri, RDFS.label, Literal(ref_val)))

        return uri

    def _add_timespan(
            self,
            ts_uri: URIRef,
            label: str,
            earliest: str | None,
            latest: str | None) -> URIRef:
        self.graph.add((ts_uri, RDF.type, CRM['E52_Time-Span']))
        self.graph.add((ts_uri, RDFS.label, Literal(label)))
        if earliest and latest:
            if earliest == latest:
                self.graph.add((
                    ts_uri,
                    CRM.P82_at_some_time_within,
                    Literal(earliest, datatype=XSD.date)))
            else:
                self.graph.add((
                    ts_uri,
                    CRM.P82a_begin_of_the_begin,
                    Literal(earliest, datatype=XSD.date)))
                self.graph.add((
                    ts_uri,
                    CRM.P82b_end_of_the_end,
                    Literal(latest, datatype=XSD.date)))
        return ts_uri

    def _ensure_type(self, type_entity: Entity) -> URIRef:
        type_uri = URIRef(entity_uri(type_entity))
        self.graph.add((type_uri, RDF.type, CRM.E55_Type))
        self.graph.add((type_uri, RDFS.label, Literal(type_entity.name)))
        return type_uri

    def _ensure_place_ref(self, place_entity: Entity) -> URIRef:
        place_uri = self._add_base_entity(place_entity, CRM.E53_Place)
        if (place_uri, CRM.P168_place_is_defined_by, None) not in self.graph:
            if wkt := self.geometries.get(place_entity.id):
                self.graph.add((
                    place_uri,
                    CRM.P168_place_is_defined_by,
                    Literal(wkt, datatype=GEO.wktLiteral)))
        return place_uri

    def _format_place(self, data: EntityLinks) -> URIRef:
        entity = data.entity
        place_uri = self._add_base_entity(
            entity,
            CRM.E53_Place,
            data.links,
            data.links_inverse)
        wkt = self.geometries.get(entity.id)
        if not wkt:
            for link_ in data.links:
                if link_.property.code == 'P53':
                    if loc_wkt := self.geometries.get(link_.range.id):
                        wkt = loc_wkt
                        break
        if wkt and (
                place_uri,
                CRM.P168_place_is_defined_by,
                None) not in self.graph:
            self.graph.add((
                place_uri,
                CRM.P168_place_is_defined_by,
                Literal(wkt, datatype=GEO.wktLiteral)))
        return place_uri

    def _format_event(self, data: EntityLinks) -> URIRef:
        entity = data.entity
        event_uri = self._add_base_entity(
            entity,
            EVENT_CLASS_MAP.get(entity.class_.name, CRM.E7_Activity),
            data.links,
            data.links_inverse)

        earliest, latest = _get_full_bounds(entity.dates)
        if (earliest
                or entity.dates.begin_comment
                or entity.dates.end_comment):
            ts_label = (
                entity.dates.begin_comment
                or entity.dates.end_comment
                or f'Timespan of {entity.name}')
            ts_uri = self._add_timespan(
                URIRef(f'{event_uri}/timespan'),
                ts_label,
                earliest,
                latest)
            self.graph.add((event_uri, CRM['P4_has_time-span'], ts_uri))

        for link_ in data.links:
            self._add_event_link(event_uri, link_)
        return event_uri

    def _add_event_link(self, event_uri: URIRef, link_: Link) -> None:
        code = link_.property.code
        if code == 'P2':
            if not (link_.description and is_float(link_.description)):
                type_entity = g.types.get(link_.range.id, link_.range)
                self.graph.add((
                    event_uri,
                    CRM.P2_has_type,
                    self._ensure_type(type_entity)))
        elif code in ('P7', 'P26', 'P27'):
            place_uri = self._ensure_place_ref(link_.range)
            pred = (
                CRM.P7_took_place_at if code == 'P7'
                else (CRM.P26_moved_to if code == 'P26'
                      else CRM.P27_moved_from))
            self.graph.add((event_uri, pred, place_uri))
        elif (code in ACTOR_EVENT_PROPERTIES
                and link_.range.class_.name in ('person', 'group')):
            fwd_prop, inv_prop = ACTOR_EVENT_PROPERTIES[code]
            actor_cls = (
                CRM.E21_Person
                if link_.range.class_.name == 'person'
                else CRM.E74_Group)
            actor_uri = self._add_base_entity(link_.range, actor_cls)
            self.graph.add((event_uri, fwd_prop, actor_uri))
            self.graph.add((actor_uri, inv_prop, event_uri))

    def _add_actor_event_participation(
            self,
            actor_uri: URIRef,
            links_inverse: list[Link]) -> None:
        for link_ in links_inverse:
            code = link_.property.code
            domain = link_.domain
            if (code in ACTOR_EVENT_PROPERTIES
                    and domain.class_.name in EVENT_CLASS_MAP):
                fwd_prop, inv_prop = ACTOR_EVENT_PROPERTIES[code]
                event_data = (
                    self.event_links.get(domain.id)
                    or EntityLinks(entity=domain))
                event_uri = self._format_event(event_data)
                self.graph.add((event_uri, fwd_prop, actor_uri))
                self.graph.add((actor_uri, inv_prop, event_uri))

    def _format_person(self, data: EntityLinks) -> URIRef:
        entity = data.entity
        person_uri = self._add_base_entity(
            entity,
            CRM.E21_Person,
            data.links,
            data.links_inverse)

        for link_ in data.links:
            if link_.property.code == 'P2':
                self._add_person_type(person_uri, link_)

        self._add_person_life_events(entity, person_uri, data.links)

        for link_ in data.links_inverse:
            if (link_.property.code == 'P107'
                    and link_.domain.class_.name == 'group'):
                self._add_membership_events(link_, link_.domain, entity)

        self._add_actor_event_participation(person_uri, data.links_inverse)
        return person_uri

    def _add_person_type(self, person_uri: URIRef, link_: Link) -> None:
        if link_.description and is_float(link_.description):
            return
        type_entity = g.types.get(link_.range.id, link_.range)
        if _is_sex_type(type_entity):
            key = type_entity.name.strip().lower()
            gender_uri, en_label, de_label = GENDER_MAP.get(
                key,
                (PFPG.unknown, 'unknown', 'unbekannt'))
            self.graph.add((person_uri, CRM.P2_has_type, gender_uri))
            if (person_uri, PFP.has_gender, None) not in self.graph:
                self.graph.add((person_uri, PFP.has_gender, gender_uri))
            self.graph.add((gender_uri, RDF.type, PFPG.Gender_Type))
            self.graph.add((
                gender_uri,
                RDFS.label,
                Literal(en_label, lang='en')))
            self.graph.add((
                gender_uri,
                RDFS.label,
                Literal(de_label, lang='de')))
        else:
            pursuit_uri = URIRef(f'{person_uri}/profession/{link_.id}')
            self.graph.add((person_uri, PFP.has_profession, pursuit_uri))
            self.graph.add((pursuit_uri, RDF.type, FRBROO.F51_Pursuit))
            self.graph.add((
                pursuit_uri,
                RDFS.label,
                Literal(type_entity.name)))
            self.graph.add((pursuit_uri, CRM.P14_carried_out_by, person_uri))

    def _add_person_life_events(
            self,
            person: Entity,
            person_uri: URIRef,
            links: list[Link]) -> None:
        dates = person.dates
        self._add_life_event(
            person_uri,
            f'Birth of {person.name}',
            URIRef(f'{person_uri}/birth'),
            CRM.E67_Birth,
            CRM.P98i_was_born,
            CRM.P98_brought_into_life,
            _get_begin_bounds(dates),
            dates.begin_comment,
            next((l.range for l in links if l.property.code == 'OA8'), None))
        self._add_life_event(
            person_uri,
            f'Death of {person.name}',
            URIRef(f'{person_uri}/death'),
            CRM.E69_Death,
            CRM.P100i_died_in,
            CRM.P100_was_death_of,
            _get_end_bounds(dates),
            dates.end_comment,
            next((l.range for l in links if l.property.code == 'OA9'), None))

    def _add_life_event(  # pylint: disable=too-many-arguments,too-many-positional-arguments
            self,
            person_uri: URIRef,
            label: str,
            event_uri: URIRef,
            event_class: URIRef,
            person_to_event: URIRef,
            event_to_person: URIRef,
            bounds: tuple[str | None, str | None],
            comment: str | None,
            place: Entity | None) -> None:
        earliest, latest = bounds
        if not (earliest or comment or place):
            return
        self.graph.add((event_uri, RDF.type, event_class))
        self.graph.add((event_uri, RDFS.label, Literal(label)))
        self.graph.add((person_uri, person_to_event, event_uri))
        self.graph.add((event_uri, event_to_person, person_uri))
        if earliest or comment:
            ts_uri = self._add_timespan(
                URIRef(f'{event_uri}/timespan'),
                comment or f'Timespan of {label}',
                earliest,
                latest)
            self.graph.add((event_uri, CRM['P4_has_time-span'], ts_uri))
        if place:
            self.graph.add((
                event_uri,
                CRM.P7_took_place_at,
                self._ensure_place_ref(place)))

    def _format_group(self, data: EntityLinks) -> URIRef:
        entity = data.entity
        group_uri = self._add_base_entity(
            entity,
            CRM.E74_Group,
            data.links,
            data.links_inverse)
        for link_ in data.links:
            if (link_.property.code == 'P107'
                    and link_.range.class_.name == 'person'):
                self._add_membership_events(link_, entity, link_.range)
        self._add_actor_event_participation(group_uri, data.links_inverse)
        return group_uri

    def _add_membership_events(
            self,
            link_: Link,
            group: Entity,
            person: Entity) -> None:
        group_uri = self._add_base_entity(group, CRM.E74_Group)
        person_uri = self._add_base_entity(person, CRM.E21_Person)

        joining_uri = URIRef(f'{group_uri}/joining/{link_.id}')
        self.graph.add((joining_uri, RDF.type, CRM.E85_Joining))
        self.graph.add((
            joining_uri,
            RDFS.label,
            Literal(f'Joining of {person.name} in {group.name}')))
        self.graph.add((person_uri, CRM.P143i_was_joined_by, joining_uri))
        self.graph.add((joining_uri, CRM.P143_joined, person_uri))
        self.graph.add((group_uri, CRM.P144i_gained_member_by, joining_uri))

        if link_.type and (role_type := g.types.get(link_.type.id)):
            role_uri = self._ensure_type(role_type)
            pc144_uri = URIRef(f'{joining_uri}/pc144')
            self.graph.add((pc144_uri, RDF.type, CRM.PC144_joined_with))
            self.graph.add((joining_uri, CRM.P01i_is_domain_of, pc144_uri))
            self.graph.add((pc144_uri, CRM.P01_is_domain_of, joining_uri))
            self.graph.add((pc144_uri, CRM.P02_has_range, group_uri))
            self.graph.add((pc144_uri, CRM.P144_1_kind_of_member, role_uri))
        else:
            self.graph.add((joining_uri, CRM.P144_joined_with, group_uri))

        b_earliest, b_latest = _get_begin_bounds(link_.dates)
        if b_earliest or link_.dates.begin_comment:
            ts_uri = self._add_timespan(
                URIRef(f'{joining_uri}/timespan'),
                link_.dates.begin_comment
                or f'Timespan of Joining of {person.name} in {group.name}',
                b_earliest,
                b_latest)
            self.graph.add((joining_uri, CRM['P4_has_time-span'], ts_uri))

        e_earliest, e_latest = _get_end_bounds(link_.dates)
        if e_earliest or link_.dates.end_comment:
            self._add_leaving_event(
                link_,
                group,
                person,
                group_uri,
                person_uri,
                (e_earliest, e_latest))

    def _add_leaving_event(  # pylint: disable=too-many-arguments,too-many-positional-arguments
            self,
            link_: Link,
            group: Entity,
            person: Entity,
            group_uri: URIRef,
            person_uri: URIRef,
            bounds: tuple[str | None, str | None]) -> None:
        leaving_uri = URIRef(f'{group_uri}/leaving/{link_.id}')
        self.graph.add((leaving_uri, RDF.type, CRM.E86_Leaving))
        self.graph.add((
            leaving_uri,
            RDFS.label,
            Literal(f'Leaving of {person.name} from {group.name}')))
        self.graph.add(
            (person_uri, CRM.P145i_was_separated_by, leaving_uri))
        self.graph.add((leaving_uri, CRM.P145_separated, person_uri))
        self.graph.add((group_uri, CRM.P146i_lost_member_by, leaving_uri))
        self.graph.add((leaving_uri, CRM.P146_separated_from, group_uri))

        ts_uri = self._add_timespan(
            URIRef(f'{leaving_uri}/timespan'),
            link_.dates.end_comment
            or f'Timespan of Leaving of {person.name} from {group.name}',
            bounds[0],
            bounds[1])
        self.graph.add((leaving_uri, CRM['P4_has_time-span'], ts_uri))

    def _format_manifestation(self, data: EntityLinks) -> URIRef:
        entity = data.entity
        manif_uri = self._add_base_entity(
            entity,
            LRMOO.F3_Manifestation,
            data.links,
            data.links_inverse)

        creation_uri = URIRef(f'{manif_uri}/creation')
        self.graph.add(
            (creation_uri, RDF.type, LRMOO.F30_Manifestation_Creation))
        self.graph.add((
            creation_uri,
            RDFS.label,
            Literal(f'Creation of {entity.name}')))
        self.graph.add((creation_uri, LRMOO.R24_created, manif_uri))

        earliest, latest = _get_full_bounds(entity.dates)
        ts_uri = self._add_timespan(
            URIRef(f'{creation_uri}/timespan'),
            entity.dates.begin_comment
            or entity.dates.end_comment
            or f'Timespan of Creation of {entity.name}',
            earliest,
            latest)
        self.graph.add((creation_uri, CRM['P4_has_time-span'], ts_uri))

        for link_ in data.links:
            self._add_manifestation_link(creation_uri, link_)

        return manif_uri

    def _add_manifestation_link(
            self,
            creation_uri: URIRef,
            link_: Link) -> None:
        if (link_.property.code in ('P7', 'OA8', 'P67')
                and link_.range.class_.name in (
                    'place', 'object_location', 'administrative_unit')):
            place_uri = self._ensure_place_ref(link_.range)
            self.graph.add((creation_uri, CRM.P7_took_place_at, place_uri))
        elif (link_.property.code in ('P14', 'P67')
                and link_.range.class_.name in ('person', 'group')
                and link_.type
                and (role_type := g.types.get(link_.type.id))):
            actor_cls = (
                CRM.E21_Person
                if link_.range.class_.name == 'person'
                else CRM.E74_Group)
            actor_uri = self._add_base_entity(link_.range, actor_cls)
            role_uri = self._ensure_type(role_type)
            pc14_uri = URIRef(f'{creation_uri}/carried_out_by/{link_.id}')
            self.graph.add((pc14_uri, RDF.type, CRM.PC14_carried_out_by))
            self.graph.add((
                pc14_uri,
                RDFS.label,
                Literal(f'{link_.range.name} ({role_type.name})')))
            self.graph.add((creation_uri, CRM.P01i_is_domain_of, pc14_uri))
            self.graph.add((pc14_uri, CRM.P01_is_domain_of, creation_uri))
            self.graph.add((pc14_uri, CRM.P02_has_range, actor_uri))
            self.graph.add((
                pc14_uri,
                CRM['P14.1_in_the_role_of'],
                role_uri))


def _load_event_links_and_geometries(
        links_data: dict[int, EntityLinks]) \
        -> tuple[dict[int, EntityLinks], dict[int, str]]:
    referenced_events: dict[int, Entity] = {}
    for item in links_data.values():
        for link_ in item.links_inverse:
            if (link_.property.code in ACTOR_EVENT_PROPERTIES
                    and link_.domain.class_.name in EVENT_CLASS_MAP
                    and link_.domain.id not in links_data):
                referenced_events[link_.domain.id] = link_.domain

    event_links = dict(links_data)
    if referenced_events:
        event_links.update(
            get_links_for_entities(list(referenced_events.values())))

    extra_geom_ids: set[int] = set()
    for item in event_links.values():
        for link_ in item.links:
            if link_.property.code in (
                    'OA8', 'OA9', 'P7', 'P26', 'P27', 'P53'):
                extra_geom_ids.add(link_.range.id)

    geometries = (
        get_wkts_by_ids(list(extra_geom_ids)) if extra_geom_ids else {})
    return event_links, geometries


def get_pfp_export_graph(query: PfpExportQuery) -> Graph:
    type_ids = resolve_type_ids(query.type_id)
    case_study_ids = resolve_type_ids(query.case_study)
    if type_ids == [] or case_study_ids == []:
        return PfpFormatter().graph

    rows, _total = search_entities_api(
        PFP_CLASSES,
        order_by=f'{query.sort_by}_{query.sort}',
        limit=query.limit,
        offset=(query.page - 1) * query.limit,
        search_name=query.search,
        start_date=query.start_date,
        end_date=query.end_date,
        type_ids=type_ids,
        case_study_ids=case_study_ids)

    if not rows:
        return PfpFormatter().graph

    ids = [r['id'] for r in rows]
    entities_by_id = {
        e.id: e for e in Entity.get_by_ids(ids, types=True, aliases=True)}
    entities = [entities_by_id[id_] for id_ in ids if id_ in entities_by_id]

    links_data = get_links_for_entities(entities)
    event_links, geometries = _load_event_links_and_geometries(links_data)
    formatter = PfpFormatter(geometries=geometries, event_links=event_links)
    return formatter.format_entities(list(links_data.values()))
