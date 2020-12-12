from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
import itertools
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING, Union, ValuesView

from flask import g, request
from flask_login import current_user
from flask_wtf import FlaskForm
from fuzzywuzzy import fuzz
from psycopg2.extras import NamedTupleCursor
from werkzeug.exceptions import abort

from openatlas import app
from openatlas.models.date import Date
from openatlas.models.link import Link
from openatlas.util.display import get_file_extension, link
from openatlas.util.util import is_authorized
from openatlas.forms.date import format_date

if TYPE_CHECKING:  # pragma: no cover - Type checking is disabled in tests
    from openatlas.models.node import Node


class Entity:

    def __init__(self, row: NamedTupleCursor.Record) -> None:

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
            self.first = format_date(self.begin_from, 'year') if self.begin_from else None
            self.last = format_date(self.end_from, 'year') if self.end_from else None
            self.last = format_date(self.end_to, 'year') if self.end_to else self.last
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

    def delete(self) -> None:
        Entity.delete_(self.id)

    def delete_links(self, codes: List[str], inverse: bool = False) -> None:
        Link.delete_by_codes(self, codes, inverse)

    def update(self, form: Optional[FlaskForm] = None) -> None:
        from openatlas.util.display import sanitize
        if form:
            self.save_nodes(form)
            for field in ['name', 'description']:
                if hasattr(form, field):
                    setattr(self, field, getattr(form, field).data)
            if hasattr(form, 'begin_year_from'):
                self.set_dates(form)
            if hasattr(form, 'alias') and (self.system_type == 'place' or
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
            Entity.delete_(id_)
        for alias in new_aliases:  # Insert new aliases if not empty
            if alias.strip() and self.class_.code == 'E18':
                self.link('P1', Entity.insert('E41', alias))
            elif alias.strip():
                self.link('P131', Entity.insert('E82', alias))

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
        if not self.view_name or self.view_name == 'actor':  # Actors have no base type
            return ''
        if self.system_type and self.system_type.startswith('external reference '):
            return ''   # e.g. "External Reference GeoNames"
        root_name = self.view_name.title()
        if self.view_name in ['reference', 'place']:
            root_name = self.system_type.title()
        elif self.view_name == 'file':
            root_name = 'License'
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
    def delete_(id_: int) -> None:
        """ Triggers psql function model.delete_entity_related() for deleting related entities."""
        if not is_authorized('contributor'):
            abort(403)  # pragma: no cover
        g.execute('DELETE FROM model.entity WHERE id = %(id_)s;', {'id_': id_})

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
            if get_file_extension(row.id) in app.config['DISPLAY_FILE_EXTENSIONS']:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def insert(code: str,
               name: str,
               system_type: Optional[str] = None,
               description: Optional[str] = None) -> Entity:
        from openatlas.util.display import sanitize
        from openatlas import logger
        if not name:  # pragma: no cover
            logger.log('error', 'database', 'Insert entity without name')
            abort(422)
        sql = """
            INSERT INTO model.entity (name, system_type, class_code, description)
            VALUES (%(name)s, %(system_type)s, %(code)s, %(description)s) RETURNING id;"""
        params = {'name': str(name).strip(),
                  'code': code,
                  'system_type': system_type.strip() if system_type else None,
                  'description': sanitize(description, 'text') if description else None}
        g.execute(sql, params)
        return Entity.get_by_id(g.cursor.fetchone()[0])

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
        try:
            entity = Entity(g.cursor.fetchone())
        except AttributeError:
            if 'activity' in request.path:
                raise AttributeError  # pragma: no cover, re-raise if user activity view
            abort(418)
            return Entity(g.cursor.fetchone())  # pragma: no cover, this line is just for type check
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
    def delete_orphans(parameter: str) -> int:
        from openatlas.models.node import Node
        class_codes = tuple(app.config['CODE_CLASS'].keys())
        if parameter == 'orphans':
            class_codes = class_codes + ('E55',)
            sql_where = Entity.sql_orphan + " AND e.class_code NOT IN %(class_codes)s"
        elif parameter == 'unlinked':
            sql_where = Entity.sql_orphan + " AND e.class_code IN %(class_codes)s"
        elif parameter == 'types':
            count = 0
            for node in Node.get_node_orphans():
                node.delete()
                count += 1
            return count
        else:
            return 0
        sql = 'DELETE FROM model.entity WHERE id IN (' + sql_where + ');'
        g.execute(sql, {'class_codes': class_codes})
        return g.cursor.rowcount

    @staticmethod
    def search(form: FlaskForm) -> ValuesView[Entity]:
        if not form.term.data:
            return {}.values()
        sql = Entity.build_sql() + """
            {user_clause} WHERE (LOWER(e.name) LIKE LOWER(%(term)s) {description_clause})
            AND {user_clause2} (""".format(
            user_clause="""
                LEFT JOIN web.user_log ul ON e.id = ul.entity_id """ if form.own.data else '',
            description_clause="""
                OR lower(e.description) LIKE lower(%(term)s) """ if form.desc.data else '',
            user_clause2=' ul.user_id = %(user_id)s AND ' if form.own.data else '')
        sql_where = []
        for name in form.classes.data:
            if name in ['source', 'event']:
                sql_where.append("e.class_code IN ({codes})".format(
                    codes=str(app.config['CLASS_CODES'][name])[1:-1]))
            elif name == 'actor':
                codes = app.config['CLASS_CODES'][name] + ['E82']  # Add alias
                sql_where.append(" e.class_code IN ({codes})".format(codes=str(codes)[1:-1]))
            elif name == 'place':
                sql_where.append("(e.class_code = 'E41' OR e.system_type = 'place')")
            elif name == 'feature':
                sql_where.append("e.system_type = 'feature'")
            elif name == 'stratigraphic unit':
                sql_where.append("e.system_type = 'stratigraphic unit'")
            elif name == 'find':
                sql_where.append("e.class_code = 'E22'")
            elif name == 'reference':
                sql_where.append(" e.class_code IN ({codes}) AND e.system_type != 'file'".format(
                    codes=str(app.config['CLASS_CODES']['reference'])[1:-1]))
            elif name == 'file':
                sql_where.append(" e.system_type = 'file'")
        sql += ' OR '.join(sql_where) + ") GROUP BY e.id ORDER BY e.name;"
        g.execute(sql, {'term': '%' + form.term.data + '%', 'user_id': current_user.id})

        # Prepare date filter
        from_date = Date.form_to_datetime64(form.begin_year.data,
                                            form.begin_month.data,
                                            form.begin_day.data)
        to_date = Date.form_to_datetime64(form.end_year.data,
                                          form.end_month.data,
                                          form.end_day.data,
                                          to_date=True)

        # Refill form in case dates were completed
        if from_date:
            string = str(from_date)
            if string.startswith('-') or string.startswith('0000'):
                string = string[1:]
            parts = string.split('-')
            form.begin_month.raw_data = None
            form.begin_day.raw_data = None
            form.begin_month.data = int(parts[1])
            form.begin_day.data = int(parts[2])

        if to_date:
            string = str(to_date)
            if string.startswith('-') or string.startswith('0000'):
                string = string[1:]  # pragma: no cover
            parts = string.split('-')
            form.end_month.raw_data = None
            form.end_day.raw_data = None
            form.end_month.data = int(parts[1])
            form.end_day.data = int(parts[2])

        entities = []
        for row in g.cursor.fetchall():
            entity = None
            if row.class_code == 'E82':  # If found in actor alias
                entity = Link.get_linked_entity(row.id, 'P131', True)
            elif row.class_code == 'E41':  # If found in place alias
                entity = Link.get_linked_entity(row.id, 'P1', True)
            elif row.class_code == 'E18':
                if row.system_type in form.classes.data:
                    entity = Entity(row)
            else:
                entity = Entity(row)

            if not entity:  # pragma: no cover
                continue

            if not from_date and not to_date:
                entities.append(entity)
                continue

            # Date criteria present but entity has no dates
            if not entity.begin_from and not entity.begin_to and not entity.end_from \
                    and not entity.end_to:
                if form.include_dateless.data:  # Include dateless entities
                    entities.append(entity)
                continue

            # Check date criteria
            dates = [entity.begin_from, entity.begin_to, entity.end_from, entity.end_to]
            begin_check_ok = False
            if not from_date:
                begin_check_ok = True  # pragma: no cover
            else:
                for date in dates:
                    if date and date >= from_date:
                        begin_check_ok = True

            end_check_ok = False
            if not to_date:
                end_check_ok = True  # pragma: no cover
            else:
                for date in dates:
                    if date and date <= to_date:
                        end_check_ok = True

            if begin_check_ok and end_check_ok:
                entities.append(entity)
        return {d.id: d for d in entities}.values()  # Remove duplicates before returning

    @staticmethod
    def set_profile_image(id_: int, origin_id: int) -> None:
        sql = """
            INSERT INTO web.entity_profile_image (entity_id, image_id)
            VALUES (%(entity_id)s, %(image_id)s)
            ON CONFLICT (entity_id) DO UPDATE SET image_id=%(image_id)s;"""
        g.execute(sql, {'entity_id': origin_id, 'image_id': id_})

    @staticmethod
    def get_circular() -> List[Entity]:
        """ Get entities that are linked to itself."""
        g.execute('SELECT domain_id FROM model.link WHERE domain_id = range_id;')
        return [Entity.get_by_id(row.domain_id) for row in g.cursor.fetchall()]
