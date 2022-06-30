import ast
from typing import Any

from flask import g


class Gis:

    @staticmethod
    def get_by_id(id_: int) -> list[dict[str, Any]]:
        geometries = []
        g.cursor.execute(
            """
            SELECT
                g.id,
                g.name,
                g.description,
                g.type,
                public.ST_AsGeoJSON(geom_point) AS point,
                public.ST_AsGeoJSON(geom_linestring) AS linestring,
                public.ST_AsGeoJSON(geom_polygon) AS polygon
            FROM model.entity place
            JOIN model.gis g ON place.id = g.entity_id
            WHERE place.id = %(id_)s;
            """,
            {'id_': id_})
        for row in g.cursor.fetchall():
            if row['point']:
                geometry = ast.literal_eval(row['point'])
            elif row['linestring']:  # pragma: no cover
                geometry = ast.literal_eval(row['linestring'])
            else:  # pragma: no cover
                geometry = ast.literal_eval(row['polygon'])
            geometry['title'] = row['name'].replace('"', '\"') \
                if row['name'] else ''
            geometry['description'] = \
                row['description'].replace('"', '\"') \
                    if row['description'] else ''
            geometry['shapeType'] = row['type'].replace('"', '\"') \
                if row['type'] else ''
            geometries.append(geometry)
        return geometries

    @staticmethod
    def get_all(extra_ids: list[int]) -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT
                object.id AS object_id,
                g.entity_id AS location_id,
                g.id,
                g.name,
                g.description,
                g.type,
                public.ST_AsGeoJSON(geom_point) AS point,
                public.ST_AsGeoJSON(geom_linestring) AS linestring,
                public.ST_AsGeoJSON(geom_polygon) AS polygon,
                CASE WHEN geom_polygon IS NULL THEN NULL ELSE
                    public.ST_AsGeoJSON(public.ST_PointOnSurface(geom_polygon))
                    END AS polygon_point,
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
                    4326));
            """,
            {'geojson': geometry})
        return bool(g.cursor.fetchone()['st_isvalid'])

    @staticmethod
    def insert(data: dict[str, Any], shape: str) -> None:
        g.cursor.execute(
            f"""
            INSERT INTO model.gis (
                entity_id,
                name,
                description,
                type,
                geom_{shape})
            VALUES (
                %(entity_id)s,
                %(name)s,
                %(description)s,
                %(type)s,
                public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s),4326)
            );
            """,
            data)

    @staticmethod
    def insert_import(data: dict[str, Any]) -> None:
        g.cursor.execute(
            """
            INSERT INTO model.gis (
                entity_id,
                name,
                description,
                type,
                geom_point)
            VALUES (
                %(entity_id)s,
                '',
                %(description)s,
                'centerpoint',
                public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s),4326)
            );
            """,
            data)

    @staticmethod
    def delete_by_entity_id(id_: int) -> None:
        g.cursor.execute(
            'DELETE FROM model.gis WHERE entity_id = %(id)s;',
            {'id': id_})
