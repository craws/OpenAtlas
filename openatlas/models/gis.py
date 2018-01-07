# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import json
import openatlas
from openatlas.util.util import uc_first


class GisMapper:

    @staticmethod
    def get_all(object_ids=None):
        all_ = {'point': [], 'polygon': []}
        selected = {'point': [], 'polygon': [], 'polygon_point': []}
        object_ids = object_ids if object_ids else []
        object_ids = object_ids if isinstance(object_ids, list) else [object_ids]
        polygon_point_sql = """
            (SELECT public.ST_AsGeoJSON(public.ST_PointOnSurface(p.geom))
            FROM gis.polygon p WHERE id = polygon.id) AS polygon_point, """
        for shape in ['point', 'polygon']:
            sql = """
                SELECT
                    object.id AS object_id,
                    {shape}.id,
                    {shape}.name,
                    {shape}.description,
                    {shape}.type,
                    public.ST_AsGeoJSON({shape}.geom) AS geojson, {polygon_point_sql}
                    object.name AS object_name,
                    object.description AS object_desc,
                    string_agg(CAST(t.range_id AS text), ',') AS types,
                    (SELECT COUNT(*) FROM gis.point point2
                        WHERE {shape}.entity_id = point2.entity_id) AS point_count,
                    (SELECT COUNT(*) FROM gis.polygon polygon2
                        WHERE {shape}.entity_id = polygon2.entity_id) AS polygon_count
                FROM model.entity place
                JOIN model.link l ON place.id = l.range_id
                JOIN model.entity object ON l.domain_id = object.id
                JOIN gis.{shape} {shape} ON place.id = {shape}.entity_id
                LEFT JOIN model.link t ON object.id = t.domain_id AND t.property_code = 'P2'
                WHERE place.class_code = 'E53' AND l.property_code = 'P53'
                GROUP BY object.id, {shape}.id;""".format(
                        shape=shape,
                        polygon_point_sql=polygon_point_sql if shape == 'polygon' else '')
            cursor = openatlas.get_cursor()
            cursor.execute(sql)
            place_type_root_id = openatlas.NodeMapper.get_hierarchy_by_name('Place').id
            for row in cursor.fetchall():
                description = row.description.replace('"', '\"') if row.description else ''
                object_desc = row.object_desc.replace('"', '\"') if row.object_desc else ''
                item = {
                    'type': 'Feature',
                    'geometry': json.loads(row.geojson),
                    'properties': {
                        'title': row.object_name.replace('"', '\"'),
                        'objectId': row.object_id,
                        'objectDescription': object_desc,
                        'id': row.id,
                        'name': row.name.replace('"', '\"'),
                        'description': description,
                        'siteType': '',
                        'shapeType': uc_first(row.type),
                        'count': row.point_count + row.polygon_count}}
                if hasattr(row, 'types') and row.types:
                    nodes_list = ast.literal_eval('[' + row.types + ']')
                    for node_id in list(set(nodes_list)):
                        node = openatlas.nodes[node_id]
                        if node.root and node.root[-1] == place_type_root_id:
                            item['properties']['siteType'] = node.name
                            break
                if row.object_id in object_ids:
                    selected[shape].append(item)
                else:
                    all_[shape].append(item)
                if hasattr(row, 'polygon_point'):
                    polygon_point_item = dict(item)  # make a copy to prevent overriding geometry
                    polygon_point_item['geometry'] = json.loads(row.polygon_point)
                    if row.object_id in object_ids:
                        selected['polygon_point'].append(polygon_point_item)
                    else:
                        all_['point'].append(polygon_point_item)
        gis = {
            'gisPointAll': json.dumps(all_['point']),
            'gisPointSelected': json.dumps(selected['point']),
            'gisPolygonAll': json.dumps(all_['polygon']),
            'gisPolygonSelected': json.dumps(selected['polygon']),
            'gisPolygonPointSelected': json.dumps(selected['polygon_point'])}
        return gis

    @staticmethod
    def insert(entity, form):
        cursor = openatlas.get_cursor()
        for shape in ['point', 'polygon']:
            data = getattr(form, 'gis_' + shape + 's').data
            if not data:
                continue
            for item in json.loads(data):
                sql = """
                    INSERT INTO gis.{shape} (entity_id, name, description, type, geom)
                    VALUES (
                        %(entity_id)s,
                        %(name)s,
                        %(description)s,
                        %(type)s,
                        public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s),4326));
                    """.format(shape=shape)
                cursor.execute(sql, {
                    'entity_id': entity.id,
                    'name': item['properties']['name'],
                    'description': item['properties']['description'],
                    'type': item['properties']['shapeType'],
                    'geojson': json.dumps(item['geometry'])})

    @staticmethod
    def delete_by_entity(entity):
        cursor = openatlas.get_cursor()
        sql = 'DELETE FROM gis.point WHERE entity_id = %(entity_id)s;'
        cursor.execute(sql, {'entity_id': entity.id})
        sql = 'DELETE FROM gis.polygon WHERE entity_id = %(entity_id)s;'
        cursor.execute(sql, {'entity_id': entity.id})
