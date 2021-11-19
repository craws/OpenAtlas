from datetime import datetime
from typing import Any, Dict, List, Optional

from flask import g

from openatlas.api.v03.resources.formats.linked_places import get_geometries
from openatlas.api.v03.resources.formats.linked_places_helper import \
    get_reference_systems
from openatlas.api.v03.resources.util import get_license
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.place import get_structure
from openatlas.util.util import get_file_path


def get_subunits(
        entity: Entity,
        links: List[Link],
        links_inverse: List[Link],
        latest_mod_rec: datetime) -> Dict[str, Any]:
    struct = get_structure(entity)
    return {
        'id': entity.id,
        'rootId': get_root(struct),
        'parentId': get_parent(struct),
        'openatlasClassName': entity.class_.name,
        'crmClass': entity.cidoc_class.code,
        'created': str(entity.created),
        'modified': str(entity.modified),
        'latestModRec': latest_mod_rec,
        'geometry': get_geometries(entity, links),
        'children': get_children(struct),
        'properties': get_properties(entity, links, links_inverse)}


def get_children(struct: Dict[str, Any]) -> Optional[List[dict[str, Any]]]:
    if struct['subunits']:
        return [subunit.id for subunit in struct['subunits']]
    return None


def get_root(struct: Dict[str, Any]) -> Optional[List[dict[str, Any]]]:
    if struct['place']:
        return struct['place'].id
    return None


def get_stratigraphic_unit(
        struct: Dict[str, Any]) -> Optional[List[dict[str, Any]]]:
    return struct['stratigraphic_unit'].id if struct[
        'stratigraphic_unit'] else None


def get_parent(struct: Dict[str, Any]) -> Optional[List[dict[str, Any]]]:
    if struct['stratigraphic_unit']:
        return struct['stratigraphic_unit'].id
    if struct['feature']:
        return struct['feature'].id
    if struct['place']:
        return struct['place'].id
    return None


def get_properties(
        entity: Entity,
        links: List[Link],
        links_inverse: List[Link]) -> Dict[str, Any]:
    return {
        'name': entity.name,
        'aliases': [value for value in
                    entity.aliases.values()] if entity.aliases.values() else None,
        'description': entity.description,
        'standardType': None,
        'timespan': get_timespans(entity),
        'externalReferences': get_reference_systems(links_inverse),
        'references': get_references(links_inverse),
        'files': get_file(links_inverse),
        'types': get_types(entity, links)}


def get_references(links: List[Link]):
    out = []
    for link_ in links:
        if link_.property.code == "P67" and link_.domain.class_.name in [
                'bibliography', 'edition', 'external_reference']:
            out.append({
                'abbreviation': link_.domain.name,
                'id': link_.domain.id,
                'title': link_.domain.description,
                'pages': link_.description if link_.description else None})
    return out if out else None


def get_timespans(entity: Entity) -> Dict[str, str]:
    return {
        'earliestBegin': str(entity.begin_from) if entity.begin_from else None,
        'latestBegin': str(entity.begin_to) if entity.begin_to else None,
        'earliestEnd': str(entity.end_from) if entity.end_from else None,
        'latestEnd': str(entity.end_to) if entity.end_to else None}


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
            'source': link.domain.description if link.domain.description else None})
    return files if files else None


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
