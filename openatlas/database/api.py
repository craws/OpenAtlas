from typing import Any
from uuid import UUID

from flask import g

from openatlas.database.entity import select_sql

BEGIN_COALESCE = 'COALESCE(e.begin_from, e.begin_to)'
END_COALESCE = 'COALESCE(e.end_to, e.end_from, e.begin_to, e.begin_from)'
TYPE_CLASSES = ['administrative_unit', 'type', 'type_tools']

ORDER_CLAUSES: dict[str, str] = {
    'name_asc': 'ORDER BY e.name ASC, e.id ASC',
    'name_desc': 'ORDER BY e.name DESC, e.id DESC',
    'start_date_asc': f'ORDER BY {BEGIN_COALESCE} ASC NULLS LAST, e.id ASC',
    'start_date_desc': (
        f'ORDER BY {BEGIN_COALESCE} DESC NULLS LAST, e.id DESC'),
    'end_date_asc': f'ORDER BY {END_COALESCE} ASC NULLS LAST, e.id ASC',
    'end_date_desc': f'ORDER BY {END_COALESCE} DESC NULLS LAST, e.id DESC'}
DEFAULT_ORDER = ORDER_CLAUSES['name_asc']

SEARCH_RANK_ORDER = """
    ORDER BY
        CASE
            WHEN LOWER(e.name) = LOWER(%(search)s) THEN 0
            WHEN LOWER(e.name) LIKE LOWER(%(search_prefix)s) THEN 1
            WHEN LOWER(e.name) LIKE LOWER(%(search_like)s) THEN 2
            ELSE 3
        END ASC,
        e.name ASC,
        e.id ASC
"""


def format_date_for_sql(date: str) -> str:
    date_string = date.strip()
    if date_string.startswith('-'):
        return f"{date_string.lstrip('-')} BC"
    return date_string


def escape_like(value: str) -> str:
    return (
        value.replace('\\', '\\\\')
        .replace('%', '\\%')
        .replace('_', '\\_'))


def execute_paginated_entities(
        conditions: list[str],
        params: dict[str, Any],
        order_sql: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
        types: bool = False,
        aliases: bool = False) -> tuple[list[dict[str, Any]], int]:
    where_sql = 'WHERE ' + ' AND '.join(conditions)
    g.cursor.execute(
        f'SELECT COUNT(*) FROM model.entity e {where_sql};',
        params)
    total = g.cursor.fetchone()['count']
    if not total or (offset is not None and offset >= total):
        return [], total

    query_params = dict(params)
    limit_sql = ''
    if limit is not None:
        limit_sql += ' LIMIT %(limit)s'
        query_params['limit'] = limit
    if offset is not None:
        limit_sql += ' OFFSET %(offset)s'
        query_params['offset'] = offset

    if types or aliases:
        inner_sql = (
            f'SELECT e.id FROM model.entity e '
            f'{where_sql} {order_sql}{limit_sql}')
        sql = (
            f'{select_sql(types, aliases)} '
            f'JOIN ({inner_sql}) page ON page.id = e.id '
            f'GROUP BY e.id {order_sql};')
    else:
        sql = f'{select_sql()} {where_sql} {order_sql}{limit_sql};'

    g.cursor.execute(sql, query_params)
    return list(g.cursor), total


### File ###

def get_public_files_api(
        license_ids: set[int],
        public_share_id: int | None,
        limit: int,
        offset: int,
        entity_id: int | None = None) -> tuple[list[dict[str, Any]], int]:
    if not license_ids or public_share_id is None:
        return [], 0  # pragma: no cover

    conditions = [
        "e.openatlas_class_name = 'file'",
        """EXISTS (
            SELECT 1 FROM model.link l
            WHERE l.domain_id = e.id
              AND l.property_code = 'P2'
              AND l.range_id = ANY(%(license_ids)s))""",
        """EXISTS (
            SELECT 1 FROM model.link l
            WHERE l.domain_id = e.id
              AND l.property_code = 'P2'
              AND l.range_id = %(public_share_id)s)"""]
    params: dict[str, Any] = {
        'license_ids': list(license_ids),
        'public_share_id': public_share_id}
    if entity_id is not None:
        conditions.append("""EXISTS (
            SELECT 1 FROM model.link l
            WHERE l.domain_id = e.id
              AND l.property_code = 'P67'
              AND l.range_id = %(entity_id)s)""")
        params['entity_id'] = entity_id

    return execute_paginated_entities(
        conditions,
        params,
        'ORDER BY e.id',
        limit=limit,
        offset=offset,
        types=True)


## Entity ##

def get_entities_api(
        classes: list[str],
        *,
        types: bool = False,
        aliases: bool = False,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        search_name: str | None = None,
        phonetic: bool = False,
        start_date: str | None = None,
        end_date: str | None = None,
        type_ids: list[int] | None = None,
        case_study_ids: list[int] | None = None) \
        -> tuple[list[dict[str, Any]], int]:
    conditions = ['e.openatlas_class_name = ANY(%(classes)s)']
    params: dict[str, Any] = {'classes': classes}

    if search_name:
        escaped = escape_like(search_name)
        params['search_like'] = f'%{escaped}%'
        if phonetic:
            conditions.append(
                '(e.name ILIKE %(search_like)s '
                'OR public.daitch_mokotoff(e.name) '
                '&& public.daitch_mokotoff(%(search)s))')
            params['search'] = search_name
            params['search_prefix'] = f'{escaped}%'
        else:
            conditions.append('e.name ILIKE %(search_like)s')

    if start_date:
        conditions.append(f'{BEGIN_COALESCE} >= %(start_date)s')
        params['start_date'] = format_date_for_sql(start_date)

    if end_date:
        conditions.append(f'{END_COALESCE} <= %(end_date)s')
        params['end_date'] = format_date_for_sql(end_date)

    if type_ids is not None:
        conditions.append("""EXISTS (
            SELECT 1 FROM model.link l
            WHERE l.domain_id = e.id
              AND l.property_code IN ('P2', 'P89')
              AND l.range_id = ANY(%(type_ids)s))""")
        params['type_ids'] = type_ids

    if case_study_ids is not None:
        conditions.append("""EXISTS (
            SELECT 1 FROM model.link l
            WHERE l.domain_id = e.id
              AND l.property_code IN ('P2', 'P89')
              AND l.range_id = ANY(%(case_study_ids)s))""")
        params['case_study_ids'] = case_study_ids

    order_sql = (
        SEARCH_RANK_ORDER if phonetic and search_name
        else ORDER_CLAUSES.get(order_by or '', DEFAULT_ORDER))
    return execute_paginated_entities(
        conditions,
        params,
        order_sql,
        limit=limit,
        offset=offset,
        types=types,
        aliases=aliases)


## Vocabulary ##

def get_type_sub_ids_api(identifier: int | UUID) -> list[int]:
    where_clause = (
        'id = %(identifier)s' if isinstance(identifier, int)
        else 'uuid = %(identifier)s')
    param = identifier if isinstance(identifier, int) else str(identifier)
    g.cursor.execute(
        f"""
        WITH RECURSIVE type_tree AS (
            SELECT id
            FROM model.entity
            WHERE {where_clause}
              AND openatlas_class_name = ANY(%(type_classes)s)
            UNION
            SELECT l.domain_id
            FROM model.link l
            JOIN type_tree tt ON l.range_id = tt.id
            JOIN model.entity e ON l.domain_id = e.id
            WHERE l.property_code IN ('P127', 'P89')
              AND e.openatlas_class_name = ANY(%(type_classes)s))
        SELECT id FROM type_tree;
        """,
        {'identifier': param, 'type_classes': TYPE_CLASSES})
    return [row['id'] for row in list(g.cursor)]


def get_vocab_ids_for_case_study(case_study_id: int) -> set[int]:
    sql = """
        SELECT DISTINCT l_type.range_id
        FROM model.link l_cs
        JOIN model.link l_type ON l_cs.domain_id = l_type.domain_id
        WHERE l_cs.range_id = %(case_study_id)s
          AND l_cs.property_code = 'P2'
          AND l_type.property_code IN ('P2', 'P89');
        """
    g.cursor.execute(sql, {'case_study_id': case_study_id})
    return {row['range_id'] for row in list(g.cursor)}


## Case study ##

def get_overview_counts_by_case_study(
        classes: list[str],
        case_study_id: int | None = None) -> dict[str, int]:
    conditions = ['e.openatlas_class_name = ANY(%(classes)s)']
    params: dict[str, Any] = {'classes': classes}
    if case_study_id is not None:
        conditions.append("""EXISTS (
            SELECT 1 FROM model.link l
            WHERE l.domain_id = e.id
              AND l.property_code = 'P2'
              AND l.range_id = %(case_study_id)s)""")
        params['case_study_id'] = case_study_id

    where_sql = 'WHERE ' + ' AND '.join(conditions)
    g.cursor.execute(
        f"""
        SELECT e.openatlas_class_name AS name, COUNT(e.id) AS count
        FROM model.entity e
        {where_sql}
        GROUP BY e.openatlas_class_name;
        """,
        params)
    return {row['name']: row['count'] for row in list(g.cursor)}


## Geographic ##

SPATIAL_CLASSES = [
    'place',
    'feature',
    'stratigraphic_unit',
    'artifact',
    'human_remains']

ENTITY_SELECT_SQL = """
    e.id,
    e.uuid,
    e.name,
    e.description,
    e.openatlas_class_name,
    COALESCE(to_char(e.begin_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
        AS begin_from,
    e.begin_comment,
    COALESCE(to_char(e.begin_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
        AS begin_to,
    COALESCE(to_char(e.end_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
        AS end_from,
    e.end_comment,
    COALESCE(to_char(e.end_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
        AS end_to"""


def envelope_sql(bbox: tuple[float, float, float, float]) -> str:
    min_lon, min_lat, max_lon, max_lat = bbox
    if min_lon == max_lon and min_lat == max_lat:
        return (
            'public.ST_SetSRID('
            'public.ST_MakePoint(%(min_lon)s, %(min_lat)s), 4326)')
    if min_lon == max_lon or min_lat == max_lat:
        return (
            'public.ST_SetSRID(public.ST_MakeLine('
            'public.ST_MakePoint(%(min_lon)s, %(min_lat)s), '
            'public.ST_MakePoint(%(max_lon)s, %(max_lat)s)), 4326)')
    return (
        'public.ST_MakeEnvelope('
        '%(min_lon)s, %(min_lat)s, %(max_lon)s, %(max_lat)s, 4326)')


def geom_sql(centroid_only: bool) -> str:
    if centroid_only:
        return """
            public.ST_AsGeoJSON(
                COALESCE(
                    g.geom_point,
                    public.ST_PointOnSurface(g.geom_linestring),
                    public.ST_PointOnSurface(g.geom_polygon)))"""
    return """
        public.ST_AsGeoJSON(
            COALESCE(
                g.geom_point,
                g.geom_linestring,
                public.ST_ForcePolygonCCW(g.geom_polygon)))"""


def get_by_bbox(
        bbox: tuple[float, float, float, float],
        centroid_only: bool = False) -> list[dict[str, Any]]:
    min_lon, min_lat, max_lon, max_lat = bbox
    bbox_sql = envelope_sql(bbox)
    geometry_sql = geom_sql(centroid_only)
    g.cursor.execute(
        f"""
        WITH bbox AS (
            SELECT {bbox_sql} AS geom
        ),
        matched_gis AS (
            SELECT
                g.id AS geometry_id,
                g.entity_id,
                g.name AS geometry_name,
                g.description AS geometry_description,
                g.type AS shape_type,
                {geometry_sql} AS geometry
            FROM model.gis g
            CROSS JOIN bbox
            WHERE (
                public.ST_Intersects(g.geom_point, bbox.geom)
                OR public.ST_Intersects(g.geom_linestring, bbox.geom)
                OR public.ST_Intersects(g.geom_polygon, bbox.geom))
        )
        SELECT
            {ENTITY_SELECT_SQL},
            CASE WHEN loc.openatlas_class_name = 'object_location'
                THEN loc.id ELSE NULL END AS location_id,
            mg.geometry_id,
            mg.geometry_name,
            mg.geometry_description,
            mg.shape_type,
            mg.geometry
        FROM matched_gis mg
        JOIN model.entity loc ON loc.id = mg.entity_id
        LEFT JOIN model.link l ON l.range_id = loc.id
            AND l.property_code = 'P53'
            AND loc.openatlas_class_name = 'object_location'
        JOIN model.entity e ON e.id = COALESCE(l.domain_id, loc.id)
            AND e.openatlas_class_name = ANY(%(classes)s)
        ORDER BY e.id, mg.geometry_id;
        """,
        {
            'min_lon': min_lon,
            'min_lat': min_lat,
            'max_lon': max_lon,
            'max_lat': max_lat,
            'classes': SPATIAL_CLASSES})
    return list(g.cursor)


def get_clustered_by_bbox(
        bbox: tuple[float, float, float, float],
        grid_size: float,
        centroid_only: bool = False) -> list[dict[str, Any]]:
    min_lon, min_lat, max_lon, max_lat = bbox
    bbox_sql = envelope_sql(bbox)
    geometry_sql = geom_sql(centroid_only)
    g.cursor.execute(
        f"""
        WITH bbox AS (
            SELECT {bbox_sql} AS geom
        ),
        matched AS (
            SELECT
                e.id AS entity_id,
                g.id AS geometry_id,
                CASE WHEN loc.openatlas_class_name = 'object_location'
                    THEN loc.id ELSE NULL END AS location_id,
                COALESCE(
                    g.geom_point,
                    public.ST_PointOnSurface(g.geom_linestring),
                    public.ST_PointOnSurface(g.geom_polygon)) AS pt
            FROM model.gis g
            CROSS JOIN bbox
            JOIN model.entity loc ON loc.id = g.entity_id
            LEFT JOIN model.link l ON l.range_id = loc.id
                AND l.property_code = 'P53'
                AND loc.openatlas_class_name = 'object_location'
            JOIN model.entity e ON e.id = COALESCE(l.domain_id, loc.id)
                AND e.openatlas_class_name = ANY(%(classes)s)
            WHERE (
                public.ST_Intersects(g.geom_point, bbox.geom)
                OR public.ST_Intersects(g.geom_linestring, bbox.geom)
                OR public.ST_Intersects(g.geom_polygon, bbox.geom))
        ),
        cells AS (
            SELECT
                public.ST_SnapToGrid(
                    public.ST_Transform(
                        public.ST_SetSRID(
                            public.ST_MakePoint(
                                public.ST_X(pt),
                                LEAST(
                                    85.0511287,
                                    GREATEST(-85.0511287, public.ST_Y(pt)))),
                            4326),
                        3857),
                    %(grid_size)s) AS cell,
                COUNT(*) AS point_count,
                MIN(entity_id) AS single_entity_id,
                MIN(geometry_id) AS single_geometry_id,
                MIN(location_id) AS single_location_id,
                public.ST_AsGeoJSON(
                    public.ST_Centroid(public.ST_Collect(pt))
                ) AS cluster_geom,
                MIN(public.ST_X(pt)) AS min_lon,
                MIN(public.ST_Y(pt)) AS min_lat,
                MAX(public.ST_X(pt)) AS max_lon,
                MAX(public.ST_Y(pt)) AS max_lat
            FROM matched
            GROUP BY cell
        )
        SELECT
            c.point_count,
            c.min_lon,
            c.min_lat,
            c.max_lon,
            c.max_lat,
            {ENTITY_SELECT_SQL},
            c.single_location_id AS location_id,
            g.id AS geometry_id,
            g.name AS geometry_name,
            g.description AS geometry_description,
            g.type AS shape_type,
            CASE WHEN c.point_count = 1
                THEN {geometry_sql}
                ELSE c.cluster_geom
            END AS geometry
        FROM cells c
        LEFT JOIN model.entity e
            ON c.point_count = 1 AND e.id = c.single_entity_id
        LEFT JOIN model.gis g
            ON c.point_count = 1 AND g.id = c.single_geometry_id
        ORDER BY c.point_count DESC, c.min_lon, c.min_lat,
            c.single_geometry_id;
        """,
        {
            'min_lon': min_lon,
            'min_lat': min_lat,
            'max_lon': max_lon,
            'max_lat': max_lat,
            'grid_size': grid_size,
            'classes': SPATIAL_CLASSES})
    return list(g.cursor)
