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
                                          + link.property.i18n['en'].replace(' ', '_')})
            if link.property.code == 'P53':
                entity.location = link.range

        for link in Link.get_links(entity.id, inverse=True):
            links.append({'label': link.domain.name,
                          'relationTo': url_for('api_entity', id_=link.domain.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_'
                                          + link.property.i18n['en'].replace(' ', '_')})

        return links

    @staticmethod
    def get_file(entity: Entity) -> List[Dict[str, str]]:
        files = []
        for link in Link.get_links(entity.id, inverse=True):
            if link.domain.system_type == 'file':
                path = get_file_path(link.domain.id)
                #filename = os.path.basename(path)
                file_dict = {'@id': url_for('api_entity', id_=link.domain.id, _external=True),
                             'title': link.domain.name}
                if Api.get_license(link.domain.id):
                    file_dict['license'] = Api.get_license(link.domain.id)
                try:
                    filename = os.path.basename(path)
                    file_dict['url'] = url_for('display_file', filename=filename, external=True)
                except (TypeError):
                    pass
                files.append(file_dict)
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
        geo = Geonames.get_geonames_link(entity)
        type_ = 'FeatureCollection'
        nodes = []
        features = {'@id': url_for('entity_view', id_=entity.id, _external=True),
                    'type': 'Feature',
                    'crmClass': "".join(entity.class_.code + " "
                                        + entity.class_.i18n['en']).replace(" ", "_"),
                    'crmClassLabel': entity.class_.i18n['en'],
                    'properties': {'title': entity.name}}

        # Types
        for node in entity.nodes:
            nodes_dict = {'identifier': url_for('api_entity', id_=node.id, _external=True),
                          'label': node.name}

            for link in Link.get_links(entity.id):
                if link.range.id == node.id and link.description:
                    nodes_dict['value'] = link.description
                    if link.range.id == node.id and node.description:
                        nodes_dict['unit'] = node.description
            if 'unit' not in nodes_dict and node.description:
                nodes_dict['description'] = node.description
            nodes.append(nodes_dict)

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

        # Todo: This functions won't work on references! Need to change
        # Depictions
        if Api.get_file(entity):
            features['depictions'] = Api.get_file(entity)

        # Time spans
        if entity.begin_from or entity.end_from:
            features['when'] = {'timespans': []}
            if entity.begin_from:
                start = {'earliest': format_date(entity.begin_from)}
                if entity.begin_to:
                    start['latest'] = format_date(entity.begin_to)
                if entity.begin_comment:
                    start['comment'] = entity.begin_comment
            if entity.end_from:
                end = {'earliest': format_date(entity.end_from)}
                if entity.end_to:
                    end['latest'] = format_date(entity.end_to)
                if entity.end_comment:
                    end['comment'] = entity.end_comment

            if entity.begin_from and not entity.end_from:
                features['when']['timespans'].append({'start': start})
            elif not entity.begin_from and entity.end_from:
                features['when']['timespans'].append({'end': end})
            else:
                features['when']['timespans'].append({'start': start, 'end': end})

        # Geonames
        if geo:
            features['links'] = []
            geo_name = {}
            if geo.type.name:
                geo_name['type'] = Api.to_camelcase(geo.type.name)
            if geo.domain.name:
                geo_name['identifier'] = app.config['GEONAMES_VIEW_URL'] + geo.domain.name
            features['links'].append(geo_name)

        # Geometry
        try:
            geometries = []
            shape = {'linestring': 'LineString', 'polygon': 'Polygon', 'point': 'Point'}
            for geo in Gis.get_by_id(entity.location.id):
                geo_dict = {'type': shape[geo['shape']],
                            'coordinates': geo['geometry']['coordinates'],
                            'classification': geo['type']}
                if geo['description']:
                    geo_dict['description'] = geo['description']
                if geo['name']:
                    geo_dict['title'] = geo['name']
                geometries.append(geo_dict)

            if len(geometries) == 1:
                features['geometry'] = geometries[0]
            else:
                features['geometry'] = {'type': 'GeometryCollection', 'geometries': geometries}
        except (AttributeError, KeyError):
            features['geometry'] = {'type': 'GeometryCollection', 'geometries': []}

        data: dict = {'type': type_, '@context': app.config['API_SCHEMA'], 'features': [features]}

        return data
