from typing import Any

from flask import g
from fuzzywuzzy import fuzz

from openatlas.database import checks as db
from openatlas.database import date
from openatlas.models.entity import Entity


def check_single_type_duplicates() -> list[dict[str, Any]]:
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


def get_invalid_dates() -> list[Entity]:
    return [
        Entity.get_by_id(row['id'], types=True)
        for row in date.get_invalid_dates()]


def get_orphans() -> list[Entity]:
    return [Entity.get_by_id(row['id']) for row in db.get_orphans()]


def get_orphaned_subunits() -> list[Entity]:
    return [Entity.get_by_id(x['id']) for x in db.get_orphaned_subunits()]


def get_entities_linked_to_itself() -> list[Entity]:
    return [Entity.get_by_id(row['domain_id']) for row in db.get_circular()]


def get_invalid_cidoc_links() -> list[dict[str, Any]]:
    invalid_linking = []
    for row in db.get_cidoc_links():
        valid_domain = g.properties[row['property_code']].find_object(
            'domain_class_code',
            row['domain_code'])
        valid_range = g.properties[row['property_code']].find_object(
            'range_class_code',
            row['range_code'])
        if not valid_domain or not valid_range:
            invalid_linking.append(row)
    invalid_links = []
    for item in invalid_linking:
        for row in db.get_invalid_links(item):
            invalid_links.append({
                'domain': Entity.get_by_id(row['domain_id']),
                'property': g.properties[row['property_code']],
                'range': Entity.get_by_id(row['range_id'])})
    return invalid_links


def get_similar_named(class_: str, ratio: int) -> dict[int, Any]:
    similar: dict[int, Any] = {}
    already_added: set[int] = set()
    entities = Entity.get_by_class(class_)
    for sample in [e for e in entities if e.id not in already_added]:
        similar[sample.id] = {'entity': sample, 'entities': []}
        for e in entities:
            if e.id != sample.id and fuzz.ratio(sample.name, e.name) >= ratio:
                already_added.add(sample.id)
                already_added.add(e.id)
                similar[sample.id]['entities'].append(e)
    return {item: data for item, data in similar.items() if data['entities']}
