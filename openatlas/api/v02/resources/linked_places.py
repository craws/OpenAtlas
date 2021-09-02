from typing import Any, Dict, List, Optional, Union

from flask import url_for

from openatlas import app
from openatlas.api.v02.resources.linked_places_helper import LPHelper
from openatlas.models.entity import Entity
from openatlas.models.link import Link


class LinkedPlaces:

    @staticmethod
    def get_entity(entity: Entity,
                   links: List[Link],
                   links_inverse: List[Link],
                   parser: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'FeatureCollection',
            '@context': app.config['API_SCHEMA'],
            'features': [LinkedPlaces.build_feature(
                entity,
                links,
                links_inverse,
                parser)]}

    @staticmethod
    def build_feature(
            entity: Entity,
            links: List[Link],
            links_inverse: List[Link],
            parser: Dict[str, Any]) -> Dict[str, Any]:
        return {'@id': url_for('entity_view', id_=entity.id, _external=True),
                'type': 'Feature',
                'crmClass': LinkedPlaces.get_crm_class(entity),
                'systemClass': entity.class_.name,
                'properties': {'title': entity.name},
                'types': LinkedPlaces.get_types(entity, links, parser),
                'depictions':
                    LinkedPlaces.get_depictions(links_inverse, parser),
                'when': LinkedPlaces.get_timespans(entity, parser),
                'links':
                    LinkedPlaces.get_reference_links(links_inverse, parser),
                'description': LinkedPlaces.get_description(entity),
                'names': LinkedPlaces.get_names(entity, parser),
                'geometry': LinkedPlaces.get_geometries(entity, links, parser),
                'relations':
                    LinkedPlaces.get_relations(links, links_inverse, parser)}

    @staticmethod
    def get_description(entity: Entity) -> Optional[List[Dict[str, Any]]]:
        return [{'value': entity.description}] if entity.description else None

    @staticmethod
    def get_relations(
            links: List[Link],
            links_inverse: List[Link],
            parser: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
        return LPHelper.get_links(links, links_inverse) \
            if 'relations' in parser['show'] else None

    @staticmethod
    def get_types(
            entity: Entity,
            links: List[Link],
            parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        return LPHelper.get_node(entity, links) \
            if 'types' in parser['show'] else None

    @staticmethod
    def get_depictions(
            links_inverse: List[Link],
            parser: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
        return LPHelper.get_file(links_inverse) \
            if 'depictions' in parser['show'] else None

    @staticmethod
    def get_timespans(
            entity: Entity,
            parser: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {'timespans': [LPHelper.get_time(entity)]} \
            if 'when' in parser['show'] else None

    @staticmethod
    def get_reference_links(
            links_inverse: List[Link],
            parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        return LPHelper.get_reference_systems(links_inverse) \
            if 'links' in parser['show'] else None

    @staticmethod
    def get_geometries(
            entity: Entity,
            links: List[Link],
            parser: Dict[str, Any]) -> Union[Dict[str, Any], None]:
        if 'geometry' in parser['show']:
            if entity.class_.view == 'place' \
                    or entity.class_.name in ['find', 'artifact']:
                return LPHelper.get_geoms_by_entity(
                    LPHelper.get_location_id(links))
            if entity.class_.name == 'object_location':
                return LPHelper.get_geoms_by_entity(entity.id)
        return None

    @staticmethod
    def get_names(
            entity: Entity,
            parser: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        return [{"alias": value} for value in entity.aliases.values()] \
            if entity.aliases and 'names' in parser['show'] else None

    @staticmethod
    def get_crm_class(entity: Entity) -> str:
        return f"crm:{entity.cidoc_class.code} {entity.cidoc_class.i18n['en']}"
