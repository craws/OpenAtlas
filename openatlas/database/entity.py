from typing import Any, Iterable, Optional, Union

from flask import g


class Entity:

    @staticmethod
    def get_by_id(
            id_: int,
            types: bool = False,
            aliases: bool = False) -> Optional[dict[str, Any]]:
        g.cursor.execute(
            Entity.select_sql(types, aliases) +
            ' WHERE e.id = %(id)s GROUP BY e.id;',
            {'id': id_})
        return dict(g.cursor.fetchone()) if g.cursor.rowcount else None

    @staticmethod
    def get_by_ids(
            ids: Iterable[int],
            types: bool = False,
            aliases: bool = False) -> list[dict[str, Any]]:
        if not ids:
            return []
        g.cursor.execute(
            Entity.select_sql(types, aliases) +
            ' WHERE e.id IN %(ids)s GROUP BY e.id ',
            {'ids': tuple(ids)})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_link_property(code: str, class_: str) -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT
                e.id, e.cidoc_class_code, e.name, e.openatlas_class_name,
                e.description, e.created, e.modified
            FROM model.entity e
            JOIN model.link l ON e.id = l.domain_id
                AND l.property_code = %(code)s
            WHERE e.openatlas_class_name = %(class)s
            """,
            {'code': code, 'class': class_})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_project_id(project_id: int) -> list[dict[str, Any]]:
        sql = """
            SELECT
                e.id, ie.origin_id, e.cidoc_class_code, e.name, e.description,
                e.created, e.modified, e.openatlas_class_name,
                array_to_json(
                    array_agg((t.range_id, t.description))
                        FILTER (WHERE t.range_id IS NOT NULL)
                ) as types
            FROM model.entity e
            LEFT JOIN model.link t ON e.id = t.domain_id
                AND t.property_code IN ('P2', 'P89')
            JOIN import.entity ie ON e.id = ie.entity_id
            WHERE ie.project_id = %(id)s GROUP BY e.id, ie.origin_id;"""
        g.cursor.execute(sql, {'id': project_id})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_class(
            classes: Union[str, list[str]],
            types: bool = False,
            aliases: bool = False) -> list[dict[str, Any]]:
        g.cursor.execute(
            Entity.select_sql(types, aliases) +
            ' WHERE e.openatlas_class_name IN %(class)s GROUP BY e.id;',
            {'class': tuple(
                classes if isinstance(classes, list) else [classes])})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_cidoc_class(
            code: Union[str, list[str]],
            types: bool = False,
            aliases: bool = False) -> list[dict[str, Any]]:
        g.cursor.execute(
            Entity.select_sql(types, aliases) +
            'WHERE e.cidoc_class_code IN %(codes)s GROUP BY e.id;',
            {'codes': tuple(code if isinstance(code, list) else [code])})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_overview_counts(classes: list[str]) -> dict[str, int]:
        g.cursor.execute(
            """
            SELECT openatlas_class_name AS name, COUNT(openatlas_class_name)
            FROM model.entity
            WHERE openatlas_class_name IN %(classes)s
            GROUP BY openatlas_class_name;
            """,
            {'classes': tuple(classes)})
        return {
            row['name']: row['count'] for row in g.cursor.fetchall()}

    @staticmethod
    def get_orphaned_subunits() -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT e.id FROM model.entity e
            LEFT JOIN model.link l
                ON e.id = l.range_id
                AND l.property_code = 'P46'
            WHERE l.domain_id IS NULL
                AND e.openatlas_class_name
                    IN ('feature', 'stratigraphic_unit');""")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_orphans() -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT e.id FROM model.entity e
            LEFT JOIN model.link l1 ON e.id = l1.domain_id
                AND l1.range_id NOT IN
                (SELECT id FROM model.entity WHERE cidoc_class_code = 'E55')
            LEFT JOIN model.link l2 on e.id = l2.range_id
            WHERE l1.domain_id IS NULL
                AND l2.range_id IS NULL AND e.cidoc_class_code != 'E55';
            """)
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_latest(classes: list[str], limit: int) -> list[dict[str, Any]]:
        g.cursor.execute(
            f"""
            {Entity.select_sql()}
            WHERE e.openatlas_class_name IN %(codes)s GROUP BY e.id
            ORDER BY e.created DESC LIMIT %(limit)s;
            """,
            {'codes': tuple(classes), 'limit': limit})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_all_entities() -> list[dict[str, Any]]:
        g.cursor.execute(Entity.select_sql())
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_circular() -> list[dict[str, Any]]:
        g.cursor.execute(
            'SELECT domain_id FROM model.link WHERE domain_id = range_id;')
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def insert(data: dict[str, Any]) -> int:
        g.cursor.execute(
            """
            INSERT INTO model.entity
                (name, openatlas_class_name, cidoc_class_code, description)
            VALUES
                (%(name)s, %(openatlas_class_name)s, %(code)s, %(description)s)
            RETURNING id;
            """,
            data)
        return g.cursor.fetchone()['id']

    @staticmethod
    def update(data: dict[str, Any]) -> None:
        g.cursor.execute(
            """
            UPDATE model.entity SET (
                name, description, begin_from, begin_to, begin_comment,
                end_from, end_to, end_comment
            ) = (
                %(name)s, %(description)s, %(begin_from)s, %(begin_to)s,
                %(begin_comment)s, %(end_from)s, %(end_to)s, %(end_comment)s)
            WHERE id = %(id)s;
            """,
            data)

    @staticmethod
    def get_profile_image_id(id_: int) -> Optional[int]:
        g.cursor.execute(
            """
            SELECT i.image_id
            FROM web.entity_profile_image i
            WHERE i.entity_id = %(id_)s;
            """,
            {'id_': id_})
        return g.cursor.fetchone()['image_id'] if g.cursor.rowcount else None

    @staticmethod
    def set_profile_image(id_: int, origin_id: int) -> None:
        g.cursor.execute(
            """
            INSERT INTO web.entity_profile_image (entity_id, image_id)
            VALUES (%(entity_id)s, %(image_id)s)
            ON CONFLICT (entity_id) DO UPDATE SET image_id=%(image_id)s;
            """,
            {'entity_id': origin_id, 'image_id': id_})

    @staticmethod
    def remove_profile_image(id_: int) -> None:
        g.cursor.execute(
            'DELETE FROM web.entity_profile_image WHERE entity_id = %(id)s;',
            {'id': id_})

    @staticmethod
    def delete(ids: list[int]) -> None:  # Triggers psql delete_entity_related
        g.cursor.execute(
            'DELETE FROM model.entity WHERE id IN %(ids)s;',
            {'ids': tuple(ids)})

    @staticmethod
    def select_sql(types: bool = False, aliases: bool = False) -> str:
        sql = """
            SELECT
                e.id,
                e.cidoc_class_code,
                e.name,
                e.description,
                e.created,
                e.modified,
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
        if types:
            sql += """
                ,array_to_json(
                    array_agg((t.range_id, t.description))
                        FILTER (WHERE t.range_id IS NOT NULL)
                ) AS types """
        if aliases:
            sql += """
                ,array_to_json(
                    array_agg((alias.id, alias.name))
                        FILTER (WHERE alias.name IS NOT NULL)
                ) AS aliases """
        sql += " FROM model.entity e "
        if types:
            sql += """ LEFT JOIN model.link t
                ON e.id = t.domain_id AND t.property_code IN ('P2', 'P89') """
        if aliases:
            sql += """
                LEFT JOIN model.link la ON e.id = la.domain_id
                    AND la.property_code = 'P1'
                LEFT JOIN model.entity alias ON la.range_id = alias.id """
        return sql

    @staticmethod
    def search(
            term: str,
            classes: list[str],
            desc: bool = False,
            own: bool = False,
            user_id: Optional[int] = None) -> list[dict[str, Any]]:
        description_clause = """
            OR UNACCENT(lower(e.description)) LIKE UNACCENT(lower(%(term)s))
            OR UNACCENT(lower(e.begin_comment)) LIKE UNACCENT(lower(%(term)s))
            OR UNACCENT(lower(e.end_comment)) LIKE UNACCENT(lower(%(term)s))"""
        g.cursor.execute(
            f"""
            {Entity.select_sql()}
            {'LEFT JOIN web.user_log ul ON e.id = ul.entity_id' if own else ''}
            WHERE e.openatlas_class_name IN %(classes)s
                {'AND ul.user_id = %(user_id)s' if own else ''}
                AND (
                    UNACCENT(LOWER(e.name)) LIKE UNACCENT(LOWER(%(term)s))
                    {description_clause if desc else ''}
                )
            GROUP BY e.id
            ORDER BY e.name;
            """, {
                'term': f'%{term}%',
                'user_id': user_id,
                'classes': tuple(classes)})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def link(data: dict[str, Any]) -> int:
        g.cursor.execute(
            """
            INSERT INTO model.link (
                property_code,
                domain_id,
                range_id,
                description,
                type_id
            ) VALUES (
                %(property_code)s,
                %(domain_id)s,
                %(range_id)s,
                %(description)s,
                %(type_id)s)
            RETURNING id;
            """,
            data)
        return g.cursor.fetchone()['id']

    @staticmethod
    def get_subunits_without_super(classes: list[str]) -> list[int]:
        g.cursor.execute(
            """
            SELECT e.id
            FROM model.entity e
            JOIN model.link l
                ON e.id = l.range_id AND l.property_code = 'P46'
            WHERE e.openatlas_class_name IN %(classes)s;
            """,
            {'classes': tuple(classes)})
        return [row['id'] for row in g.cursor.fetchall()]

    @staticmethod
    def get_root_place(
            ids: list[int],
            property_code: Optional[str] = 'P46') -> dict[int, Any]:
        g.cursor.execute(
            """
            WITH RECURSIVE parent_tree AS (
                SELECT
                    p.parent_id,
                    p.child_id,
                    ARRAY [p.child_id] AS path,
                    1 AS depth
                FROM (
                    SELECT domain_id AS parent_id, range_id AS child_id
                    FROM model.link WHERE property_code = %(property_code)s
                ) p
                WHERE p.child_id IN %(ids)s
                UNION ALL
                SELECT
                    t.parent_id,
                    t.child_id,
                    pt.path || ARRAY [t.child_id],
                    pt.depth + 1
                FROM (
                    SELECT domain_id as parent_id, range_id as child_id
                    FROM model.link WHERE property_code = %(property_code)s
                ) t
                JOIN parent_tree pt ON pt.parent_id = t.child_id
            ),
            root_nodes AS (
                SELECT DISTINCT ON (path[1]) path[1] AS child_id,
                    parent_id AS top_level
                FROM parent_tree
                WHERE parent_id IS NOT NULL
                ORDER BY path[1], depth DESC
            )
            SELECT DISTINCT a.child_id AS start_node, r.top_level, e.name
            FROM root_nodes r
            JOIN parent_tree a ON a.child_id = r.child_id
            JOIN model.entity e ON e.id = r.top_level
            ORDER BY a.child_id
            """,
            {'ids': tuple(ids), 'property_code': property_code})
        return {
            row['start_node']: {
                'id': row['top_level'],
                'name': row['name']} for row in g.cursor.fetchall()}
