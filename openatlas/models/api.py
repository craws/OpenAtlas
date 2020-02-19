import os
from typing import List, Dict, Any

from flask import request, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.geonames import Geonames
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.util.util import format_date, get_file_path


class Api:

    @staticmethod
    def get_links(entity: Entity) -> List[Dict[str, str]]:
        links = []
        for link in Link.get_links(entity.id):
            links.append({'label': link.range.name,
                          'relationTo': url_for('api_entity', id_=link.range.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_' + link.property.i18n['en'].replace(' ',
                                                                                                               '_')}, )
            if link.property.code == 'P53':
                entity.location = link.range

        for link in Link.get_links(entity.id, inverse=True):
            links.append({'label': link.domain.name,
                          'relationTo': url_for('api_entity', id_=link.domain.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_' + link.property.i18n['en'].replace(' ',
                                                                                                               '_')}, )

        return links

    @staticmethod
    def get_file(entity: Entity) -> List[Dict[str, str]]:
        files = []
        for link in Link.get_links(entity.id, inverse=True):
            if link.domain.system_type == 'file':
                path = get_file_path(link.domain.id)
                filename = os.path.basename(path) if path else False
                files.append({'@id': url_for('api_entity', id_=link.domain.id, _external=True),
                              'title': link.domain.name,
                              'license': Api.get_license(link.domain.id),
                              'url': url_for('display_file', filename=filename, _external=True) if filename else 'N/A'})
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
    def get_entities_by_id(ids: list):
        entities = []
        for i in ids:
            for entity in Entity.get_by_ids(i, nodes=True):
                entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entity(id_: int) -> Dict[str, Any]:
        entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        # Todo: find better vocabulary for types and shorten the dict
        possible_types: dict = {'E7': 'EventCollection',
                                'E8': 'EventCollection',
                                'E9': 'EventCollection',
                                'E18': 'FeatureCollection',
                                'E21': 'FindCollection',
                                'E21': 'ActorCollection',
                                'E22': 'FindCollection',
                                'E31': 'DocumentCollection',
                                'E33': 'SourceCollection',
                                'E40': 'ActorCollection',
                                'E53': 'PlaceCollection',
                                'E55': 'TypeCollection',
                                'E74': 'ActorCollection',
                                'E84': 'ObjectCollection'}

        type_ = 'unknown'
        for t in possible_types:
            if t == entity.class_.code:
                type_ = possible_types.get(t)

        nodes = []
        for node in entity.nodes:
            nodes.append({'identifier': url_for('api_entity', id_=node.id, _external=True),
                          'label': node.name})
        geo = Geonames.get_geonames_link(entity)

        features = {'@id': url_for('entity_view', id_=entity.id, _external=True),
                    'type': entity.class_.code,
                    'typeLabel': entity.class_.i18n['en'],
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

        # Todo: How to get into the if function? Why this method won't work?
        # Depictions
        if Api.get_file(entity):
            features['depictions'] = [Api.get_file(entity)]

        # Todo: Make it flexible
        # Timespans
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

        # Geometry and Geonames
        if type_ == 'FeatureCollection':
            if geo:
                link_type = geo.type.name if geo else ''
                identifier = app.config['GEONAMES_VIEW_URL'] + geo.domain.name if geo else ''
                features['links'] = [{'type': link_type, 'identifier': identifier}]

        if geo:
            geo_type = geo.type.name.split(' ')
            link_type = geo_type[0] + ''.join(x.title() for x in geo_type[1:]) if geo else ''
            identifier = app.config['GEONAMES_VIEW_URL'] + geo.domain.name if geo else ''
            features['links'] = [{'type': link_type, 'identifier': identifier}]

        if type_ == "FeatureCollection":
            if Gis.get_by_id(entity.location.id):
                geometries = []
                for geo in Gis.get_by_id(entity.location.id):
                    geometries.append({'type': geo['shape'],
                                       'coordinates': geo['geometry']['coordinates'],
                                       'classification': geo['type'],
                                       'description': geo['description'],
                                       'title': geo['name']})
                features['geometry'] = {'type': 'GeometryCollection', 'geometries': geometries}

        data: dict = {'type': type_, '@context': app.config['API_SCHEMA'], 'features': [features]}

        return data
