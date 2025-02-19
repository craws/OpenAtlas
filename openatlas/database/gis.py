import ast
from collections import defaultdict
from typing import Any

from flask import g


def get_by_id(id_: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            g.id,
            g.name,
            g.description,
            g.type,
            public.ST_AsGeoJSON(geom_point) AS point,
            public.ST_AsGeoJSON(geom_linestring) AS linestring,
            public.ST_AsGeoJSON(ST_ForcePolygonCCW(geom_polygon)) AS polygon
        FROM model.entity place
        JOIN model.gis g ON place.id = g.entity_id
        WHERE place.id = %(id_)s;
        """,
        {'id_': id_})
    return [get_geometry_dict(row) for row in list(g.cursor)]


def get_by_ids(ids: list[int]) -> defaultdict[int, list[dict[str, Any]]]:
    g.cursor.execute(
        """
        SELECT
            g.id,
            g.entity_id,
            g.name,
            g.description,
            g.type,
            public.ST_AsGeoJSON(geom_point) AS point,
            public.ST_AsGeoJSON(geom_linestring) AS linestring,
            public.ST_AsGeoJSON(ST_ForcePolygonCCW(geom_polygon)) AS polygon
        FROM model.entity place
        JOIN model.gis g ON place.id = g.entity_id
        WHERE place.id IN %(ids)s;
        """,
        {'ids': tuple(ids)})
    locations = defaultdict(list)
    for row in list(g.cursor):
        locations[row['entity_id']].append(get_geometry_dict(row))
    return locations


def get_by_place_ids(
        ids: list[int]) -> defaultdict[int, list[dict[str, Any]]]:
    g.cursor.execute(
        """
        SELECT
            g.id,
			l.domain_id as entity_id,
            g.entity_id as location_id,
            g.name,
            g.description,
            g.type,
            public.ST_AsGeoJSON(geom_point) AS point,
            public.ST_AsGeoJSON(geom_linestring) AS linestring,
            public.ST_AsGeoJSON(ST_ForcePolygonCCW(geom_polygon)) AS polygon
		FROM model.link l
        JOIN model.gis g ON l.range_id = g.entity_id
		WHERE l.property_code = 'P53' AND l.domain_id IN %(ids)s;
        """,
        {'ids': tuple(ids)})
    locations = defaultdict(list)
    for row in list(g.cursor):
        locations[row['entity_id']].append(get_geometry_dict(row))
    return locations


def get_geometry_dict(row: dict[str, Any]) -> dict[str, Any]:
    if row['point']:
        geometry = ast.literal_eval(row['point'])
    elif row['linestring']:
        geometry = ast.literal_eval(row['linestring'])
    else:
        geometry = ast.literal_eval(row['polygon'])
    geometry['title'] = row['name'].replace('"', '\"') \
        if row['name'] else ''
    geometry['description'] = row['description'].replace('"', '\"') \
        if row['description'] else ''
    geometry['shapeType'] = row['type'].replace('"', '\"') \
        if row['type'] else ''
    return geometry


def get_centroids_by_id(id_: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            g.id,
            g.name,
            g.description,
            g.type,
            CASE WHEN geom_linestring IS NULL THEN NULL ELSE
                public.ST_AsGeoJSON(public.ST_PointOnSurface(geom_linestring))
                END AS linestring_point,
            CASE WHEN geom_polygon IS NULL THEN NULL ELSE
                public.ST_AsGeoJSON(public.ST_PointOnSurface(geom_polygon))
                END AS polygon_point
        FROM model.entity place
        JOIN model.gis g ON place.id = g.entity_id
        WHERE place.id = %(id_)s;
        """,
        {'id_': id_})
    geometries = []
    for row in list(g.cursor):
        if data := get_centroid_dict(row):
            geometries.append(data)
    return geometries


def get_centroids_by_ids(ids: list[int]) -> defaultdict[int, list[Any]]:
    g.cursor.execute(
        """
        SELECT
            g.id,
            g.entity_id,
            g.name,
            g.description,
            g.type,
            CASE WHEN geom_linestring IS NULL THEN NULL ELSE
                public.ST_AsGeoJSON(public.ST_PointOnSurface(geom_linestring))
                END AS linestring_point,
            CASE WHEN geom_polygon IS NULL THEN NULL ELSE
                public.ST_AsGeoJSON(public.ST_PointOnSurface(geom_polygon))
                END AS polygon_point
        FROM model.entity place
        JOIN model.gis g ON place.id = g.entity_id
        WHERE place.id IN %(ids)s;
        """,
        {'ids': tuple(ids)})
    locations = defaultdict(list)
    for row in list(g.cursor):
        locations[row['entity_id']].append(get_centroid_dict(row))
    return locations


def get_centroid_dict(row: dict[str, Any]) -> dict[str, Any]:
    if row['linestring_point']:
        geometry = ast.literal_eval(row['linestring_point'])
    elif row['polygon_point']:
        geometry = ast.literal_eval(row['polygon_point'])
    else:
        return {}  # pragma: no cover, because ignored by optimizer
    geometry['title'] = \
        (row['name'].replace('"', '\"') if row['name'] else '') \
        + '(autogenerated)'
    geometry['description'] = row['description'].replace('"', '\"') \
        if row['description'] else ''
    geometry['shapeType'] = 'centerpoint'
    return geometry


def get_wkt_by_id(id_: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            g.id,
            g.name,
            g.description,
            g.type,
            public.ST_AsText(geom_point) AS point,
            public.ST_AsText(geom_linestring) AS linestring,
            public.ST_AsText(ST_ForcePolygonCCW(geom_polygon)) AS polygon
        FROM model.entity place
        JOIN model.gis g ON place.id = g.entity_id
        WHERE place.id = %(id_)s;
        """,
        {'id_': id_})
    geometries = []
    for row in list(g.cursor):
        geometry = {}
        if row['point']:
            geometry['defined_by'] = row['point']
        elif row['linestring']:
            geometry['defined_by'] = row['linestring']
        else:
            geometry['defined_by'] = row['polygon']
        geometry['content'] = row['description'].replace('"', '\"') \
            if row['description'] else ''
        geometry['shape_type'] = row['type'].replace('"', '\"') \
            if row['type'] else ''
        geometries.append(geometry)
    return geometries


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
            public.ST_AsGeoJSON(ST_ForcePolygonCCW(geom_polygon)) AS polygon,
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
    return list(g.cursor)


def test_geom(geometry: str) -> bool:
    g.cursor.execute(
        """
        SELECT st_isvalid(
            public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s), 4326));
        """,
        {'geojson': geometry})
    return bool(g.cursor.fetchone()['st_isvalid'])


def insert(data: dict[str, Any], shape: str) -> None:
    g.cursor.execute(
        f"""
        INSERT INTO model.gis (
            entity_id, name, description, type, geom_{shape}
        ) VALUES (
            %(entity_id)s, %(name)s, %(description)s, %(type)s,
            public.ST_SetSRID(public.ST_GeomFromGeoJSON(%(geojson)s),4326)
        );
        """,
        data)


def insert_wkt(data: dict[str, Any], shape: str) -> None:
    g.cursor.execute(
        f"""
        INSERT INTO model.gis (
            entity_id, name, description, type, geom_{shape}
        ) VALUES (
            %(entity_id)s, '', %(description)s, %(type)s,
            public.ST_SetSRID(public.ST_GeomFromText(%(wkt)s),4326));
        """,
        data)


def delete_by_entity_id(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM model.gis WHERE entity_id = %(id)s;',
        {'id': id_})
