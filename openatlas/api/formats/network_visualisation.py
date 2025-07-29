from collections import defaultdict
from typing import Any

from flask import g

from openatlas import app
from openatlas.api.endpoints.parser import Parser
from openatlas.api.resources.database_mapper import (
    get_all_links_for_network, get_links_by_id_network,
    get_place_linked_to_location_id, get_types_linked_to_network_ids)


def overwrite_object_locations_with_place(
        links: list[dict[str, Any]],
        exclude_: set[str]) -> list[dict[str, Any]]:
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


def get_excluded_classes(parser: Parser) -> set[str]:
    location_classes = {
        "administrative_unit",
        "artifact",
        "feature",
        "human_remains",
        "place",
        "stratigraphic_unit"}
    exclude = set(parser.exclude_system_classes or [])
    if all(item in location_classes for item in exclude):
        exclude.add('object_location')
    return exclude


def get_network_visualisation(parser: Parser) -> dict[str, Any]:
    exclude_classes = get_excluded_classes(parser)
    included_classes = [
        cls for cls in g.classes if cls not in exclude_classes]

    links = get_all_links_for_network(included_classes)
    links = overwrite_object_locations_with_place(links, exclude_classes)

    entity_ids = set()
    filtered_links = []
    for link in links:
        classes = {
            link['domain_system_class'],
            link['range_system_class']}
        if classes.isdisjoint(exclude_classes):
            entity_ids.add(link['domain_id'])
            entity_ids.add(link['range_id'])
            filtered_links.append(link)
    links = filtered_links

    if parser.linked_to_ids:
        linked_to_ids = set(parser.linked_to_ids)
        valid_type_links = get_types_linked_to_network_ids(
            entity_ids,
            linked_to_ids)
        filtered_links = []
        for link in links:
            if {link['domain_id'], link['range_id']} & valid_type_links:
                filtered_links.append(link)
        links = filtered_links

    results: dict[str, Any] = {'results': []}
    for node_id, node_data in get_link_dictionary(links).items():
        node_data['id'] = node_id
        results['results'].append(node_data)
    return results


def get_ego_network_visualisation(id_: int, parser: Parser) -> dict[str, Any]:
    entity_ids = {id_}
    all_links = []
    previous_link_count = 0

    for _ in range(parser.depth):
        links = get_links_by_id_network(entity_ids)

        # Stop early if no new links were added
        if len(links) == previous_link_count:
            break
        previous_link_count = len(links)

        # Add place links for location-related properties
        location_ids = []
        for link in links:
            if link['property_code'] in app.config['LOCATION_PROPERTIES']:
                location_ids.append(link['range_id'])
        if location_ids:
            location_links = get_place_linked_to_location_id(location_ids)
            links.extend(location_links)

        for link in links:
            entity_ids.add(link['domain_id'])
            entity_ids.add(link['range_id'])
            all_links.append(link)

    exclude_classes = set(parser.exclude_system_classes or [])
    all_links = overwrite_object_locations_with_place(
        all_links,
        exclude_classes)

    filtered_links = []
    for link in all_links:
        link_classes = {
            link['domain_system_class'],
            link['range_system_class']}
        if link_classes.isdisjoint(exclude_classes):
            filtered_links.append(link)
    all_links = filtered_links

    if parser.linked_to_ids:
        linked_to_ids = set(parser.linked_to_ids)
        valid_type_links = get_types_linked_to_network_ids(
            entity_ids,
            linked_to_ids)

        filtered_links = []
        for link in all_links:
            link_ids = {link['domain_id'], link['range_id']}
            if link_ids.issubset(valid_type_links):
                filtered_links.append(link)
        all_links = filtered_links

    results: dict[str, Any] = {'results': []}
    for node_id, node_data in get_link_dictionary(all_links).items():
        node_data['id'] = node_id
        results['results'].append(node_data)
    return results
