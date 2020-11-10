import ast
from typing import Any, Dict, List

from flask import g, session, url_for

from openatlas import app
from openatlas.api.v01.error import APIError
from openatlas.models.entity import Entity
from openatlas.models.geonames import Geonames
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.util.display import format_date, get_file_path


class GeoJsonEntity:

    @staticmethod
    def to_camelcase(string: str) -> str:  # pragma: nocover
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
                          'relationType': 'crm:' + link.property.code + 'i_'
                                          + link.property.i18n['en'].replace(' ', '_')})
        return links

    @staticmethod
    def get_file(entity: Entity) -> List[Dict[str, str]]:
        files = []
        for link in Link.get_links(entity.id, codes="P67", inverse=True):  # pragma: nocover
            if link.domain.system_type == 'file':
                path = get_file_path(link.domain.id)
                files.append({'@id': url_for('api_entity', id_=link.domain.id, _external=True),
                              'title': link.domain.name,
                              'license': GeoJsonEntity.get_license(link.domain.id),
                              'url': url_for('display_file_api',
                                             filename=path.name,
                                             _external=True) if path else "N/A"})
        return files

    @staticmethod
    def get_license(entity_id: int) -> str:  # pragma: nocover
        file_license = ""
        for link in Link.get_links(entity_id):
            if link.property.code == "P2":
                file_license = link.range.name
        return file_license

    @staticmethod
    def get_node(entity: Entity) -> List[Dict[str, Any]]:
        nodes = []
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

            hierarchy = []
            for root in node.root:
                hierarchy.append(g.nodes[root].name)  # pragma: nocover
            hierarchy.reverse()
            nodes_dict['hierarchy'] = ' > '.join(map(str, hierarchy))
            nodes.append(nodes_dict)
        return nodes

    @staticmethod
    def get_time(entity: Entity) -> Dict[str, Any]:
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
        return time

    @staticmethod
    def get_geometry(entity: Entity) -> Dict[str, Any]:
        geometries = []
        shape = {'linestring': 'LineString', 'polygon': 'Polygon', 'point': 'Point'}
        for geometry in Gis.get_by_id(entity.location.id):
            geo_dict = {'type': shape[geometry['shape']],
                        'coordinates': geometry['geometry']['coordinates']}
            if geometry['description']:
                geo_dict['description'] = geometry['description']
            if geometry['name']:
                geo_dict['title'] = geometry['name']
            geometries.append(geo_dict)
        if len(geometries) == 1:
            return geometries[0]
        else:
            return {'type': 'GeometryCollection', 'geometries': geometries}

    @staticmethod
    def get_geom_by_entity(entity: Entity):
        if entity.class_.code != 'E53':
            return 'Wrong class'
        geom = []
        for shape in ['point', 'polygon', 'linestring']:
            sql = """
                    SELECT
                        {shape}.id,
                        {shape}.name,
                        {shape}.description,
                        public.ST_AsGeoJSON({shape}.geom) AS geojson
                    FROM model.entity e
                    JOIN gis.{shape} {shape} ON e.id = {shape}.entity_id
                    WHERE e.id = %(entity_id)s;""".format(shape=shape)
            g.execute(sql, {'entity_id': entity.id})
            for row in g.cursor.fetchall():
                test = ast.literal_eval(row.geojson)
                test['title'] = row.name.replace('"', '\"') if row.name else ''
                test['description'] = row.description.replace('"',
                                                              '\"') if row.description else ''
                geom.append(test)
        if len(geom) == 1:
            return geom[0]
        else:
            return {'type': 'GeometryCollection', 'geometries': geom}

    @staticmethod
    def get_geonames(entity: Entity) -> Dict[str, Any]:
        geonames_link = Geonames.get_geonames_link(entity)
        if geonames_link and geonames_link.range.class_.code == 'E18':
            geo_name = {}
            if geonames_link.type.name:
                geo_name['type'] = GeoJsonEntity.to_camelcase(geonames_link.type.name)
            if geonames_link.domain.name:
                geo_name['identifier'] = session['settings']['geonames_url'] + \
                                         geonames_link.domain.name
            return geo_name

    @staticmethod
    def get_entity_by_id(id_: int) -> Entity:
        try:
            int(id_)
        except Exception:
            raise APIError('Invalid ID: ' + str(id_), status_code=404, payload="404b")
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise APIError('Entity ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                           payload="404a")

        return entity

    @staticmethod
    def get_entity(entity: Entity, meta: Dict[str, Any]) -> Dict[str, Any]:
        type_ = 'FeatureCollection'

        class_code = ''.join(entity.class_.code + " " + entity.class_.i18n['en']).replace(" ", "_")
        features = {'@id': url_for('entity_view', id_=entity.id, _external=True),
                    'type': 'Feature',
                    'crmClass': "crm:" + class_code,
                    'properties': {'title': entity.name}}

        # Relations
        if GeoJsonEntity.get_links(entity) and 'relations' in meta['show']:
            features['relations'] = GeoJsonEntity.get_links(entity)

        # Descriptions
        if entity.description:
            features['description'] = [{'value': entity.description}]

        # Types
        if GeoJsonEntity.get_node(entity) and 'types' in meta['show']:
            features['types'] = GeoJsonEntity.get_node(entity)

        # Alias
        if entity.aliases and 'names' in meta['show']:
            features['names'] = []
            for key, value in entity.aliases.items():
                features['names'].append({"alias": value})

        # Depictions
        if GeoJsonEntity.get_file(entity) and 'depictions' in meta['show']:  # pragma: nocover
            features['depictions'] = GeoJsonEntity.get_file(entity)

        # Time spans
        if GeoJsonEntity.get_time(entity) and 'when' in meta['show']:
            if entity.begin_from or entity.end_from:
                features['when'] = {'timespans': [GeoJsonEntity.get_time(entity)]}

        # Geonames
        if GeoJsonEntity.get_geonames(entity) and 'geonames' in meta['show']:
            features['links'] = [GeoJsonEntity.get_geonames(entity)]

        # Geometry
        # Todo: both functions are basically the same, compare and merge functions
        if 'geometry' in meta['show'] and entity.class_.code == 'E53':
            features['geometry'] = GeoJsonEntity.get_geom_by_entity(entity)
        elif 'geometry' in meta['show'] and entity.location:
            features['geometry'] = GeoJsonEntity.get_geom_by_entity(entity.location)

        data: Dict[str, Any] = {'type': type_,
                                '@context': app.config['API_SCHEMA'],
                                'features': [features]}
        return data
