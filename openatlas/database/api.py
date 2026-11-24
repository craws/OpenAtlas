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
