import json
import os
from typing import List, Dict, Any

from flask import request, url_for

from openatlas import app
from openatlas.models.model import CidocClass
from openatlas.models.entity import Entity
from openatlas.models.geonames import Geonames
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.util.util import format_date, get_file_path


class Api:

    @staticmethod
    def to_camelcase(string: str) -> str:
        if not string:
            return ''
        words = string.split(' ')
        return words[0] + ''.join(x.title() for x in words[1:])

    @staticmethod
    def get_links(entity: Entity) -> List[Dict[str, str]]:
        links = []
        for link in Link.get_links(entity.id):
            links.append({'label': link.range.name,
                          'relationTo': url_for('api_entity', id_=link.range.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_'
                                          + link.property.i18n['en'].replace(' ', '_')}, )
            if link.property.code == 'P53':
                entity.location = link.range

        for link in Link.get_links(entity.id, inverse=True):
            links.append({'label': link.domain.name,
                          'relationTo': url_for('api_entity', id_=link.domain.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_'
                                          + link.property.i18n['en'].replace(' ', '_')}, )

        return links

    @staticmethod
    def get_file(entity: Entity) -> List[Dict[str, str]]:
        files = []
        for link in Link.get_links(entity.id, inverse=True):
            if link.domain.system_type == 'file':
                path = get_file_path(link.domain.id)
                filename = os.path.basename(path) if path else None
                files.append({'@id': url_for('api_entity', id_=link.domain.id, _external=True),
                              'title': link.domain.name,
                              'license': Api.get_license(link.domain.id) if Api.get_license(
                                  link.domain.id) else None,
                              'url': url_for('display_file', filename=filename,
                                             _external=True) if filename else None})
        return files

    @staticmethod
    def get_license(entity_id) -> List[Dict[str, str]]:
        file_license = ""
        for link in Link.get_links(entity_id):
            if link.property.code == "P2":
                file_license = link.range.name

        return file_license

    @staticmethod
    def get_entities_by_code(code_: str):
        entities = []
        for entity in Entity.get_by_codes(code_):
            entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entities_by_class(class_code_: str):
        entities = []
        for entity in Entity.get_by_class(class_code_):
            entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entities_get_latest(limit_: int):
        entities = []
        for entity in Entity.get_latest(limit_):
            entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entities_by_id(ids: list):
        entities = []
        for i in ids:
            for entity in Entity.get_by_ids(i, nodes=True):
                entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entity(id_: int) -> Dict[str, Any]:
        entity = Entity.get_by_id(id_, nodes=True, aliases=True)

        type_ = 'FeatureCollection'

        nodes = []
        for node in entity.nodes:
            nodes.append({'identifier': url_for('api_entity', id_=node.id, _external=True),
                          'label': node.name, 'description': node.description})
        geo = Geonames.get_geonames_link(entity)

        features = {'@id': url_for('entity_view', id_=entity.id, _external=True),
                    'type': 'Feature',
                    'crmClass': entity.class_.code,
                    'crmClassLabel': entity.class_.i18n['en'],
                    'properties': {'title': entity.name}}

        # Relations
        if Api.get_links(entity):
            features['relations'] = Api.get_links(entity)

        # Descriptions
        if entity.description:
            features['description'] = [{'@id': request.base_url, 'value': entity.description}]

        # Types
        if nodes:
            features['types'] = nodes

        if entity.aliases:
            features['names'] = []
            for key, value in entity.aliases.items():
                features['names'].append({"alias": value})

        # Todo: How to get into the if function? Why this method won't work?
        # Depictions
        if Api.get_file(entity):
            features['depictions'] = Api.get_file(entity)

        # Time spans
        if entity.begin_from or entity.begin_to or entity.end_from or entity.end_to:
            features['when'] = {'timespans': [{
                'start': {'earliest': format_date(entity.begin_from) if entity.begin_from else None,
                          'latest': format_date(entity.begin_to) if entity.begin_to else None,
                          'comment': entity.begin_comment if entity.begin_comment else None}
                if entity.begin_from or entity.begin_to else None,
                'end': {'earliest': format_date(entity.end_from) if entity.end_from else None,
                        'latest': format_date(entity.end_to) if entity.end_to else None,
                        'comment': entity.end_comment if entity.end_comment else None}
                if entity.end_from or entity.end_to else None}]}

        # Geonames
        if geo:
            link_type = Api.to_camelcase(geo.type.name)
            identifier = app.config['GEONAMES_VIEW_URL'] + geo.domain.name if geo else ''
            features['links'] = [{'type': link_type, 'identifier': identifier}]

        # Geometry
        try:
            geometries = []
            shape = {'linestring': 'LineString', 'polygon': 'Polygon', 'point': 'Point'}
            for geo in Gis.get_by_id(entity.location.id):
                geometries.append({'type': shape[geo['shape']],
                                   'coordinates': geo['geometry']['coordinates'],
                                   'classification': geo['type'],
                                   'description': geo['description'] if geo[
                                       'description'] else None,
                                   'title': geo['name'] if geo['description'] else None})

            if len(geometries) == 1:
                features['geometry'] = geometries[0]
            else:
                features['geometry'] = {'type': 'GeometryCollection', 'geometries': geometries}
        except (AttributeError, KeyError):
            features['geometry'] = {'type': 'GeometryCollection', 'geometries': []}

        data: dict = {'type': type_, '@context': app.config['API_SCHEMA'], 'features': [features]}

        return data
