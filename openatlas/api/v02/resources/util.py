from typing import Any, Dict, List, Optional, Union

from flask import g

from openatlas.api.v02.resources.error import EntityDoesNotExistError
from openatlas.api.v02.templates.geojson import GeojsonTemplate
from openatlas.api.v02.templates.linked_places import LinkedPlacesTemplate
from openatlas.models.entity import Entity
from openatlas.models.link import Link


def get_entity_by_id(id_: int) -> Entity:
    try:
        entity = Entity.get_by_id(id_, nodes=True, aliases=True)
    except Exception:
        raise EntityDoesNotExistError
    return entity


def get_all_links(entities: Union[int, List[int]]) -> List[Link]:
    links = []
    for link in Link.get_links(entities, list(g.properties)):
        links.append(link)
    return links


def get_all_links_inverse(entities: Union[int, List[int]]) -> List[Link]:
    links_inverse = []
    for link in Link.get_links(entities, list(g.properties), inverse=True):
        links_inverse.append(link)
    return links_inverse


def get_license(entity: Entity) -> Optional[str]:
    file_license = None
    for node in entity.nodes:
        if g.nodes[node.root[-1]].name == 'License':
            file_license = node.name
    return file_license


def get_template(parser: Dict[str, str]) -> Dict[str, List]:
    if parser['format'] == 'lp':
        return LinkedPlacesTemplate.pagination(parser['show'])
    if parser['format'] == 'geojson':
        return GeojsonTemplate.geojson_template()
