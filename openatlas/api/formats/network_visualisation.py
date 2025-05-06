from collections import defaultdict
from typing import Any

from flask import g

from openatlas.database import network as db
from openatlas.database.entity import get_linked_entities_recursive
from openatlas.api.endpoints.parser import Parser
from openatlas.api.resources.database_mapper import (
    get_all_links_for_network, get_ego_network_filtered_classes,
    get_links_by_id_network)


def overwrite_object_locations_with_place(
        links: list[dict[str, Any]],
        exclude_: list[str]) -> list[dict[str, Any]]:
    locations = {}
    for l in links:
        if l['property_code'] == 'P53':
            locations[l['range_id']] = {
                'range_id': l['domain_id'],
                'range_name': l['domain_name'],
                'range_system_class': l['domain_system_class']}

    copy = links.copy()
    for i, l in enumerate(copy):
        if l['range_id'] in locations:
            links[i].update(
                range_id=locations[l['range_id']]['range_id'],
                range_name=locations[l['range_id']]['range_name'],
                range_system_class=locations[
                    l['range_id']]['range_system_class'])
        if (l['domain_id'] in locations
                and "administrative_unit" not in exclude_):
            links[i].update(
                domain_id=locations[l['domain_id']]['range_id'],
                domain_name=locations[
                    l['domain_id']]['range_name'],
                domain_ystem_class=locations[
                    l['domain_id']]['range_system_class'])
    return links


def get_link_dictionary(links: list[dict[str, Any]]) -> dict[int, Any]:
    output: dict[int, Any] = defaultdict(set)
    for item in links:
        if output.get(item['domain_id']):
            output[item['domain_id']]['relations'].add(item['range_id'])
        else:
            output[item['domain_id']] = {
                'label': item['domain_name'],
                'systemClass': item['domain_system_class'],
                'relations': {item['range_id']}}
        if output.get(item['range_id']):
            output[item['range_id']]['relations'].add(item['domain_id'])
        else:
            output[item['range_id']] = {
                'label': item['range_name'],
                'systemClass': item['range_system_class'],
                'relations': {item['domain_id']}}
    return output


def get_excluded_classes(parser: Parser) -> list[str]:
    location_classes = [
        "administrative_unit",
        "artifact",
        "feature",
        "human_remains",
        "place",
        "stratigraphic_unit"]
    exclude = parser.exclude_system_classes or []
    if all(item in location_classes for item in exclude):
        exclude += ['object_location']
    return exclude


def get_network_visualisation(parser: Parser) -> dict[str, Any]:
    system_classes = g.classes
    exclude_ = get_excluded_classes(parser)
    if exclude_:
        system_classes = [s for s in system_classes if s not in exclude_]

    if linked_to_ids := parser.linked_to_ids:
        ids = []
        for id_ in linked_to_ids:
            ids += get_linked_entities_recursive(
                id_,
                list(g.properties),
                True)
            ids += get_linked_entities_recursive(
                id_,
                list(g.properties),
                False)
        all_ = get_links_by_id_network(ids + linked_to_ids)
        links = []
        if exclude_:
            for link_ in all_:
                if (link_['domain_system_class'] not in exclude_
                        or link_['range_system_class'] not in exclude_):
                    links.append(link_)
    else:
        links = get_all_links_for_network(system_classes)

    links = overwrite_object_locations_with_place(links, exclude_)
    link_dict = get_link_dictionary(links)

    results: dict[str, Any] = {'results': []}
    for id_, dict_ in link_dict.items():
        if linked_to_ids:
            if not set(linked_to_ids) & set(dict_['relations']):
                continue
        dict_['id'] = id_
        results['results'].append(dict_)

    return results


def get_ego_network_visualisation(id_: int, parser: Parser) -> dict[str, Any]:
    exclude_ = get_excluded_classes(parser)
    location_mapping = db.get_object_mapping()
    entity_ids = {id_}
    found_location_id = next(
        (key for key, value in location_mapping.items() if value == id_),
        None)
    if found_location_id is not None:
        entity_ids.add(found_location_id)
    all_ = []
    for _ in range(parser.depth):
        for row in get_ego_network_filtered_classes(entity_ids, exclude_):
            entity_ids.add(row['domain_id'])
            entity_ids.add(row['range_id'])
            all_.append(row)
    links = [dict(t) for t in {frozenset(d.items()) for d in all_}]
    links = overwrite_object_locations_with_place(links, exclude_)
    link_dict = get_link_dictionary(links)
    results: dict[str, Any] = {'results': []}
    for _id, dict_ in link_dict.items():
        if parser.linked_to_ids:
            if not set(parser.linked_to_ids) & set(dict_['relations']):
                continue
        dict_['id'] = _id
        results['results'].append(dict_)
    return results
