# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information

from flask import json
import openatlas


class GisMapper(object):

    @staticmethod
    def get_all(object_ids=None):
        all_ = {'point': [], 'polygon': []}
        selected = {'point': [], 'polygon': [], 'polygon_point': []}
        object_ids = object_ids if object_ids else []
        object_ids = object_ids if isinstance(object_ids, list) else [object_ids]
        polygon_point_sql = """
            (SELECT ST_AsGeoJSON(ST_PointOnSurface(p.geom))
            FROM gis.polygon p WHERE id = polygon.id) AS polygon_point, """
        for shape in ['point', 'polygon']:
            sql = """
                SELECT
                    object.id AS object_id,
                    {shape}.id,
                    {shape}.name,
                    {shape}.description,
                    {shape}.type,
                    ST_AsGeoJSON({shape}.geom) AS geojson, {polygon_point_sql}
                    object.name AS object_name,
                    object.description AS object_description,
                    (SELECT COUNT(*) FROM gis.point point2
                        WHERE {shape}.entity_id = point2.entity_id) AS point_count,
                    (SELECT COUNT(*) FROM gis.polygon polygon2
                        WHERE {shape}.entity_id = polygon2.entity_id) AS polygon_count
                FROM model.entity place
                JOIN model.link l ON place.id = l.range_id
                JOIN model.entity object ON l.domain_id = object.id
                JOIN gis.{shape} {shape} ON place.id = {shape}.entity_id
                WHERE place.class_code = 'E53' AND l.property_code = 'P53';""".format(
                        shape=shape,
                        polygon_point_sql=polygon_point_sql if shape == 'polygon' else '')
            cursor = openatlas.get_cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                item = {
                    'type': 'Feature',
                    'geometry': json.loads(row.geojson),
                    'properties': {
                        'title': row.object_name.replace('"', '\"'),
                        'objectId': row.object_id,
                        'objectDescription': row.object_description.replace('"', '\"'),
                        'id': row.id,
                        'name': row.name.replace('"', '\"'),
                        'description': row.description.replace('"', '\"') if row.description else '',
                        'siteType': 'To do',
                        'shapeType': row.type,
                        'count': row.point_count + row.polygon_count}}
                if row.object_id in object_ids:
                    selected[shape].append(item)
                else:
                    all_[shape].append(item)
                if hasattr(row, 'polygon_point'):
                    item['geometry'] = json.loads(row.polygon_point)
                    if row.object_id in object_ids:
                        selected['polygon_point'].append(item)
                    else:
                        all_['point'].append(item)
        gis = {
            'gisPointAll': json.dumps(all_['point']),
            'gisPointSelected': json.dumps(selected['point']),
            'gisPolygonAll': json.dumps(all_['polygon']),
            'gisPolygonSelected': json.dumps(selected['polygon']),
            'gisPolygonPointSelected': json.dumps(selected['polygon_point'])}
        return gis
