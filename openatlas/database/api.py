from collections import defaultdict
from typing import Any

from flask import g
from shapely import GeometryCollection, from_wkt

from openatlas.database.entity import select_sql

### Files (Entity) ###

def check_file(file_id: int) -> dict[str, str | list[int]]:
    sql = """                                                                                                                                                                                                                          
        SELECT                                                                                                                                                                                                                         
            e.openatlas_class_name,                                                                                                                                                                                                    
            array_agg(t.range_id) FILTER (WHERE t.range_id IS NOT NULL) AS type_ids                                                                                                                                                    
        FROM model.entity e                                                                                                                                                                                                            
        LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code = 'P2'                                                                                                                                                        
        WHERE e.id = %(id)s
        GROUP BY e.openatlas_class_name;
    """
    g.cursor.execute(sql, {'id': file_id})
    return g.cursor.fetchone()



### Entity ###

def _format_date_for_sql(date: Any) -> str | None:
    if date is None:
        return None
    date_string = str(date).strip()
    if date_string.startswith('-'):
        return f"{date_string.lstrip('-')} BC"
    return date_string


def get_by_class_api(
        class_: str,
        types: bool = False,
        aliases: bool = False,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        search_name: str | None = None,
        start_date: Any = None,
        end_date: Any = None,
        type_ids: list[int] | None = None,
        case_study_ids: list[int] | None = None) -> list[dict[str, Any]]:
    inner_sql = ('SELECT e2.id FROM model.entity e2 WHERE '
                 'e2.openatlas_class_name = %(class)s')
    params: dict[str, Any] = {'class': class_}

    if search_name:
        inner_sql += ' AND e2.name ILIKE %(search)s'
        params['search'] = f'%{search_name}%'

    if start_date:
        inner_sql += (' AND COALESCE(e2.begin_from, e2.begin_to) >= %('
                      'start_date)s')
        params['start_date'] = _format_date_for_sql(start_date)

    if end_date:
        inner_sql += (
            ' AND COALESCE(e2.end_to, e2.end_from, e2.begin_to, '
            'e2.begin_from) '
            '<= %(end_date)s')
        params['end_date'] = _format_date_for_sql(end_date)

    if type_ids is not None:
        if not type_ids:
            return []
        inner_sql += (
            ' AND EXISTS (SELECT 1 FROM model.link l_t '
            'WHERE l_t.domain_id = e2.id AND l_t.range_id IN %(type_ids)s '
            "AND l_t.property_code IN ('P2', 'P89'))")
        params['type_ids'] = tuple(type_ids)

    if case_study_ids is not None:
        if not case_study_ids:
            return []
        inner_sql += (
            ' AND EXISTS (SELECT 1 FROM model.link l_cs '
            'WHERE l_cs.domain_id = e2.id AND l_cs.range_id IN %('
            'case_study_ids)s '
            "AND l_cs.property_code IN ('P2', 'P89'))")
        params['case_study_ids'] = tuple(case_study_ids)

    order_sql = ''
    match order_by:
        case 'name_desc':
            order_sql = ' ORDER BY e2.name DESC, e2.id DESC'
        case 'start_date_asc':
            order_sql = ' ORDER BY e2.begin_from ASC NULLS LAST, e2.id ASC'
        case 'start_date_desc':
            order_sql = ' ORDER BY e2.begin_from DESC NULLS LAST, e2.id DESC'
        case 'end_date_asc':
            order_sql = (
                ' ORDER BY COALESCE(e2.end_to, e2.end_from, e2.begin_to, '
                'e2.begin_from) ASC NULLS LAST, e2.id ASC')
        case 'end_date_desc':
            order_sql = (
                ' ORDER BY COALESCE(e2.end_to, e2.end_from, e2.begin_to, '
                'e2.begin_from) DESC NULLS LAST, e2.id DESC')
        case _:
            order_sql = ' ORDER BY e2.name ASC, e2.id ASC'

    inner_sql += order_sql

    if limit is not None:
        inner_sql += ' LIMIT %(limit)s'
        params['limit'] = limit
    if offset is not None:
        inner_sql += ' OFFSET %(offset)s'
        params['offset'] = offset

    sql = select_sql(types, aliases)
    sql += f' JOIN ({inner_sql}) AS le ON e.id = le.id GROUP BY e.id'
    sql += order_sql.replace('e2.', 'e.')
    sql += ';'

    g.cursor.execute(sql, params)
    return list(g.cursor)


def get_count_by_class_api(
        class_: str,
        search_name: str | None = None,
        start_date: Any = None,
        end_date: Any = None,
        type_ids: list[int] | None = None,
        case_study_ids: list[int] | None = None) -> int:
    sql = (
        'SELECT COUNT(*) FROM model.entity e '
        'WHERE e.openatlas_class_name = %(class)s')
    params: dict[str, Any] = {'class': class_}

    if search_name:
        sql += ' AND e.name ILIKE %(search)s'
        params['search'] = f'%{search_name}%'

    if start_date:
        sql += ' AND COALESCE(e.begin_from, e.begin_to) >= %(start_date)s'
        params['start_date'] = _format_date_for_sql(start_date)

    if end_date:
        sql += (
            ' AND COALESCE(e.end_to, e.end_from, e.begin_to, e.begin_from) '
            '<= %(end_date)s')
        params['end_date'] = _format_date_for_sql(end_date)

    if type_ids is not None:
        if not type_ids:
            return 0
        sql += (
            ' AND EXISTS (SELECT 1 FROM model.link l_t '
            'WHERE l_t.domain_id = e.id AND l_t.range_id IN %(type_ids)s '
            "AND l_t.property_code IN ('P2', 'P89'))")
        params['type_ids'] = tuple(type_ids)

    if case_study_ids is not None:
        if not case_study_ids:
            return 0
        sql += (
            ' AND EXISTS (SELECT 1 FROM model.link l_cs '
            'WHERE l_cs.domain_id = e.id AND l_cs.range_id IN %('
            'case_study_ids)s '
            "AND l_cs.property_code IN ('P2', 'P89'))")
        params['case_study_ids'] = tuple(case_study_ids)

    sql += ';'
    g.cursor.execute(sql, params)
    return g.cursor.fetchone()['count']


def get_vocab_ids_for_case_study(case_study_id: int) -> set[int]:
    sql = """
          SELECT DISTINCT l_type.range_id
          FROM model.link l_cs
                   JOIN model.link l_type ON l_cs.domain_id = l_type.domain_id
          WHERE l_cs.range_id = %(case_study_id)s
            AND l_cs.property_code = 'P2'
            AND l_type.property_code IN ('P2', 'P89') \
          """
    g.cursor.execute(sql, {'case_study_id': case_study_id})
    return {row['range_id'] for row in g.cursor.fetchall()}


def get_overview_counts_by_case_study(
        classes: list[str],
        case_study_id: int | None = None) -> dict[str, int]:
    sql = """
          SELECT e.openatlas_class_name AS name, COUNT(e.id) AS count
          FROM model.entity e \
          """
    if case_study_id is not None:
        sql += """
            JOIN model.link l_cs ON e.id = l_cs.domain_id
            WHERE e.openatlas_class_name IN %(classes)s
              AND l_cs.range_id = %(case_study_id)s
              AND l_cs.property_code = 'P2'
        """
    else:
        sql += """
            WHERE e.openatlas_class_name IN %(classes)s
        """

    sql += " GROUP BY e.openatlas_class_name;"

    g.cursor.execute(sql, {
        'classes': tuple(classes),
        'case_study_id': case_study_id})
    return {row['name']: row['count'] for row in list(g.cursor)}


### GIS ###

def get_wkts_by_ids(ids: list[int]) -> dict[int, str]:
    if not ids:
        return {}
    g.cursor.execute(
        """
        SELECT place.id,
               public.ST_AsText(geom_point)                       AS point,
               public.ST_AsText(geom_linestring)                  AS linestring,
               public.ST_AsText(ST_ForcePolygonCCW(geom_polygon)) AS polygon
        FROM model.entity place
                 JOIN model.gis g ON place.id = g.entity_id
        WHERE place.id IN %(ids)s;
        """,
        {'ids': tuple(ids)})
    geometries = defaultdict(list)
    for row in list(g.cursor):
        if row['point']:
            geometries[row['id']].append(from_wkt(row['point']))
        if row['linestring']:
            geometries[row['id']].append(from_wkt(row['linestring']))
        if row['polygon']:
            geometries[row['id']].append(from_wkt(row['polygon']))
    result = {}
    for id_, geoms in geometries.items():
        if not geoms:
            result[id_] = ""
        elif len(geoms) == 1:
            result[id_] = geoms[0].wkt
        else:
            result[id_] = GeometryCollection(geoms).wkt
    return result
