# Created by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict
from typing import Iterator, Set, Union, Optional, Dict

from flask import g
from flask_login import current_user
from werkzeug.exceptions import abort

from openatlas import app, debug_model, logger
from openatlas.forms.date import DateForm
from openatlas.models.date import DateMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import print_file_extension, uc_first


class Entity:
    def __init__(self, row) -> None:
        if not row:
            logger.log('error', 'model', 'invalid id')
            abort(418)
        self.id = row.id
        self.nodes = {}  # type: Dict
        if hasattr(row, 'nodes') and row.nodes:
            for node in row.nodes:
                self.nodes[g.nodes[node['f1']]] = node['f2']  # f1 = node id, f2 = value
        self.aliases = {}  # type: Dict
        if hasattr(row, 'aliases') and row.aliases:
            for alias in row.aliases:
                self.aliases[alias['f1']] = alias['f2']  # f1 = alias id, f2 = alias name
            self.aliases = OrderedDict(sorted(self.aliases.items(), key=lambda kv: (kv[1], kv[0])))
        self.name = row.name
        self.root = None  # type: Optional[list]
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
        self.origin_id = None  # type: Optional[int]
        if hasattr(row, 'begin_from'):
            self.begin_from = DateMapper.timestamp_to_datetime64(row.begin_from)
            self.begin_to = DateMapper.timestamp_to_datetime64(row.begin_to)
            self.begin_comment = row.begin_comment
            self.end_from = DateMapper.timestamp_to_datetime64(row.end_from)
            self.end_to = DateMapper.timestamp_to_datetime64(row.end_to)
            self.end_comment = row.end_comment
            self.first = DateForm.format_date(self.begin_from, 'year') if self.begin_from else None
            self.last = DateForm.format_date(self.end_from, 'year') if self.end_from else None
            self.last = DateForm.format_date(self.end_to, 'year') if self.end_to else self.last
        self.class_ = g.classes[row.class_code]
        self.view_name = None  # view_name is used to build urls
        self.external_references = []  # type: list
        if self.system_type == 'file':
            self.view_name = 'file'
        elif self.class_.code in app.config['CODE_CLASS']:
            self.view_name = app.config['CODE_CLASS'][self.class_.code]
        self.table_name = self.view_name  # table_name is used to build tables
        if self.view_name == 'place':
            self.table_name = self.system_type.replace(' ', '-')

    def get_linked_entity(self, code,
                          inverse: Optional[bool] = False,
                          nodes: Optional[bool] = False):
        return LinkMapper.get_linked_entity(self, code, inverse=inverse, nodes=nodes)

    def get_linked_entities(self, code,
                            inverse: Optional[bool] = False,
                            nodes: Optional[bool] = False):
        return LinkMapper.get_linked_entities(self, code, inverse=inverse, nodes=nodes)

    def link(self, code, range_, description: Optional[str] = None,
             inverse: Optional[bool] = False):
        return LinkMapper.insert(self, code, range_, description, inverse)

    def get_links(self, code, inverse: Optional[bool] = False):
        return LinkMapper.get_links(self, code, inverse)

    def delete(self) -> None:
        EntityMapper.delete(self.id)

    def delete_links(self, codes) -> None:
        LinkMapper.delete_by_codes(self, codes)

    def update(self):
        EntityMapper.update(self)

    def update_aliases(self, form):
        old_aliases = self.aliases
        new_aliases = form.alias.data
        delete_ids = []
        for id_, alias in old_aliases.items():  # Compare old aliases with form values
            if alias in new_aliases:
                new_aliases.remove(alias)
            else:
                delete_ids.append(id_)
        for id_ in delete_ids:  # Delete obsolete aliases
            EntityMapper.delete(id_)
        for alias in new_aliases:  # Insert new aliases if not empty
            if alias.strip() and self.class_.code == 'E18':
                self.link('P1', EntityMapper.insert('E41', alias))
            elif alias.strip():
                self.link('P131', EntityMapper.insert('E82', alias))

    def save_nodes(self, form):
        from openatlas.models.node import NodeMapper
        NodeMapper.save_entity_nodes(self, form)

    def set_dates(self, form):
        self.begin_from = None
        self.begin_to = None
        self.begin_comment = None
        self.end_from = None
        self.end_to = None
        self.end_comment = None
        if form.begin_year_from.data:  # Only if begin year is set create a begin date or time span
            self.begin_comment = form.begin_comment.data
            self.begin_from = DateMapper.form_to_datetime64(
                form.begin_year_from.data, form.begin_month_from.data, form.begin_day_from.data)
            self.begin_to = DateMapper.form_to_datetime64(
                form.begin_year_to.data, form.begin_month_to.data, form.begin_day_to.data, True)

        if form.end_year_from.data:  # Only if end year is set create a year date or time span
            self.end_comment = form.end_comment.data
            self.end_from = DateMapper.form_to_datetime64(
                form.end_year_from.data, form.end_month_from.data, form.end_day_from.data)
            self.end_to = DateMapper.form_to_datetime64(
                form.end_year_to.data, form.end_month_to.data, form.end_day_to.data, True)

    def get_profile_image_id(self):
        return EntityMapper.get_profile_image_id(self.id)

    def remove_profile_image(self):
        return EntityMapper.remove_profile_image(self.id)

    def print_base_type(self):
        from openatlas.models.node import NodeMapper
        if not self.view_name or self.view_name == 'actor':  # actors have no base type
            return ''
        root_name = self.view_name.title()
        if self.view_name == 'reference':
            root_name = self.system_type.title()
        elif self.view_name == 'file':
            root_name = 'License'
        elif self.view_name == 'place':
            root_name = uc_first(self.system_type)
            if self.system_type == 'stratigraphic unit':
                root_name = 'Stratigraphic Unit'
        root_id = NodeMapper.get_hierarchy_by_name(root_name).id
        for node in self.nodes:
            if node.root and node.root[-1] == root_id:
                return node.name
        return ''

    def get_name_directed(self, inverse=False):
        """ Returns name part of a directed type e.g. Actor Actor Relation: Parent of (Child of)"""
        from openatlas.util.util import sanitize
        name_parts = self.name.split(' (')
        if inverse and len(name_parts) > 1:  # pragma: no cover
            return sanitize(name_parts[1], 'node')
        return name_parts[0]


class EntityMapper:
    sql_orphan = """
        SELECT e.id FROM model.entity e
        LEFT JOIN model.link l1 on e.id = l1.domain_id AND l1.range_id NOT IN
            (SELECT id FROM model.entity WHERE class_code = 'E55')
        LEFT JOIN model.link l2 on e.id = l2.range_id
        WHERE l1.domain_id IS NULL AND l2.range_id IS NULL AND e.class_code != 'E55'"""

    @staticmethod
    def build_sql(nodes=False, aliases=False):
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
    def update(entity: Entity) -> None:
        from openatlas.util.util import sanitize
        sql = """
            UPDATE model.entity SET
            (name, description, begin_from, begin_to, begin_comment, end_from, end_to, end_comment) 
                = (%(name)s, %(description)s, %(begin_from)s, %(begin_to)s, %(begin_comment)s, 
                %(end_from)s, %(end_to)s, %(end_comment)s)
            WHERE id = %(id)s;"""
        g.cursor.execute(sql, {
            'id': entity.id, 'name': entity.name,
            'begin_from': DateMapper.datetime64_to_timestamp(entity.begin_from),
            'begin_to': DateMapper.datetime64_to_timestamp(entity.begin_to),
            'end_from': DateMapper.datetime64_to_timestamp(entity.end_from),
            'end_to': DateMapper.datetime64_to_timestamp(entity.end_to),
            'begin_comment': entity.begin_comment, 'end_comment': entity.end_comment,
            'description': sanitize(entity.description, 'description')})
        debug_model['div sql'] += 1

    @staticmethod
    def get_by_system_type(system_type, nodes=False, aliases=False):
        sql = EntityMapper.build_sql(nodes=nodes, aliases=aliases)
        sql += ' WHERE e.system_type = %(system_type)s GROUP BY e.id ORDER BY e.name;'
        g.cursor.execute(sql, {'system_type': system_type})
        debug_model['div sql'] += 1
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_display_files():
        sql_clause = " WHERE e.system_type = 'file' GROUP BY e.id ORDER BY e.name;"
        g.cursor.execute(EntityMapper.build_sql(nodes=True) + sql_clause)
        debug_model['div sql'] += 1
        entities = []
        for row in g.cursor.fetchall():
            if print_file_extension(row.id)[1:] in app.config['DISPLAY_FILE_EXTENSIONS']:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def insert(code, name, system_type=None, description=None):
        if not name:  # pragma: no cover
            logger.log('error', 'database', 'Insert entity without name and date')
            return
        sql = """
            INSERT INTO model.entity (name, system_type, class_code, description)
            VALUES (%(name)s, %(system_type)s, %(code)s, %(description)s)
            RETURNING id;"""
        params = {'name': name.strip(), 'code': code,
                  'system_type': system_type.strip() if system_type else None,
                  'description': description.strip() if description else None}
        g.cursor.execute(sql, params)
        debug_model['div sql'] += 1
        return EntityMapper.get_by_id(g.cursor.fetchone()[0])

    @staticmethod
    def get_by_id(entity_id: int, nodes=False, aliases=False, ignore_not_found=False):
        if entity_id in g.nodes:  # pragma: no cover, just in case a node is requested
            return g.nodes[entity_id]
        sql = EntityMapper.build_sql(nodes, aliases) + ' WHERE e.id = %(id)s GROUP BY e.id;'
        g.cursor.execute(sql, {'id': entity_id})
        debug_model['by id'] += 1
        if g.cursor.rowcount < 1 and ignore_not_found:
            return None  # pragma: no cover, only used where expected to avoid a 418 e.g. at logs
        return Entity(g.cursor.fetchone())

    @staticmethod
    def get_by_ids(entity_ids: Union[Iterator, Set], nodes=False) -> list:
        if not entity_ids:
            return []
        sql = EntityMapper.build_sql(nodes) + ' WHERE e.id IN %(ids)s GROUP BY e.id;'
        g.cursor.execute(sql, {'ids': tuple(entity_ids)})
        debug_model['by id'] += 1
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_project_id(project_id: int) -> list:
        sql = """
            SELECT e.id, ie.origin_id, e.class_code, e.name, e.description, e.created, e.modified,
                e.system_type,
            array_to_json(
                array_agg((t.range_id, t.description)) FILTER (WHERE t.range_id IS NOT NULL)
            ) as nodes
            FROM model.entity e
            LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code IN ('P2', 'P89')
            JOIN import.entity ie ON e.id = ie.entity_id
            WHERE ie.project_id = %(id)s GROUP BY e.id, ie.origin_id ORDER BY e.name;"""
        g.cursor.execute(sql, {'id': project_id})
        debug_model['by id'] += 1
        entities = []
        for row in g.cursor.fetchall():
            entity = Entity(row)
            entity.origin_id = row.origin_id
            entities.append(entity)
        return entities

    @staticmethod
    def get_by_codes(class_name: str) -> list:
        # Possible class names: actor, event, place, reference, source
        if class_name == 'source':
            sql = EntityMapper.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type = 'source content'
                GROUP BY e.id ORDER BY e.name;"""
        elif class_name == 'reference':
            sql = EntityMapper.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type != 'file'
                GROUP BY e.id ORDER BY e.name;"""
        else:
            aliases = True if class_name == 'actor' and current_user.settings[
                'table_show_aliases'] else False
            sql = EntityMapper.build_sql(nodes=True if class_name == 'event' else False,
                                         aliases=aliases) + """
                WHERE e.class_code IN %(codes)s GROUP BY e.id ORDER BY e.name;"""
        g.cursor.execute(sql, {'codes': tuple(app.config['CLASS_CODES'][class_name])})
        debug_model['by codes'] += 1
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def delete(entity) -> None:
        """ Triggers function model.delete_entity_related() for deleting related entities"""
        id_ = entity if type(entity) is int else entity.id
        g.cursor.execute('DELETE FROM model.entity WHERE id = %(id_)s;', {'id_': id_})
        debug_model['by id'] += 1

    @staticmethod
    def get_overview_counts() -> OrderedDict:
        sql = """
            SELECT
            SUM(CASE WHEN
                class_code = 'E33' AND system_type = 'source content' THEN 1 END) AS source,
            SUM(CASE WHEN class_code IN ('E6', 'E7', 'E8', 'E12') THEN 1 END) AS event,
            SUM(CASE WHEN class_code IN ('E21', 'E74', 'E40') THEN 1 END) AS actor,
            SUM(CASE WHEN class_code = 'E18' THEN 1 END) AS place,
            SUM(CASE WHEN class_code IN ('E31', 'E84') AND system_type != 'file' THEN 1 END)
                AS reference,
            SUM(CASE WHEN class_code = 'E31' AND system_type = 'file' THEN 1 END) AS file
            FROM model.entity;"""
        g.cursor.execute(sql)
        debug_model['div sql'] += 1
        row = g.cursor.fetchone()
        counts = OrderedDict()  # type: OrderedDict
        for idx, col in enumerate(g.cursor.description):
            counts[col[0]] = row[idx]
        return counts

    @staticmethod
    def get_orphans() -> list:
        """ Returns entities without links. """
        g.cursor.execute(EntityMapper.sql_orphan)
        debug_model['div sql'] += 1
        return [EntityMapper.get_by_id(row.id) for row in g.cursor.fetchall()]

    @staticmethod
    def get_latest(limit: int) -> list:
        """ Returns the newest created entities"""
        codes = []  # type: list
        for class_codes in app.config['CLASS_CODES'].values():
            codes += class_codes
        sql = EntityMapper.build_sql() + """
                WHERE e.class_code IN %(codes)s GROUP BY e.id
                ORDER BY e.created DESC LIMIT %(limit)s;"""
        g.cursor.execute(sql, {'codes': tuple(codes), 'limit': limit})
        debug_model['div sql'] += 1
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def delete_orphans(parameter) -> int:
        from openatlas.models.node import NodeMapper
        class_codes = tuple(app.config['CODE_CLASS'].keys())
        if parameter == 'orphans':
            class_codes = class_codes + ('E55',)
            sql_where = EntityMapper.sql_orphan + " AND e.class_code NOT IN %(class_codes)s"
        elif parameter == 'unlinked':
            sql_where = EntityMapper.sql_orphan + " AND e.class_code IN %(class_codes)s"
        elif parameter == 'types':
            count = 0
            for node in NodeMapper.get_orphans():
                EntityMapper.delete(node)
                count += 1
            return count
        else:
            return 0
        sql = 'DELETE FROM model.entity WHERE id IN (' + sql_where + ');'
        g.cursor.execute(sql, {'class_codes': class_codes})
        debug_model['div sql'] += 1
        return g.cursor.rowcount

    @staticmethod
    def search(form):
        if not form.term.data:
            return []
        sql = EntityMapper.build_sql() + """
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
        g.cursor.execute(sql, {'term': '%' + form.term.data + '%', 'user_id': current_user.id})
        debug_model['div sql'] += 1

        # Prepare date filter
        from_date = DateMapper.form_to_datetime64(form.begin_year.data, form.begin_month.data,
                                                  form.begin_day.data)
        to_date = DateMapper.form_to_datetime64(form.end_year.data, form.end_month.data,
                                                form.end_day.data, True)

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
                entity = LinkMapper.get_linked_entity(row.id, 'P131', True)
            elif row.class_code == 'E41':  # If found in place alias
                entity = LinkMapper.get_linked_entity(row.id, 'P1', True)
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
        g.cursor.execute(sql, {'entity_id': origin_id, 'image_id': id_})
        debug_model['div sql'] += 1

    @staticmethod
    def get_profile_image_id(id_: int):
        sql = 'SELECT image_id FROM web.entity_profile_image WHERE entity_id = %(entity_id)s;'
        g.cursor.execute(sql, {'entity_id': id_})
        debug_model['div sql'] += 1
        return g.cursor.fetchone()[0] if g.cursor.rowcount else None

    @staticmethod
    def remove_profile_image(entity_id: int) -> None:
        sql = 'DELETE FROM web.entity_profile_image WHERE entity_id = %(entity_id)s;'
        g.cursor.execute(sql, {'entity_id': entity_id})
        debug_model['div sql'] += 1

    @staticmethod
    def get_circular() -> list:
        # Get entities that are linked to itself
        g.cursor.execute('SELECT domain_id FROM model.link WHERE domain_id = range_id;')
        debug_model['div sql'] += 1
        return [EntityMapper.get_by_id(row.domain_id) for row in g.cursor.fetchall()]
