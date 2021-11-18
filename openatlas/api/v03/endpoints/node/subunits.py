from typing import Any, Dict, List, Optional, Tuple, Union

from flask import Response, g
from flask_restful import Resource

from openatlas.api.v03.resources.formats.linked_places import get_geometries
from openatlas.api.v03.resources.formats.linked_places_helper import \
    get_geoms_by_entity, get_reference_systems
from openatlas.api.v03.resources.parser import default
from openatlas.api.v03.resources.resolve_endpoints import resolve_subunit_parser
from openatlas.api.v03.resources.util import get_all_links, \
    get_all_links_inverse, get_entity_by_id, get_license
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.place import get_structure
from openatlas.util.util import get_file_path


class GetSubunits(Resource):  # type: ignore

    def get(self,
            id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_subunit_parser(
            GetSubunits.get_subunits(get_entity_by_id(id_)),
            default.parse_args(), id_)

    @staticmethod
    def get_subunits(entity: Entity) -> Dict[str, Any]:
        links = get_all_links([entity.id])
        links_inverse = get_all_links_inverse([entity.id])
        struct = get_structure(entity)
        return {
            'id': entity.id,
            'rootId': GetSubunits.get_root(struct),
            'parentId': GetSubunits.get_parent(struct),
            'openatlasClassName': entity.class_.name,
            'crmClass': entity.cidoc_class.code,
            'created': entity.created,
            'modified': entity.modified,
            'latestModRec': None,
            'geometry': get_geometries(entity, links),
            'children': GetSubunits.get_children(struct),
            'properties': GetSubunits.get_properties(entity, links,
                                                     links_inverse)
        }

    @staticmethod
    def get_children(struct: Dict[str, Any]) -> Optional[List[dict[str, Any]]]:
        if struct['subunits']:
            return [subunit.id for subunit in struct['subunits']]
        return None

    @staticmethod
    def get_root(struct: Dict[str, Any]) -> Optional[List[dict[str, Any]]]:
        if struct['place']:
            return struct['place'].id
        return None

    @staticmethod
    def get_stratigraphic_unit(struct: Dict[str, Any]) -> Optional[
        List[dict[str, Any]]]:
        return struct['stratigraphic_unit'].id if struct[
            'stratigraphic_unit'] else None

    @staticmethod
    def get_parent(struct: Dict[str, Any]) -> Optional[List[dict[str, Any]]]:
        if struct['stratigraphic_unit']:
            return struct['stratigraphic_unit'].id
        if struct['feature']:
            return struct['feature'].id
        if struct['place']:
            return struct['place'].id
        return None

    @staticmethod
    def get_properties(entity: Entity, links: List[Link],
                       links_inverse: List[Link]) -> Dict[str, Any]:
        return {
            'name': entity.name,
            'aliases': [value for value in entity.aliases.values()] if entity.aliases.values() else None,
            'description': entity.description,
            'standardType': entity.nodes.values(),
            'timespan': GetSubunits.get_timespans(entity),
            'externalReferences': get_reference_systems(links_inverse),
            'references': GetSubunits.get_references(links_inverse),
            'files': GetSubunits.get_file(links_inverse),
            'types': GetSubunits.get_types(entity, links),
        }

    @staticmethod
    def get_references(links: List[Link]):
        out = []
        for link_ in links:
            if link_.property.code == "P67" and link_.domain.class_.name in ['bibliography', 'edition', 'external_reference']:
                out.append({
                    'abbreviation': link_.domain.name,
                    'id': link_.domain.id,
                    'title': link_.domain.description,
                    'pages': link_.description})
        return out if out else None

    @staticmethod
    def get_timespans(entity: Entity) -> Dict[str, str]:
        return {
            'earliestBegin': str(entity.begin_from),
            'latestBegin': str(entity.begin_to),
            'earliestEnd': str(entity.end_from),
            'latestEnd': str(entity.end_to), }

    @staticmethod
    def get_file(links_inverse: List[Link]) -> Optional[List[Dict[str, str]]]:
        files = []
        for link in links_inverse:
            if link.domain.class_.name != 'file':
                continue
            path = get_file_path(link.domain.id)
            files.append({
                'id': link.domain.id,
                'name': link.domain.name,
                'fileName': path.name if path else None,
                'license': get_license(link.domain),
                'source': link.domain.description})
        return files if files else None

    @staticmethod
    def get_types(entity: Entity, links: List[Link]) -> List[Dict[str, Any]]:
        nodes = []
        for node in entity.nodes:
            nodes_dict = {
                'id': node.id,
                'name': node.name}
            for link in links:
                if link.range.id == node.id and link.description:
                    nodes_dict['value'] = link.description
                    if link.range.id == node.id and node.description:
                        nodes_dict['unit'] = node.description
            hierarchy = [g.nodes[root].name for root in node.root]
            hierarchy.reverse()
            nodes_dict['path'] = ' > '.join(map(str, hierarchy))
            nodes_dict['rootId'] = node.root[0]
            nodes.append(nodes_dict)
        return nodes if nodes else None
