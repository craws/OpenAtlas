import ast
from typing import Any

from flask import g


class Gis:

    @staticmethod
    def get_by_id(id_: int) -> list[dict[str, Any]]:
        geometries = []
        g.cursor.execute(
            f"""
            SELECT
                id,
                name,
                description,
                type,
                public.ST_AsGeoJSON(geom_point) AS point,
                public.ST_AsGeoJSON(geom_linestring) AS linestring,
                public.ST_AsGeoJSON(geom_polygon) AS polygon,
            FROM model.entity place
            JOIN model.gis g ON place.id = g.entity_id
            WHERE place.id = %(id_)s;
            """,
            {'id_': id_})
        for row in g.cursor.fetchall():
            geometry = ast.literal_eval(row['geojson'])
            geometry['title'] = row['name'].replace('"', '\"') \
                if row['name'] else ''
            geometry['description'] = \
                row['description'].replace('"', '\"') \
                if row['description'] else ''
            if row['point']:
                geometry['geom'] = row['point']
            elif row['linestring']:
                geometry['geom'] = row['linestring']
            else:
                geometry['geom'] = row['polygon']
            geometries.append(geometry)
        return geometries

    @staticmethod
    def get_all(extra_ids: list[int]) -> list[dict[str, Any]]:
        #polygon_sql = '' if shape != 'polygon' else \
        #    ' public.ST_AsGeoJSON(public.ST_PointOnSurface(polygon.geom))' \
        #    ' AS polygon_point, '
        g.cursor.execute(
            f"""
            SELECT
                object.id AS object_id,
                g.id,
                g.name,
                g.description,
                g.type,
                public.ST_AsGeoJSON(geom_point) AS point,
                public.ST_AsGeoJSON(geom_linestring) AS linestring,
                public.ST_AsGeoJSON(geom_polygon) AS polygon,
                object.name AS object_name,
                object.description AS object_desc,
                string_agg(CAST(t.range_id AS text), ',') AS types
            FROM model.entity place
            JOIN model.link l ON place.id = l.range_id
            JOIN model.entity object ON l.domain_id = object.id
            JOIN model.gis g ON place.id = g.entity_id
            LEFT JOIN model.link t ON object.id = t.domain_id
                AND t.property_code = 'P2'
            WHERE place.cidoc_class_code = 'E53'
                AND l.property_code = 'P53'
                AND (object.openatlas_class_name = 'place'
                OR object.id IN %(extra_ids)s)
            GROUP BY object.id, g.id;
            """,
            {'extra_ids': tuple(extra_ids)})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def test_geom(geometry: str) -> bool:
        g.cursor.execute(
            """
            SELECT st_isvalid(
                public.ST_SetSRID(
                    public.ST_GeomFromGeoJSON(%(geojson)s),
                    4326
                )
            );
            """,
            {'geojson': geometry})
        return bool(g.cursor.fetchone()['st_isvalid'])

    @staticmethod
    def insert(data: dict[str, Any], shape: str) -> None:
        g.cursor.execute(
            f"""
            INSERT INTO gis.{shape} (entity_id, name, description, type, geom)
            VALUES (
                %(entity_id)s,
                %(name)s,
                %(description)s,
                %(type)s,
                public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s),4326));
            """,
            data)

    @staticmethod
    def insert_import(data: dict[str, Any]) -> None:
        g.cursor.execute(
            """
            INSERT INTO gis.point (entity_id, name, description, type, geom)
            VALUES (
                %(entity_id)s,
                '',
                %(description)s,
                'centerpoint',
                public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s),4326));
            """,
            data)

    @staticmethod
    def delete_by_entity_id(id_: int) -> None:
        g.cursor.execute(
            'DELETE FROM gis.point WHERE entity_id = %(id)s;',
            {'id': id_})
        g.cursor.execute(
            'DELETE FROM gis.linestring WHERE entity_id = %(id)s;',
            {'id': id_})
        g.cursor.execute(
            'DELETE FROM gis.polygon WHERE entity_id = %(id)s;',
            {'id': id_})
