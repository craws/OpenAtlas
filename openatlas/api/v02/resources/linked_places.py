from typing import Any, Dict, List, Optional, Union

from flask import g, url_for

from openatlas import app
from openatlas.api.v02.resources.util import get_all_links, get_all_links_inverse, get_license
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.util import get_file_path


class LinkedPlaces:

    @staticmethod
    def get_all_links(entities: Union[int, List[int]]) -> List[Link]:
        links = []
        for link in Link.get_links(entities, list(g.properties)):
            links.append(link)
        return links

    @staticmethod
    def get_all_links_inverse(entities: Union[int, List[int]]) -> List[Link]:
        links_inverse = []
        for link in Link.get_links(entities, list(g.properties), inverse=True):
            links_inverse.append(link)
        return links_inverse

    @staticmethod
    def get_links(links: List[Link], links_inverse: List[Link]) -> Optional[List[Dict[str, str]]]:
        out = []
        for link in links:
            out.append({
                'label': link.range.name,
                'relationTo': url_for('api.entity', id_=link.range.id, _external=True),
                'relationType': 'crm:' + link.property.code + ' ' + link.property.i18n['en'],
                'relationSystemClass': link.range.class_.name,
                'type': link.type.name if link.type else None,
                'when': {'timespans': [LinkedPlaces.get_time(link.range)]}})
        for link in links_inverse:
            property_ = link.property.i18n['en']
            if link.property.i18n_inverse['en']:
                property_ = link.property.i18n_inverse['en']
            out.append({
                'label': link.domain.name,
                'relationTo': url_for('api.entity', id_=link.domain.id, _external=True),
                'relationType': 'crm:' + link.property.code + 'i ' + property_,
                'relationSystemClass': link.domain.class_.name,
                'type': link.type.name if link.type else None,
                'when': {'timespans': [LinkedPlaces.get_time(link.domain)]}})
        return out if out else None

    @staticmethod
    def get_file(links_inverse: List[Link]) -> Optional[List[Dict[str, str]]]:
        files = []
        for link in links_inverse:
            if link.domain.class_.name != 'file':
                continue
            path = get_file_path(link.domain.id)
            files.append({
                '@id': url_for('api.entity', id_=link.domain.id, _external=True),
                'title': link.domain.name,
                'license': get_license(link.domain),
                'url': url_for(
                    'api.display', filename=path.name, _external=True) if path else "N/A"})
        return files if files else None

    @staticmethod
    def get_node(entity: Entity, links: List[Link]) -> Optional[List[Dict[str, Any]]]:
        nodes = []
        for node in entity.nodes:
            nodes_dict = {
                'identifier': url_for('api.entity', id_=node.id, _external=True),
                'label': node.name}
            for link in links:
                if link.range.id == node.id and link.description:
                    nodes_dict['value'] = link.description
                    if link.range.id == node.id and node.description:
                        nodes_dict['unit'] = node.description
            hierarchy = [g.nodes[root].name for root in node.root]
            hierarchy.reverse()
            nodes_dict['hierarchy'] = ' > '.join(map(str, hierarchy))
            nodes.append(nodes_dict)
        return nodes if nodes else None

    @staticmethod
    def get_time(entity: Union[Entity, Link]) -> Optional[Dict[str, Any]]:
        return {
            'start': {
                'earliest': entity.begin_from,
                'latest': entity.begin_to,
                'comment': entity.begin_comment},
            'end': {
                'earliest': entity.end_from,
                'latest': entity.end_to,
                'comment': entity.end_comment}}

    @staticmethod
    def get_geoms_by_entity(entity: Entity) -> Union[str, Dict[str, Any]]:
        geoms = Gis.get_by_id(entity.id)
        if len(geoms) == 1:
            return geoms[0]
        return {'type': 'GeometryCollection', 'geometries': geoms}

    @staticmethod
    def get_reference_systems(links_inverse: List[Link]) -> Optional[List[Dict[str, Any]]]:
        ref = []
        for link_ in links_inverse:
            if not isinstance(link_.domain, ReferenceSystem):
                continue
            system = g.reference_systems[link_.domain.id]
            ref.append({
                'identifier':
                    (system.resolver_url if system.resolver_url else '') + link_.description,
                'type': g.nodes[link_.type.id].name,
                'referenceSystem': system.name})
        return ref if ref else None

    @staticmethod
    def get_entity(entity: Entity, links: List[Link], links_inverse: List[Link],
                   parser: Dict[str, Any]) -> Dict[str, Any]:
        type_ = 'FeatureCollection'
        class_code = ''.join(entity.cidoc_class.code + " " + entity.cidoc_class.i18n['en'])
        features = {
            '@id': url_for('entity_view', id_=entity.id, _external=True),
            'type': 'Feature',
            'crmClass': "crm:" + class_code,
            'systemClass': entity.class_.name,
            'properties': {'title': entity.name}}
        if entity.description:
            features['description'] = [{'value': entity.description}]
        if entity.aliases and 'names' in parser['show']:
            features['names'] = []
            for key, value in entity.aliases.items():
                features['names'].append({"alias": value})

        features['relations'] = \
            LinkedPlaces.get_links(links, links_inverse) if 'relations' in parser['show'] else None
        features['types'] = \
            LinkedPlaces.get_node(entity, links) if 'types' in parser['show'] else None
        features['depictions'] = \
            LinkedPlaces.get_file(links_inverse) if 'depictions' in parser['show'] else None
        features['when'] = {
            'timespans': [LinkedPlaces.get_time(entity)]} if 'when' in parser['show'] else None
        features['links'] = \
            LinkedPlaces.get_reference_systems(links_inverse) if 'links' in parser['show'] else None

        if 'geometry' in parser['show']:
            if entity.class_.view == 'place' or entity.class_.name in ['find', 'artifact']:
                features['geometry'] = LinkedPlaces.get_geoms_by_entity(
                    Link.get_linked_entity(entity.id, 'P53'))
            elif entity.class_.name == 'object_location':
                features['geometry'] = LinkedPlaces.get_geoms_by_entity(entity)

        return {
            'type': type_,
            '@context': app.config['API_SCHEMA'],
            'features': [features]}
