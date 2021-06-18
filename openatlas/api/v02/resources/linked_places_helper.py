from typing import Any, Dict, List, Optional, Union

from flask import g, url_for

from openatlas.api.v02.resources.util import get_license
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.util import get_file_path


class LPHelper:
    @staticmethod
    def get_location_id(links: List[Link]) -> int:
        for link_ in links:
            if link_.property.code == 'P53':
                return link_.range.id

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
                'when': {'timespans': [LPHelper.get_time(link.range)]}})
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
                'when': {'timespans': [LPHelper.get_time(link.domain)]}})
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
    def get_geoms_by_entity(entity_id: int) -> Union[str, Dict[str, Any]]:
        geoms = Gis.get_by_id(entity_id)
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
