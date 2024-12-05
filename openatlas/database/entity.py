from typing import Any, Iterable, Optional

from flask import g


def get_by_id(
        id_: int,
        types: bool = False,
        aliases: bool = False) -> dict[str, Any]:
    g.cursor.execute(
        select_sql(types, aliases) + ' WHERE e.id = %(id)s GROUP BY e.id;',
        {'id': id_})
    return g.cursor.fetchone()


def get_by_ids(
        ids: Iterable[int],
        types: bool = False,
        aliases: bool = False) -> list[dict[str, Any]]:
    if not ids:
        return []
    g.cursor.execute(
        select_sql(types, aliases) + ' WHERE e.id IN %(ids)s GROUP BY e.id ',
        {'ids': tuple(ids)})
    return list(g.cursor)


def get_by_project_id(project_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            e.id,
            ie.origin_id,
            e.cidoc_class_code,
            e.name,
            e.description,
            e.created,
            e.modified,
            e.openatlas_class_name,
            array_to_json(
                array_agg((t.range_id, t.description))
                    FILTER (WHERE t.range_id IS NOT NULL)
            ) AS types
        FROM model.entity e
        LEFT JOIN model.link t ON e.id = t.domain_id
            AND t.property_code IN ('P2', 'P89')
        JOIN import.entity ie ON e.id = ie.entity_id
        WHERE ie.project_id = %(id)s
        GROUP BY e.id, ie.origin_id;
        """,
        {'id': project_id})
    return list(g.cursor)


def get_by_class(
        classes: str | list[str],
        types: bool = False,
        aliases: bool = False) -> list[dict[str, Any]]:
    g.cursor.execute(
        select_sql(types, aliases) +
        ' WHERE e.openatlas_class_name IN %(class)s GROUP BY e.id;',
        {'class': tuple(classes if isinstance(classes, list) else [classes])})
    return list(g.cursor)


def get_by_cidoc_class(
        code: str | list[str],
        types: bool = False,
        aliases: bool = False) -> list[dict[str, Any]]:
    g.cursor.execute(
        select_sql(types, aliases) +
        'WHERE e.cidoc_class_code IN %(codes)s GROUP BY e.id;',
        {'codes': tuple(code if isinstance(code, list) else [code])})
    return list(g.cursor)


def get_overview_counts(classes: list[str]) -> dict[str, int]:
    g.cursor.execute(
        """
        SELECT openatlas_class_name AS name, COUNT(openatlas_class_name)
        FROM model.entity
        WHERE openatlas_class_name IN %(classes)s
        GROUP BY openatlas_class_name;
        """,
        {'classes': tuple(classes)})
    return {row['name']: row['count'] for row in list(g.cursor)}


def get_overview_counts_by_type(
        ids: list[int],
        classes: list[str]) -> dict[str, int]:
    g.cursor.execute(
        """
        SELECT openatlas_class_name AS name, COUNT(openatlas_class_name)
        FROM model.entity e
        JOIN model.link t ON e.id = t.domain_id
        WHERE openatlas_class_name IN %(classes)s AND t.range_id IN %(ids)s  
        GROUP BY openatlas_class_name;
        """,
        {'ids': tuple(ids), 'classes': tuple(classes)})
    return {row['name']: row['count'] for row in list(g.cursor)}


def get_latest(classes: list[str], limit: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        select_sql() +
        """
        WHERE e.openatlas_class_name IN %(codes)s
        GROUP BY e.id
        ORDER BY e.created
        DESC LIMIT %(limit)s;
        """,
        {'codes': tuple(classes), 'limit': limit})
    return list(g.cursor)


def get_all_entities() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            e.id,
            e.cidoc_class_code,
            e.name,
            e.description,
            COALESCE(to_char(e.created, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS created,
            COALESCE(to_char(e.modified, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS modified,
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
                AS end_to
        FROM model.entity e;
        """)
    return list(g.cursor)


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


def get_profile_image_id(id_: int) -> Optional[int]:
    g.cursor.execute(
        """
        SELECT i.image_id
        FROM web.entity_profile_image i
        WHERE i.entity_id = %(id_)s;
        """,
        {'id_': id_})
    return g.cursor.fetchone()['image_id'] if g.cursor.rowcount else None


def set_profile_image(id_: int, origin_id: int) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.entity_profile_image (entity_id, image_id)
        VALUES (%(entity_id)s, %(image_id)s)
        ON CONFLICT (entity_id) DO UPDATE SET image_id=%(image_id)s;
        """,
        {'entity_id': origin_id, 'image_id': id_})


def remove_profile_image(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM web.entity_profile_image WHERE entity_id = %(id)s;',
        {'id': id_})


def delete(ids: list[int]) -> None:  # Triggers psql delete_entity_related
    g.cursor.execute(
        'DELETE FROM model.entity WHERE id IN %(ids)s;',
        {'ids': tuple(ids)})


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
    sql += ' FROM model.entity e '
    if types:
        sql += """ LEFT JOIN model.link t
            ON e.id = t.domain_id AND t.property_code IN ('P2', 'P89') """
    if aliases:
        sql += """
            LEFT JOIN model.link la ON e.id = la.domain_id
                AND la.property_code = 'P1'
            LEFT JOIN model.entity alias ON la.range_id = alias.id """
    return sql


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
        select_sql() +
        f"""
        {'LEFT JOIN web.user_log ul ON e.id = ul.entity_id' if own else ''}
        WHERE e.openatlas_class_name IN %(classes)s
            {'AND ul.user_id = %(user_id)s' if own else ''}
            AND (
                UNACCENT(LOWER(e.name)) LIKE UNACCENT(LOWER(%(term)s))
                {description_clause if desc else ''})
        GROUP BY e.id
        ORDER BY e.name;
        """,
        {'term': f'%{term}%', 'user_id': user_id, 'classes': tuple(classes)})
    return list(g.cursor)


def link(data: dict[str, Any]) -> int:
    g.cursor.execute(
        """
        INSERT INTO model.link (
            property_code, domain_id, range_id, description, type_id
        ) VALUES (
            %(property_code)s, %(domain_id)s, %(range_id)s, %(description)s,
            %(type_id)s
        ) RETURNING id;
        """,
        data)
    return g.cursor.fetchone()['id']


def update_file_info(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO model.file_info (
            entity_id,
            public,
            creator,
            license_holder
        ) VALUES (
            %(entity_id)s,
            %(public)s,
            %(creator)s,
            %(license_holder)s
        ) ON CONFLICT (entity_id) DO UPDATE SET
            public = %(public)s,
            creator = %(creator)s,
            license_holder = %(license_holder)s;
        """,
        data)


def get_file_info() -> dict[int, dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT entity_id, public, creator, license_holder
        FROM model.file_info;
        """)
    return {
        row['entity_id']: {
            'public': row['public'],
            'license_holder': row['license_holder'],
            'creator': row['creator']} for row in list(g.cursor)}


def get_subunits_without_super(classes: list[str]) -> list[int]:
    g.cursor.execute(
        """
        SELECT e.id
        FROM model.entity e
        JOIN model.link l ON e.id = l.range_id AND l.property_code = 'P46'
        WHERE e.openatlas_class_name IN %(classes)s;
        """,
        {'classes': tuple(classes)})
    return [row[0] for row in list(g.cursor)]


def get_roots(
        property_code: str,
        ids: list[int],
        inverse: bool = False) -> dict[int, Any]:
    first = 'domain_id' if inverse else 'range_id'
    second = 'range_id' if inverse else 'domain_id'
    g.cursor.execute(
        f"""
        WITH RECURSIVE parent_tree AS (
            SELECT
                p.parent_id,
                p.child_id,
                ARRAY [p.child_id] AS path,
                1 AS depth
            FROM (
                SELECT {first} AS parent_id, {second} AS child_id
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
                SELECT {first} AS parent_id, {second} AS child_id
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
        ORDER BY a.child_id;
        """,
        {'ids': tuple(ids), 'property_code': property_code})
    return {
        row['start_node']: {
            'id': row['top_level'],
            'name': row['name']} for row in list(g.cursor)}


def get_linked_entities_recursive(
        id_: int,
        codes: list[str] | str,
        inverse: bool) -> list[int]:
    first = 'domain_id' if inverse else 'range_id'
    second = 'range_id' if inverse else 'domain_id'
    codes = codes if isinstance(codes, list) else [codes]
    g.cursor.execute(
        f"""
        WITH RECURSIVE items AS (
            SELECT {first}
            FROM model.link
            WHERE {second} = %(id_)s AND property_code IN %(code)s
            UNION
                SELECT l.{first} FROM model.link l
                INNER JOIN items i ON
                    l.{second} = i.{first}
                    AND l.property_code IN %(code)s
            ) SELECT {first} FROM items;
        """,
        {'id_': id_, 'code': tuple(codes) if codes else ''})
    return [row[0] for row in list(g.cursor)]


def get_links_of_entities(
        ids: int | list[int],
        codes: str | list[str] | None,
        inverse: bool = False) -> list[dict[str, Any]]:
    sql = f"""
        SELECT
            l.id, l.property_code,
            l.domain_id,
            l.range_id,
            l.description,
            l.created,
            l.modified,
            e.name,
            l.type_id,
            COALESCE(to_char(l.begin_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS begin_from, l.begin_comment,
            COALESCE(to_char(l.begin_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS begin_to,
            COALESCE(to_char(l.end_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS end_from, l.end_comment,
            COALESCE(to_char(l.end_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS end_to
        FROM model.link l
        JOIN model.entity e
            ON l.{'domain' if inverse else 'range'}_id = e.id """
    if codes:
        codes = codes if isinstance(codes, list) else [codes]
        sql += ' AND l.property_code IN %(codes)s '
    sql += f"""
        WHERE l.{'range' if inverse else 'domain'}_id IN %(entities)s
        GROUP BY l.id, e.name
        ORDER BY e.name;"""
    g.cursor.execute(
        sql, {
            'entities': tuple(ids if isinstance(ids, list) else [ids]),
            'codes': tuple(codes) if codes else ''})
    return list(g.cursor)


def delete_reference_system_links(entity_id: int) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link l
        WHERE property_code = 'P67'
            AND domain_id IN %(systems_ids)s
            AND range_id = %(entity_id)s;
        """, {
            'systems_ids': tuple(g.reference_systems.keys()),
            'entity_id': entity_id})


def get_linked_entities(id_: int, codes: list[str]) -> list[int]:
    g.cursor.execute(
        """
        SELECT range_id
        FROM model.link
        WHERE domain_id = %(id_)s AND property_code IN %(codes)s;
        """,
        {'id_': id_, 'codes': tuple(codes)})
    return [row[0] for row in list(g.cursor)]


def get_linked_entities_inverse(id_: int, codes: list[str]) -> list[int]:
    g.cursor.execute(
        """
        SELECT domain_id
        FROM model.link
        WHERE range_id = %(id_)s AND property_code IN %(codes)s;
        """,
        {'id_': id_, 'codes': tuple(codes)})
    return [row[0] for row in list(g.cursor)]


def delete_links_by_codes(
        entity_id: int,
        codes: list[str], inverse: bool = False) -> None:
    g.cursor.execute(
        f"""
        DELETE FROM model.link
        WHERE property_code IN %(codes)s
            AND {'range_id' if inverse else 'domain_id'} = %(id)s;
        """,
        {'id': entity_id, 'codes': tuple(codes)})


def remove_types(id_: int, exclude_ids: list[int]) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link
        WHERE property_code = 'P2'
            AND domain_id = %(id)s
            AND range_id NOT IN %(exclude_ids)s;
        """,
        {'id': id_, 'exclude_ids': tuple(exclude_ids)})
