from typing import Any, Optional, Union

from flask import url_for

from openatlas import app
from openatlas.api.v02.resources.formats.linked_places_helper import LPHelper
from openatlas.models.entity import Entity
from openatlas.models.link import Link


class LinkedPlaces:

    @staticmethod
    def get_entity(entity: Entity,
                   links: list[Link],
                   links_inverse: list[Link],
                   parser: dict[str, Any]) -> dict[str, Any]:
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
            links: list[Link],
            links_inverse: list[Link],
            parser: dict[str, Any]) -> dict[str, Any]:
        return {'@id': url_for('view', id_=entity.id, _external=True),
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
    def get_description(entity: Entity) -> Optional[list[dict[str, Any]]]:
        return [{'value': entity.description}] if entity.description else None

    @staticmethod
    def get_relations(
            links: list[Link],
            links_inverse: list[Link],
            parser: dict[str, Any]) -> Optional[list[dict[str, str]]]:
        return LPHelper.get_links(links, links_inverse) \
            if 'relations' in parser['show'] else None

    @staticmethod
    def get_types(
            entity: Entity,
            links: list[Link],
            parser: dict[str, Any]) -> Optional[list[dict[str, Any]]]:
        return LPHelper.get_node(entity, links) \
            if 'types' in parser['show'] else None

    @staticmethod
    def get_depictions(
            links_inverse: list[Link],
            parser: dict[str, Any]) -> Optional[list[dict[str, str]]]:
        return LPHelper.get_file(links_inverse) \
            if 'depictions' in parser['show'] else None

    @staticmethod
    def get_timespans(
            entity: Entity,
            parser: dict[str, Any]) -> Optional[dict[str, Any]]:
        return {'timespans': [LPHelper.get_time(entity)]} \
            if 'when' in parser['show'] else None

    @staticmethod
    def get_reference_links(
            links_inverse: list[Link],
            parser: dict[str, Any]) -> Optional[list[dict[str, Any]]]:
        return LPHelper.get_reference_systems(links_inverse) \
            if 'links' in parser['show'] else None

    @staticmethod
    def get_geometries(
            entity: Entity,
            links: list[Link],
            parser: dict[str, Any]) -> Union[dict[str, Any], None]:
        if 'geometry' in parser['show']:
            if entity.class_.view == 'place' \
                    or entity.class_.name == 'artifact':
                return LPHelper.get_geoms_by_entity(
                    LPHelper.get_location_id(links))
            if entity.class_.name == 'object_location':
                return LPHelper.get_geoms_by_entity(entity.id)
        return None

    @staticmethod
    def get_names(
            entity: Entity,
            parser: dict[str, Any]) -> Optional[list[dict[str, Any]]]:
        return [{"alias": value} for value in entity.aliases.values()] \
            if entity.aliases and 'names' in parser['show'] else None

    @staticmethod
    def get_crm_class(entity: Entity) -> str:
        return f"crm:{entity.cidoc_class.code} {entity.cidoc_class.i18n['en']}"
