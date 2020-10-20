from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from flask import g
from flask_login import current_user
from psycopg2.extras import NamedTupleCursor

from openatlas import app
from openatlas.models.date import Date
from openatlas.models.link import Link

if TYPE_CHECKING:  # pragma: no cover - Type checking is disabled in tests
    from openatlas.models.node import Node


class Query:

    def __init__(self, row: NamedTupleCursor.Record) -> None:  # pragma: no cover
        from openatlas.forms.date import DateForm

        self.id = row.id
        self.nodes: Dict['Node', str] = {}
        if hasattr(row, 'nodes') and row.nodes:
            for node in row.nodes:
                self.nodes[g.nodes[node['f1']]] = node['f2']  # f1 = node id, f2 = value
        self.aliases: Dict[int, str] = {}
        if hasattr(row, 'aliases') and row.aliases:
            for alias in row.aliases:
                self.aliases[alias['f1']] = alias['f2']  # f1 = alias id, f2 = alias name
            self.aliases = {k: v for k, v in sorted(self.aliases.items(), key=lambda item: item[1])}
        self.name = row.name
        self.description = row.description if row.description else ''
        self.system_type = row.system_type
        self.created = row.created
        self.modified = row.modified
        self.begin_from = None
        self.begin_to = None
        self.begin_comment = None
        self.end_from = None
        self.end_to = None
        self.end_comment = None
        self.note: Optional[str] = None  # User specific, private note for an entity
        self.origin_id: Optional[int] = None
        self.location: Optional[Query] = None  # Needed for API
        if hasattr(row, 'begin_from'):
            self.begin_from = Date.timestamp_to_datetime64(row.begin_from)
            self.begin_to = Date.timestamp_to_datetime64(row.begin_to)
            self.begin_comment = row.begin_comment
            self.end_from = Date.timestamp_to_datetime64(row.end_from)
            self.end_to = Date.timestamp_to_datetime64(row.end_to)
            self.end_comment = row.end_comment
            self.first = DateForm.format_date(self.begin_from, 'year') if self.begin_from else None
            self.last = DateForm.format_date(self.end_from, 'year') if self.end_from else None
            self.last = DateForm.format_date(self.end_to, 'year') if self.end_to else self.last
        self.class_ = g.classes[row.class_code]
        self.view_name = ''  # Used to build URLs
        self.external_references: List[Link] = []
        if self.system_type == 'file':
            self.view_name = 'file'
        elif self.class_.code == 'E33' and self.system_type == 'source translation':
            self.view_name = 'translation'
        elif self.class_.code in app.config['CODE_CLASS']:
            self.view_name = app.config['CODE_CLASS'][self.class_.code]
        elif self.class_.code == 'E55':
            self.view_name = 'node'
        self.table_name = self.view_name  # Used to build tables
        if self.view_name == 'place':
            self.table_name = self.system_type.replace(' ', '_')

    @staticmethod
    def build_sql(nodes: bool = False, aliases: bool = False) -> str:  # pragma: no cover
        # Performance: only join nodes and/or aliases if requested
        sql = """
            SELECT
                e.id as id, e.class_code as class_code, e.name as name,
                e.description as description, e.created as created, e.modified as modified,
                e.system_type as system_type,
                COALESCE(to_char(e.begin_from, 'yyyy-mm-dd BC'), '') AS begin_from, e.begin_comment,
                COALESCE(to_char(e.begin_to, 'yyyy-mm-dd BC'), '') AS begin_to,
                COALESCE(to_char(e.end_from, 'yyyy-mm-dd BC'), '') AS end_from, e.end_comment,
                COALESCE(to_char(e.end_to, 'yyyy-mm-dd BC'), '') AS end_to"""
        if nodes:
            sql += """
                ,array_to_json(
                    array_agg((t.range_id, t.description)) FILTER (WHERE t.range_id IS NOT NULL)
                ) AS nodes """
        if aliases:
            sql += """
                ,array_to_json(
                    array_agg((alias.id, alias.name)) FILTER (WHERE alias.name IS NOT NULL)
                ) AS aliases """
        sql += " FROM model.entity e "
        if nodes:
            sql += """ LEFT JOIN model.link t
                ON e.id = t.domain_id AND t.property_code IN ('P2', 'P89') """
        if aliases:
            sql += """
                LEFT JOIN model.link la
                    ON e.id = la.domain_id AND la.property_code IN ('P1', 'P131')
                LEFT JOIN model.entity alias ON la.range_id = alias.id """
        return sql

    @staticmethod
    def get_by_class_code(code: Union[str, List[str]], meta: Dict[str, Any]) -> List[Query]:
        clause = ""
        parameters = {'codes': tuple(code if isinstance(code, list) else [code])}
        for filter_ in meta['filter']:
            if 'LIKE' in filter_['clause']:
                clause += ' ' + filter_['clause'] + ' LOWER(%(' + str(filter_['idx']) + ')s)'
            else:
                clause += ' ' + filter_['clause'] + ' %(' + str(filter_['idx']) + ')s'
            parameters[str(filter_['idx'])] = filter_['term']
        sql = Query.build_sql() + """
            WHERE class_code IN %(codes)s {clause} 
            ORDER BY {order} {sort};""".format(clause=clause,
                                               order=', '.join(meta['column']),
                                               sort=meta['sort'])
        print(sql)
        print(parameters)
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_menu_item(menu_item: str,
                         meta: Dict[str, Any]) -> List[Query]:  # pragma: no cover
        # Possible class names: actor, event, place, reference, source, object
        clause = ""
        parameters = {'codes': tuple(app.config['CLASS_CODES'][menu_item])}
        for filter_ in meta['filter']:
            clause += ' ' + filter_['clause'] + ' %(' + str(filter_['idx']) + ')s'
            parameters[str(filter_['idx'])] = filter_['term']
        if menu_item == 'source':
            sql = Query.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type = 'source content' {clause}
                 GROUP BY e.id ORDER BY {order} {sort};""".format(clause=clause,
                                                                  order=', '.join(meta['column']),
                                                                  sort=meta['sort'])
        elif menu_item == 'reference':
            sql = Query.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type != 'file' {clause} 
                 GROUP BY e.id ORDER BY {order} {sort};""".format(clause=clause,
                                                                  order=', '.join(meta['column']),
                                                                  sort=meta['sort'])
        else:
            aliases = True if menu_item == 'actor' and current_user.is_authenticated and \
                              current_user.settings['table_show_aliases'] else False
            sql = Query.build_sql(nodes=True if menu_item == 'event' else False,
                                  aliases=aliases) + """
                WHERE e.class_code IN %(codes)s {clause} GROUP BY e.id
                ORDER BY {order} {sort};""".format(clause=clause,
                                                   order=', '.join(meta['column']),
                                                   sort=meta['sort'])
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]
