from typing import Any

from flask import g
from rapidfuzz import fuzz

from openatlas.database import checks as db, date
from openatlas.models.entity import Entity, Link


def single_type_duplicates() -> list[dict[str, Any]]:
    data = []
    for type_ in g.types.values():
        if type_.multiple or type_.category in ['value', 'tools']:
            continue
        if type_ids := type_.get_sub_ids_recursive():
            for id_ in db.check_single_type_duplicates(type_ids):
                offending_types = []
                entity = Entity.get_by_id(id_, types=True)
                for entity_type in entity.types:
                    if g.types[entity_type.root[0]].id == type_.id:
                        offending_types.append(entity_type)
                if offending_types:
                    data.append({
                        'entity': entity,
                        'type': type_,
                        'offending_types': offending_types})
    return data


def invalid_dates() -> list[Entity]:
    return [Entity.get_by_id(row['id'], True) for row in date.invalid_dates()]


def orphans() -> list[Entity]:
    return [
        Entity.get_by_id(row['id'], types=True) for row in db.get_orphans()]


def orphaned_subunits() -> list[Entity]:
    return [Entity.get_by_id(x['id']) for x in db.get_orphaned_subunits()]


def entities_linked_to_itself() -> list[Link]:
    return [Link.get_by_id(id_) for id_ in db.get_circular()]


def invalid_cidoc_links() -> list[Link]:
    links = []
    for row in db.get_cidoc_links():
        if not link_is_valid(row['domain'], row['property'], row['range']):
            links.append(row['id'])
    return [Link.get_by_id(id_) for id_ in links]


def link_is_valid(domain: str, property_: str, range_: str) -> bool:
    valid_domain = g.properties[property_].find_object(
        'domain_class_code',
        domain) or (
            domain in g.cidoc_class_includes and
            g.properties[property_].find_object(
                'domain_class_code',
                g.cidoc_class_includes[domain]))
    valid_range = g.properties[property_].find_object(
        'range_class_code',
        range_) or (
            range_ in g.cidoc_class_includes and
            g.properties[property_].find_object(
                'range_class_code',
                g.cidoc_class_includes[range_]))
    return valid_domain and valid_range


def similar_named(class_: str, ratio: int) -> dict[int, Any]:
    similar: dict[int, Any] = {}
    already_added: set[int] = set()
    entities = Entity.get_by_class(class_)
    for sample in entities:
        if sample.id in already_added:
            continue
        already_added.add(sample.id)
        similar[sample.id] = {'entity': sample, 'entities': []}
        for e in entities:
            if e.id != sample.id and fuzz.ratio(sample.name, e.name) >= ratio:
                already_added.add(e.id)
                similar[sample.id]['entities'].append(e)
    return {item: data for item, data in similar.items() if data['entities']}


def link_duplicates() -> list[dict[str, Any]]:
    return db.link_duplicates()


def delete_link_duplicates() -> int:
    return db.delete_link_duplicates()


def invalid_involvement_dates() -> list[Link]:
    return [
        Link.get_by_id(row['id'])
        for row in date.invalid_involvement_dates()]


def invalid_preceding_dates() -> list[Link]:
    return [
        Link.get_by_id(row['id'])
        for row in date.invalid_preceding_dates()]


def invalid_sub_dates() -> list[Link]:
    return [Link.get_by_id(row['id']) for row in date.invalid_sub_dates()]


def get_invalid_link_dates() -> list[Link]:
    return [Link.get_by_id(row['id']) for row in date.invalid_link_dates()]


def type_orphans() -> list[Entity]:
    return [
        node for node in g.types.values()
        if node.root
        and node.category not in ['system', 'tools']
        and node.count < 1
        and not node.subs]
