from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from flask import g
from flask_login import current_user
from flask_wtf import FlaskForm
from psycopg2.extras import NamedTupleCursor

from openatlas import app
from openatlas.models.date import Date
from openatlas.models.link import Link
from openatlas.util.display import link

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

    sql_orphan = """
          SELECT e.id FROM model.entity e
          LEFT JOIN model.link l1 on e.id = l1.domain_id AND l1.range_id NOT IN
              (SELECT id FROM model.entity WHERE class_code = 'E55')
          LEFT JOIN model.link l2 on e.id = l2.range_id
          WHERE l1.domain_id IS NULL AND l2.range_id IS NULL AND e.class_code != 'E55'"""

    def get_linked_entity(self, code: str, inverse: bool = False,
                          nodes: bool = False) -> Optional[Query]:
        return Link.get_linked_entity(self.id, code, inverse=inverse, nodes=nodes)

    def get_linked_entity_safe(self, code: str, inverse: bool = False,
                               nodes: bool = False) -> Query:
        return Link.get_linked_entity_safe(self.id, code, inverse, nodes)

    def get_linked_entities(self,
                            code: Union[str, List[str]],
                            inverse: bool = False,
                            nodes: bool = False) -> List[Query]:
        return Link.get_linked_entities(self.id, code, inverse=inverse, nodes=nodes)

    def link(self,
             code: str,
             range_: Union[Query, List[Query]],
             description: Optional[str] = None,
             inverse: bool = False,
             type_id: Optional[int] = None) -> List[int]:
        return Link.insert(self, code, range_, description, inverse, type_id)

    def link_string(self,
                    code: str,
                    range_: str,
                    description: Optional[str] = None,
                    inverse: bool = False) -> List[int]:
        # range_ string from a form, can be empty, an int or an int list presentation
        # e.g. '', '1', '[]', '[1, 2]'
        ids = ast.literal_eval(range_)
        ids = [int(id_) for id_ in ids] if isinstance(ids, list) else [int(ids)]
        return Link.insert(self, code, Query.get_by_ids(ids), description, inverse)

    def get_links(self, codes: Union[str, List[str]], inverse: bool = False) -> List[Link]:
        return Link.get_links(self.id, codes, inverse)

    def delete(self) -> None:
        Query.delete_(self.id)

    def delete_links(self, codes: List[str], inverse: bool = False) -> None:
        Link.delete_by_codes(self, codes, inverse)

    def update(self, form: Optional[FlaskForm] = None) -> None:
        from openatlas.forms.date import DateForm
        from openatlas.util.display import sanitize
        if form:
            self.save_nodes(form)
            for field in ['name', 'description']:
                if hasattr(form, field):
                    setattr(self, field, getattr(form, field).data)
            if isinstance(form, DateForm):
                self.set_dates(form)
            if hasattr(form, 'alias') and (
                    self.system_type == 'place' or
                    self.class_.code in app.config['CLASS_CODES']['actor']):
                self.update_aliases(form)
        if self.class_.code == 'E53':
            self.name = sanitize(self.name, 'node')
        if self.system_type == 'place location':
            self.name = 'Location of ' + self.name
            self.description = None
        sql = """
              UPDATE model.entity SET
              (name, description, begin_from, begin_to, begin_comment, end_from, end_to, end_comment)
                  = (%(name)s, %(description)s, %(begin_from)s, %(begin_to)s, %(begin_comment)s,
                  %(end_from)s, %(end_to)s, %(end_comment)s)
              WHERE id = %(id)s;"""
        g.execute(sql, {'id': self.id,
                        'name': str(self.name).strip(),
                        'begin_from': Date.datetime64_to_timestamp(self.begin_from),
                        'begin_to': Date.datetime64_to_timestamp(self.begin_to),
                        'end_from': Date.datetime64_to_timestamp(self.end_from),
                        'end_to': Date.datetime64_to_timestamp(self.end_to),
                        'begin_comment': str(self.begin_comment).strip() if
                        self.begin_comment else None,
                        'end_comment': str(self.end_comment).strip() if self.end_comment else None,
                        'description': sanitize(self.description, 'text')})

    def update_aliases(self, form: FlaskForm) -> None:
        old_aliases = self.aliases
        new_aliases = form.alias.data
        delete_ids = []
        for id_, alias in old_aliases.items():  # Compare old aliases with form values
            if alias in new_aliases:
                new_aliases.remove(alias)
            else:
                delete_ids.append(id_)
        for id_ in delete_ids:  # Delete obsolete aliases
            Query.delete_(id_)
        for alias in new_aliases:  # Insert new aliases if not empty
            if alias.strip() and self.class_.code == 'E18':
                self.link('P1', Query.insert('E41', alias))
            elif alias.strip():
                self.link('P131', Query.insert('E82', alias))

    def save_nodes(self, form: FlaskForm) -> None:
        from openatlas.models.node import Node
        Node.save_entity_nodes(self, form)

    def set_dates(self, form: FlaskForm) -> None:
        self.begin_from = None
        self.begin_to = None
        self.begin_comment = None
        self.end_from = None
        self.end_to = None
        self.end_comment = None
        if form.begin_year_from.data:  # Only if begin year is set create a begin date or time span
            self.begin_comment = form.begin_comment.data
            self.begin_from = Date.form_to_datetime64(form.begin_year_from.data,
                                                      form.begin_month_from.data,
                                                      form.begin_day_from.data)
            self.begin_to = Date.form_to_datetime64(form.begin_year_to.data,
                                                    form.begin_month_to.data,
                                                    form.begin_day_to.data,
                                                    to_date=True)

        if form.end_year_from.data:  # Only if end year is set create a year date or time span
            self.end_comment = form.end_comment.data
            self.end_from = Date.form_to_datetime64(form.end_year_from.data,
                                                    form.end_month_from.data,
                                                    form.end_day_from.data)
            self.end_to = Date.form_to_datetime64(form.end_year_to.data,
                                                  form.end_month_to.data,
                                                  form.end_day_to.data,
                                                  to_date=True)

    def get_profile_image_id(self) -> Optional[int]:
        sql = 'SELECT i.image_id FROM web.entity_profile_image i WHERE i.entity_id = %(entity_id)s;'
        g.execute(sql, {'entity_id': self.id})
        return g.cursor.fetchone()[0] if g.cursor.rowcount else None

    def remove_profile_image(self) -> None:
        g.execute('DELETE FROM web.entity_profile_image WHERE entity_id = %(id)s;', {'id': self.id})

    def print_base_type(self) -> str:
        from openatlas.models.node import Node
        if not self.view_name or self.view_name == 'actor':  # actors have no base type
            return ''
        root_name = self.view_name.title()
        if self.view_name == 'reference':
            root_name = self.system_type.title()
            if root_name == 'External Reference Geonames':
                root_name = 'External Reference'
        elif self.view_name == 'file':
            root_name = 'License'
        elif self.view_name == 'place':
            root_name = self.system_type.title()
        elif self.class_.code == 'E84':
            root_name = 'Information Carrier'
        root_id = Node.get_hierarchy(root_name).id
        for node in self.nodes:
            if node.root and node.root[-1] == root_id:
                return link(node)
        return ''

    def get_name_directed(self, inverse: bool = False) -> str:
        """ Returns name part of a directed type e.g. Actor Actor Relation: Parent of (Child of)"""
        from openatlas.util.display import sanitize
        name_parts = self.name.split(' (')
        if inverse and len(name_parts) > 1:  # pragma: no cover
            return sanitize(name_parts[1], 'node')
        return name_parts[0]

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
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_menu_item(menu_item: str,
                         meta: Dict[str, Any]) -> List[Query]:  # pragma: no cover
        # Possible class names: actor, event, place, reference, source, object
        clause = ""
        parameters = {'codes': tuple(app.config['CLASS_CODES'][menu_item])}
        for filter_ in meta['filter']:
            if 'LIKE' in filter_['clause']:
                clause += ' ' + filter_['clause'] + ' LOWER(%(' + str(filter_['idx']) + ')s)'
            else:
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
