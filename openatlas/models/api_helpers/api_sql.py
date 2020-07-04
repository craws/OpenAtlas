from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
import itertools
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING, Union, ValuesView

from flask import g
from flask_login import current_user
from flask_wtf import FlaskForm
from fuzzywuzzy import fuzz
from psycopg2.extras import NamedTupleCursor
from werkzeug.exceptions import abort

from openatlas import app
from openatlas.models.date import Date
from openatlas.models.link import Link
from openatlas.util.util import is_authorized, get_file_extension

if TYPE_CHECKING:  # pragma: no cover - Type checking is disabled in tests
    from openatlas.models.node import Node


class Entity:

    def __init__(self, row: NamedTupleCursor.Record) -> None:
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
        self.location: Optional[Entity] = None  # Needed for API
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
                          nodes: bool = False) -> Optional[Entity]:
        return Link.get_linked_entity(self.id, code, inverse=inverse, nodes=nodes)

    def get_linked_entity_safe(self, code: str, inverse: bool = False,
                               nodes: bool = False) -> Entity:
        return Link.get_linked_entity_safe(self.id, code, inverse, nodes)

    def get_linked_entities(self,
                            code: Union[str, List[str]],
                            inverse: bool = False,
                            nodes: bool = False) -> List[Entity]:
        return Link.get_linked_entities(self.id, code, inverse=inverse, nodes=nodes)

    def link(self,
             code: str,
             range_: Union[Entity, List[Entity]],
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
        return Link.insert(self, code, Entity.get_by_ids(ids), description, inverse)

    def get_links(self, codes: Union[str, List[str]], inverse: bool = False) -> List[Link]:
        return Link.get_links(self.id, codes, inverse)

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
                return node.name
        return ''

    @staticmethod
    def build_sql(nodes: bool = False, aliases: bool = False) -> str:
        # Performance: only join nodes and/or aliases if requested
        sql = """
            SELECT
                e.id, e.class_code, e.name, e.description, e.created, e.modified, e.system_type,
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
    def get_by_system_type(system_type: str,
                           nodes: bool = False,
                           aliases: bool = False) -> List[Entity]:
        sql = Entity.build_sql(nodes=nodes, aliases=aliases)
        sql += ' WHERE e.system_type = %(system_type)s GROUP BY e.id;'
        g.execute(sql, {'system_type': system_type})
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_display_files() -> List[Entity]:
        g.execute(Entity.build_sql(nodes=True) + " WHERE e.system_type = 'file' GROUP BY e.id;")
        entities = []
        for row in g.cursor.fetchall():
            if get_file_extension(row.id)[1:] in app.config['DISPLAY_FILE_EXTENSIONS']:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def get_by_id(entity_id: int,
                  nodes: bool = False,
                  aliases: bool = False,
                  view_name: Optional[str] = None) -> Entity:
        from openatlas import logger
        if entity_id in g.nodes:  # pragma: no cover, just in case a node is requested
            return g.nodes[entity_id]
        sql = Entity.build_sql(nodes, aliases) + ' WHERE e.id = %(id)s GROUP BY e.id;'
        g.execute(sql, {'id': entity_id})
        entity = Entity(g.cursor.fetchone())
        if view_name and view_name != entity.view_name:  # Entity was called from wrong view, abort!
            logger.log('error', 'model', 'entity ({id}) view name="{view}", requested="{request}"'.
                       format(id=entity_id, view=entity.view_name, request=view_name))
            abort(422)
        return entity

    @staticmethod
    def get_by_ids(entity_ids: Any, nodes: bool = False) -> List[Entity]:
        if not entity_ids:
            return []
        sql = Entity.build_sql(nodes) + ' WHERE e.id IN %(ids)s GROUP BY e.id ORDER BY e.name'
        g.execute(sql, {'ids': tuple(entity_ids)})
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_project_id(project_id: int) -> List[Entity]:
        sql = """
            SELECT e.id, ie.origin_id, e.class_code, e.name, e.description, e.created, e.modified,
                e.system_type,
            array_to_json(
                array_agg((t.range_id, t.description)) FILTER (WHERE t.range_id IS NOT NULL)
            ) as nodes
            FROM model.entity e
            LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code IN ('P2', 'P89')
            JOIN import.entity ie ON e.id = ie.entity_id
            WHERE ie.project_id = %(id)s GROUP BY e.id, ie.origin_id;"""
        g.execute(sql, {'id': project_id})
        entities = []
        for row in g.cursor.fetchall():
            entity = Entity(row)
            entity.origin_id = row.origin_id
            entities.append(entity)
        return entities

    @staticmethod
    def get_by_class_code(code: Union[str, List[str]]) -> List[Entity]:
        codes = code if isinstance(code, list) else [code]
        g.execute(Entity.build_sql() + 'WHERE class_code IN %(codes)s;', {'codes': tuple(codes)})
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_menu_item(menu_item: str) -> List[Entity]:
        # Possible class names: actor, event, place, reference, source, object
        if menu_item == 'source':
            sql = Entity.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type = 'source content'
                GROUP BY e.id;"""
        elif menu_item == 'reference':
            sql = Entity.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type != 'file' GROUP BY e.id;"""
        else:
            aliases = True if menu_item == 'actor' and current_user.is_authenticated and \
                              current_user.settings['table_show_aliases'] else False
            sql = Entity.build_sql(nodes=True if menu_item == 'event' else False,
                                   aliases=aliases) + """
                WHERE e.class_code IN %(codes)s GROUP BY e.id;"""
        g.execute(sql, {'codes': tuple(app.config['CLASS_CODES'][menu_item])})
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_name_and_system_type(name: Union[str, int], system_type: str) -> Optional[Entity]:
        sql = "SELECT id FROM model.entity WHERE name = %(name)s AND system_type = %(system_type)s;"
        g.execute(sql, {'name': str(name), 'system_type': system_type})
        if g.cursor.rowcount:
            return Entity.get_by_id(g.cursor.fetchone()[0])
        return None

    @staticmethod
    def get_similar_named(form: FlaskForm) -> Dict[int, Any]:
        class_ = form.classes.data
        if class_ in ['source', 'event', 'actor']:
            entities = Entity.get_by_menu_item(class_)
        else:
            entities = Entity.get_by_system_type(class_)
        similar: Dict[int, Any] = {}
        already_added: Set[int] = set()
        for sample in entities:
            if sample.id in already_added:
                continue
            similar[sample.id] = {'entity': sample, 'entities': []}
            for entity in entities:
                if sample.id == entity.id:
                    continue
                if fuzz.ratio(sample.name, entity.name) >= form.ratio.data:
                    already_added.add(sample.id)
                    already_added.add(entity.id)
                    similar[sample.id]['entities'].append(entity)
        return {similar: data for similar, data in similar.items() if data['entities']}

    @staticmethod
    def get_overview_counts() -> Dict[str, int]:
        sql = """
            SELECT
            SUM(CASE WHEN
                class_code = 'E33' AND system_type = 'source content' THEN 1 END) AS source,
            SUM(CASE WHEN class_code IN ('E7', 'E8') THEN 1 END) AS event,
            SUM(CASE WHEN class_code IN ('E21', 'E74', 'E40') THEN 1 END) AS actor,
            SUM(CASE WHEN class_code = 'E18' THEN 1 END) AS place,
            SUM(CASE WHEN class_code IN ('E31', 'E84') AND system_type != 'file' THEN 1 END)
                AS reference,
            SUM(CASE WHEN class_code = 'E22' THEN 1 END) AS find,
            SUM(CASE WHEN system_type = 'human remains' THEN 1 END) AS "human remains",
            SUM(CASE WHEN class_code = 'E31' AND system_type = 'file' THEN 1 END) AS file
            FROM model.entity;"""
        g.execute(sql)
        row = g.cursor.fetchone()
        return {col[0]: row[idx] for idx, col in enumerate(g.cursor.description)}

    @staticmethod
    def get_orphans() -> List[Entity]:
        """ Returns entities without links. """
        g.execute(Entity.sql_orphan)
        return [Entity.get_by_id(row.id) for row in g.cursor.fetchall()]

    @staticmethod
    def get_latest(limit: int) -> List[Entity]:
        """ Returns the newest created entities"""
        codes = list(itertools.chain(*[code_ for code_ in app.config['CLASS_CODES'].values()]))
        sql = Entity.build_sql() + """
                WHERE e.class_code IN %(codes)s GROUP BY e.id
                ORDER BY e.created DESC LIMIT %(limit)s;"""
        g.execute(sql, {'codes': tuple(codes), 'limit': limit})
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_circular() -> List[Entity]:
        """ Get entities that are linked to itself."""
        g.execute('SELECT domain_id FROM model.link WHERE domain_id = range_id;')
        return [Entity.get_by_id(row.domain_id) for row in g.cursor.fetchall()]

    @staticmethod
    def get_pagination():
        sql = """SELECT e.id, e.class_code,
                    row_number() over(order by e.class_code, e.id) + 1 page_number
                FROM (SELECT me.id, me.class_code,
                        case row_number() over(order by me.id, me.class_code) % 10
                            when 0 then 1 
                            else 0
                        end page_boundary
                        from model.entity me
                         order by me.id) e
        WHERE class_code IN ('E33') AND e.page_boundary = 1;"""
        g.execute(sql)
        print(len(g.cursor.fetchall()))
        return [Entity(row[0]) for row in g.cursor.fetchall()]
