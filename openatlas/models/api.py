import os
from typing import Any, Dict, List

from flask import g, session, url_for

from openatlas import app
from openatlas.models.api_error import APIError
from openatlas.models.entity import Entity
from openatlas.models.geonames import Geonames
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.util.util import format_date, get_file_path


class Api:
    # Todo: unit tests and Mypy checks

    @staticmethod
    def to_camelcase(string: str) -> str:  # pragma: nocover
        if not string:
            return ''
        words = string.split(' ')
        return words[0] + ''.join(x.title() for x in words[1:])

    @staticmethod
    def get_links(entity: Entity) -> List[Dict[str, str]]:
        links = []


        for link in Link.get_links(entity.id):  # pragma: nocover
            links.append({'label': link.range.name,
                          'relationTo': url_for('api_entity', id_=link.range.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_'
                                          + link.property.i18n['en'].replace(' ', '_')})
            if link.property.code == 'P53':
                entity.location = link.range

        for link in Link.get_links(entity.id, inverse=True):  # pragma: nocover
            links.append({'label': link.domain.name,
                          'relationTo': url_for('api_entity', id_=link.domain.id, _external=True),
                          'relationType': 'crm:' + link.property.code + 'i_'
                                          + link.property.i18n['en'].replace(' ', '_')})
        #  Todo: If we get to the location node or to the p2 node, it won't work. Make an if statment to controll this.
        #  Sample Id: 105 for location and 63 for p2
        for node in entity.nodes:
            for root in node.root:
                if not any(d.get('relationTo', None) == url_for('api_entity', id_=g.nodes[root].id,
                                                        _external=True) for d in links): # pragma: nocover
                    links.append({'label': g.nodes[root].name,
                                  'relationTo': url_for('api_entity', id_=g.nodes[root].id,
                                                        _external=True),
                                  'relationType': 'crm:' + g.properties['P2'].code + '_' +
                                              g.properties['P2'].i18n['en'].replace(' ', '_'),
                                  'test': "TEST"})

        for place in entity.location.nodes:
            if not any(d.get('relationTo', None) == url_for('api_entity', id_=place.id, _external=True) for d in links): # pragma: nocover
                links.append({'label': place.name,
                              'relationTo': url_for('api_entity', id_=place.id, _external=True),
                              'relationType': 'crm:' + g.properties['P89'].code + '_' +
                                              g.properties['P89'].i18n['en'].replace(' ', '_'),
                                  'test': "places"})
        return links

    @staticmethod
    def get_file(entity: Entity) -> List[Dict[str, str]]:
        files = []
        for link in Link.get_links(entity.id, inverse=True):  # pragma: nocover
            if link.domain.system_type == 'file':
                path = get_file_path(link.domain.id)
                file_dict = {'@id': url_for('api_entity', id_=link.domain.id, _external=True),
                             'title': link.domain.name}
                if Api.get_license(link.domain.id):
                    file_dict['license'] = Api.get_license(link.domain.id)
                try:
                    file_dict['url'] = url_for('display_file', filename=os.path.basename(path),
                                               _external=True)
                except TypeError:
                    pass
                files.append(file_dict)
        return files

    @staticmethod
    def get_license(entity_id: int) -> str:  # pragma: nocover
        file_license = ""
        for link in Link.get_links(entity_id):
            if link.property.code == "P2":
                file_license = link.range.name

        return file_license

    @staticmethod
    def get_entities_by_menu_item(code_: str) -> List[Dict[str, Any]]:
        entities = []
        for entity in Entity.get_by_menu_item(code_):
            entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entities_by_class(class_code_: str) -> List[Dict[str, Any]]:
        entities = []
        for entity in Entity.get_by_class_code(class_code_):
            entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entities_get_latest(limit_: int) -> List[Dict[str, Any]]:
        entities = []
        for entity in Entity.get_latest(limit_):
            entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entities_by_id(ids: List[int]) -> List[Dict[str, Any]]:  # pragma: nocover
        entities = []
        for i in ids:
            for entity in Entity.get_by_ids(i, nodes=True):
                entities.append(Api.get_entity(entity.id))
        return entities

    @staticmethod
    def get_entity(id_: int) -> Dict[str, Any]:
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise APIError('Entity ID doesn\'t exist!', status_code="404a")

        geonames_link = Geonames.get_geonames_link(entity)
        type_ = 'FeatureCollection'
        nodes = []
        class_code = ''.join(entity.class_.code + " " + entity.class_.i18n['en']).replace(" ", "_")
        features = {'@id': url_for('entity_view', id_=entity.id, _external=True),
                    'type': 'Feature',
                    'crmClass': "crm:" + class_code,
                    'properties': {'title': entity.name}}

        # Types
        for node in entity.nodes:
            nodes_dict = {'identifier': url_for('api_entity', id_=node.id, _external=True),
                          'label': node.name}
            for link in Link.get_links(entity.id):
                if link.range.id == node.id and link.description:  # pragma: nocover
                    nodes_dict['value'] = link.description
                    if link.range.id == node.id and node.description:
                        nodes_dict['unit'] = node.description
            if 'unit' not in nodes_dict and node.description:
                nodes_dict['description'] = node.description

            #  This feature is solely for Stefan
            hierarchy = []
            for root in node.root:
                hierarchy.append(g.nodes[root].name)  # pragma: nocover
            hierarchy.reverse()
            nodes_dict['hierarchy'] = ' > '.join(map(str, hierarchy))

            nodes.append(nodes_dict)

        # Relations
        if Api.get_links(entity):
            features['relations'] = Api.get_links(entity)

        # Descriptions
        if entity.description:
            features['description'] = [{'value': entity.description}]

        # Types
        if nodes:  # pragma: nocover
            features['types'] = nodes

        if entity.aliases:  # pragma: nocover
            features['names'] = []
            for key, value in entity.aliases.items():
                features['names'].append({"alias": value})

        # Depictions
        if Api.get_file(entity):  # pragma: nocover
            features['depictions'] = Api.get_file(entity)

        # Time spans
        if entity.begin_from or entity.end_from:  # pragma: nocover
            time = {}
            if entity.begin_from:
                start = {'earliest': format_date(entity.begin_from)}
                if entity.begin_to:
                    start['latest'] = format_date(entity.begin_to)
                if entity.begin_comment:
                    start['comment'] = entity.begin_comment
                time['start'] = start
            if entity.end_from:
                end = {'earliest': format_date(entity.end_from)}
                if entity.end_to:
                    end['latest'] = format_date(entity.end_to)
                if entity.end_comment:
                    end['comment'] = entity.end_comment
                time['end'] = end
            features['when'] = {'timespans': [time]}

        # Geonames
        if geonames_link and geonames_link.range.class_.code == 'E18':
            geo_name = {}
            if geonames_link.type.name:
                geo_name['type'] = Api.to_camelcase(geonames_link.type.name)
            if geonames_link.domain.name:
                geo_name['identifier'] = session['settings']['geonames_url'] + \
                                         geonames_link.domain.name
            if geonames_link.type.name or geonames_link.domain.name:
                features['links'] = []
                features['links'].append(geo_name)

        # Geometry
        try:
            geometries = []
            shape = {'linestring': 'LineString', 'polygon': 'Polygon', 'point': 'Point'}
            for geonames_link in Gis.get_by_id(entity.location.id):
                geo_dict = {'type': shape[geonames_link['shape']],
                            'coordinates': geonames_link['geometry']['coordinates']}
                if geonames_link['description']:
                    geo_dict['description'] = geonames_link['description']  # pragma: nocover
                if geonames_link['name']:
                    geo_dict['title'] = geonames_link['name']
                geometries.append(geo_dict)

            if len(geometries) == 1:
                features['geometry'] = geometries[0]  # pragma: nocover
            else:
                features['geometry'] = {'type': 'GeometryCollection', 'geometries': geometries}
        except (AttributeError, KeyError):
            features['geometry'] = {'type': 'GeometryCollection', 'geometries': []}

        data: Dict[str, Any] = {'type': type_, '@context': app.config['API_SCHEMA'],
                                'features': [features]}

        return data
