from typing import Any, Dict, List, Optional, Union

from flask import g, url_for

from openatlas.api.v03.resources.util import get_license, to_camel_case
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.util import get_file_path


class LPHelper:
    @staticmethod
    def get_location_id(links: List[Link]) -> int:
                return [link_.range.id for link_ in
                        links if link_.property.code == 'P53'][0]

    @staticmethod
    def relation_type(link_: Link, inverse: bool = False) -> str:
        property_ = f"i {link_.property.i18n_inverse['en']}" \
            if inverse and link_.property.i18n_inverse['en'] \
            else f" {link_.property.i18n['en']}"
        return f"crm:{link_.property.code}{property_}"

    @staticmethod
    def link_dict(link_: Link, inverse: bool = False) -> Dict[str, Any]:
        return {
            'label': link_.domain.name if inverse else link_.range.name,
            'relationTo':
                url_for(
                    'api_03.entity',
                    id_=link_.domain.id if inverse else link_.range.id,
                    _external=True),
            'relationType': LPHelper.relation_type(link_, inverse),
            'relationSystemClass': link_.domain.class_.name
                if inverse else link_.range.class_.name,
            'type': to_camel_case(link_.type.name) if link_.type else None,
            'relationDescription': link_.description,
            'when': {'timespans': [
                LPHelper.get_time(link_.domain if inverse else link_.range)]}}

    @staticmethod
    def get_links(
            links: List[Link],
            links_inverse: List[Link]) -> Optional[List[Dict[str, str]]]:
        out = []
        for link_ in links:
            out.append(LPHelper.link_dict(link_))
        for link_ in links_inverse:
            out.append(LPHelper.link_dict(link_, inverse=True))
        return out if out else None

    @staticmethod
    def get_file(links_inverse: List[Link]) -> Optional[List[Dict[str, str]]]:
        files = []
        for link in links_inverse:
            if link.domain.class_.name != 'file':
                continue
            path = get_file_path(link.domain.id)
            files.append({
                '@id': url_for('api_03.entity', id_=link.domain.id,
                               _external=True),
                'title': link.domain.name,
                'license': get_license(link.domain),
                'url': url_for(
                    'api.display',
                    filename=path.name,
                    _external=True) if path else "N/A"})
        return files if files else None

    @staticmethod
    def get_node(entity: Entity,
                 links: List[Link]) -> Optional[List[Dict[str, Any]]]:
        nodes = []
        for node in entity.types:
            nodes_dict = {
                'identifier': url_for(
                    'api_03.entity',
                    id_=node.id,
                    _external=True),
                'label': node.name}
            for link in links:
                if link.range.id == node.id and link.description:
                    nodes_dict['value'] = link.description
                    if link.range.id == node.id and node.description:
                        nodes_dict['unit'] = node.description
            hierarchy = [g.types[root].name for root in node.root]
            nodes_dict['hierarchy'] = ' > '.join(map(str, hierarchy))
            nodes.append(nodes_dict)
        return nodes if nodes else None

    @staticmethod
    def get_time(entity: Union[Entity, Link]) -> Optional[Dict[str, Any]]:
        return {
            'start': {
                'earliest': str(entity.begin_from),
                'latest': str(entity.begin_to),
                'comment': entity.begin_comment},
            'end': {
                'earliest': str(entity.end_from),
                'latest': str(entity.end_to),
                'comment': entity.end_comment}}

    @staticmethod
    def get_geoms_by_entity(entity_id: int) -> Dict[str, Any]:
        geoms = Gis.get_by_id(entity_id)
        if len(geoms) == 1:
            return geoms[0]
        return {'type': 'GeometryCollection', 'geometries': geoms}

    @staticmethod
    def get_reference_systems(links_inverse: List[Link]) \
            -> Optional[List[Dict[str, Any]]]:
        ref = []
        for link_ in links_inverse:
            if not isinstance(link_.domain, ReferenceSystem):
                continue
            system = g.reference_systems[link_.domain.id]
            identifier = system.resolver_url if system.resolver_url else ''
            ref.append({
                'identifier': f"{identifier}{link_.description}",
                'type': to_camel_case(g.types[link_.type.id].name),
                'referenceSystem': system.name})
        return ref if ref else None
