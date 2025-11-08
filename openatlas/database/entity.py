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
        GROUP BY openatlas_class_name
        ORDER BY openatlas_class_name;
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
    data['cidoc_class_code'] = \
        g.classes[data['openatlas_class_name']].cidoc_class.code
    g.cursor.execute(
        """
        INSERT INTO model.entity (
            name,
            openatlas_class_name,
            cidoc_class_code,
            description,
            begin_from,
            begin_to,
            begin_comment,
            end_from,
            end_to,
            end_comment
        ) VALUES (
            %(name)s,
            %(openatlas_class_name)s,
            %(cidoc_class_code)s,
            %(description)s,
            %(begin_from)s,
            %(begin_to)s,
            %(begin_comment)s,
            %(end_from)s,
            %(end_to)s,
            %(end_comment)s)
        RETURNING id;""",
        data)
    return g.cursor.fetchone()['id']


def update(data: dict[str, Any]) -> None:
    for item in [
            'begin_from',
            'begin_to',
            'end_from',
            'end_to',
            'begin_comment',
            'end_comment',
            'description']:
        data[item] = data.get(item)
    g.cursor.execute(
        """
        UPDATE model.entity SET (
            name,
            description,
            begin_from,
            begin_to,
            begin_comment,
            end_from,
            end_to,
            end_comment
        ) = (
            %(name)s,
            %(description)s,
            %(begin_from)s,
            %(begin_to)s,
            %(begin_comment)s,
            %(end_from)s,
            %(end_to)s,
            %(end_comment)s)
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


def delete(id_: int) -> None:  # Triggers psql delete_entity_related
    g.cursor.execute(
        'DELETE FROM model.entity WHERE id = %(id)s;',
        {'id': id_})


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


def api_search(
        classes: list[str],
        term: Optional[str]) -> list[dict[str, Any]]:
    g.cursor.execute(
        select_sql() +
        """
            WHERE e.openatlas_class_name IN %(classes)s
                AND (
                    %(term)s = '' 
                    OR UNACCENT(LOWER(e.name)) LIKE UNACCENT(LOWER(%(term)s)))
            GROUP BY e.id
            ORDER BY e.name;
        """,
        {'term': f'{term}%', 'classes': tuple(classes)})
    return list(g.cursor)


def link(data: dict[str, Any]) -> int:
    g.cursor.execute(
        """
        INSERT INTO model.link (
            property_code,
            domain_id,
            range_id,
            description,
            type_id,
            begin_from,
            begin_to,
            begin_comment,
            end_from,
            end_to,
            end_comment
        ) VALUES (
            %(property_code)s,
            %(domain_id)s,
            %(range_id)s,
            %(description)s,
            %(type_id)s,
            %(begin_from)s,
            %(begin_to)s,
            %(begin_comment)s,
            %(end_from)s,
            %(end_to)s,
            %(end_comment)s
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
        row["entity_id"]: {
            key: row[key] for key in ("public", "license_holder", "creator")}
        for row in g.cursor}


def get_entity_ids_with_links(
        property_: str,
        classes: list[str],
        inverse: bool) -> list[int]:
    g.cursor.execute(
        f"""
        SELECT e.id
        FROM model.entity e
        JOIN model.link l ON e.id = l.{'domain' if inverse else 'range'}_id
            AND l.property_code = %(property)s
        WHERE e.openatlas_class_name IN %(classes)s;
        """,
        {'property': property_, 'classes': tuple(classes)})
    return [row[0] for row in list(g.cursor)]


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
        classes: list[str] | None,
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
    if classes:
        sql += ' AND e.openatlas_class_name IN %(classes)s '
    sql += f"""
        WHERE l.{'range' if inverse else 'domain'}_id IN %(entities)s
        GROUP BY l.id, e.name
        ORDER BY e.name;"""
    g.cursor.execute(
        sql, {
            'entities': tuple(ids if isinstance(ids, list) else [ids]),
            'codes': tuple(codes) if codes else None,
            'classes': tuple(classes) if classes else None})
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


def get_linked_entities(
        id_: int,
        codes: list[str],
        classes: Optional[list[str]] = None) -> list[int]:
    if classes:
        g.cursor.execute(
            """
            SELECT e.id
            FROM model.link l
            JOIN model.entity e ON l.range_id = e.id
                AND l.domain_id = %(id_)s
                AND e.openatlas_class_name IN %(classes)s
                AND l.property_code IN %(codes)s;
            """,
            {'id_': id_, 'classes': tuple(classes), 'codes': tuple(codes)})
    else:
        g.cursor.execute(
            """
            SELECT range_id
            FROM model.link
            WHERE domain_id = %(id_)s AND property_code IN %(codes)s;
            """,
            {'id_': id_, 'codes': tuple(codes)})
    return [row[0] for row in list(g.cursor)]


def get_linked_entities_inverse(
        id_: int,
        codes: list[str],
        classes: Optional[list[str]] = None) -> list[int]:
    if classes:
        g.cursor.execute(
            """
            SELECT l.domain_id
            FROM model.link l
            JOIN model.entity e ON l.domain_id = e.id
                AND l.range_id = %(id_)s
                AND e.openatlas_class_name IN %(classes)s
                AND l.property_code IN %(codes)s;
            """,
            {'id_': id_, 'classes': tuple(classes), 'codes': tuple(codes)})
    else:
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


def delete_links_by_property_and_class(
        entity_id: int,
        property_code: str,
        classes: list[str],
        inverse: bool = False) -> None:
    g.cursor.execute(
        f"""
        DELETE FROM model.link WHERE id IN (
            SELECT l.id FROM model.link l
            JOIN model.entity e ON
                l.{'range' if inverse else 'domain'}_id = e.id
                AND l.property_code = %(property_code)s
                AND e.id = %(id)s
            JOIN model.entity e2 ON
                e2.id = l.{'domain' if inverse else 'range'}_id
                AND e2.openatlas_class_name IN %(classes)s);
        """, {
            'id': entity_id,
            'property_code': property_code,
            'classes': tuple(classes)})


def remove_types(id_: int, exclude_ids: list[int]) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link
        WHERE property_code = 'P2'
            AND domain_id = %(id)s
            AND range_id NOT IN %(exclude_ids)s;
        """,
        {'id': id_, 'exclude_ids': tuple(exclude_ids)})


def get_types(with_count: bool) -> list[dict[str, Any]]:
    sql = f"""
        SELECT
            e.id,
            e.name,
            e.cidoc_class_code,
            e.description,
            e.openatlas_class_name,
            e.created,
            e.modified,
            es.id AS super_id,
            {'COUNT(l2.id)' if with_count else '0'} AS count,
            {'COUNT(l3.id)' if with_count else '0'} AS count_property,
            COALESCE(to_char(e.begin_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS begin_from,
            COALESCE(to_char(e.begin_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS begin_to,
            COALESCE(to_char(e.end_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS end_from,
            COALESCE(to_char(e.end_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS end_to,
            e.begin_comment,
            e.end_comment,
            tns.entity_id AS non_selectable

        FROM model.entity e

        -- Selectable or not
        LEFT OUTER JOIN web.type_none_selectable tns ON e.id = tns.entity_id

        -- Get super
        LEFT JOIN model.link l ON e.id = l.domain_id
            AND l.property_code IN ('P127', 'P89')
        LEFT JOIN model.entity es ON l.range_id = es.id
        """
    if with_count:
        sql += """
            -- Get count
            LEFT JOIN model.link l2 ON e.id = l2.range_id
                AND l2.property_code IN ('P2', 'P89')
            LEFT JOIN model.link l3 ON e.id = l3.type_id
            """
    sql += """
        WHERE e.openatlas_class_name
            IN ('administrative_unit', 'type', 'type_tools')
        GROUP BY e.id, es.id, tns.entity_id
        ORDER BY e.name;
        """
    g.cursor.execute(sql)
    return list(g.cursor)


def get_hierarchies() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id, name, category, multiple, directional, required
        FROM web.hierarchy;
        """)
    return list(g.cursor)


def set_required(id_: int) -> None:
    g.cursor.execute(
        "UPDATE web.hierarchy SET required = true WHERE id = %(id)s;",
        {'id': id_})


def unset_required(id_: int) -> None:
    g.cursor.execute(
        "UPDATE web.hierarchy SET required = false WHERE id = %(id)s;",
        {'id': id_})


def set_selectable(id_: int) -> None:
    g.cursor.execute(
        "DELETE FROM web.type_none_selectable WHERE entity_id = %(id)s;",
        {'id': id_})


def unset_selectable(id_: int) -> None:
    g.cursor.execute(
        "INSERT INTO web.type_none_selectable (entity_id) VALUES (%(id)s)",
        {'id': id_})


def insert_hierarchy(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.hierarchy (id, name, multiple, category)
        VALUES (%(id)s, %(name)s, %(multiple)s, %(category)s);
        """,
        data)


def update_hierarchy(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE web.hierarchy
        SET name = %(name)s, multiple = %(multiple)s
        WHERE id = %(id)s;
        """,
        data)


def add_classes_to_hierarchy(type_id: int, class_names: list[str]) -> None:
    for class_name in class_names:
        g.cursor.execute(
            """
            INSERT INTO web.hierarchy_openatlas_class
                (hierarchy_id, openatlas_class_name)
            VALUES (%(type_id)s, %(class_name)s);
            """,
            {'type_id': type_id, 'class_name': class_name})


def move_link_type(data: dict[str, int]) -> None:
    g.cursor.execute(
        """
        UPDATE model.link
        SET type_id = %(new_type_id)s
        WHERE type_id = %(old_type_id)s AND id IN %(entity_ids)s;
        """,
        data)


def move_entity_type(data: dict[str, int]) -> None:
    g.cursor.execute(
        """
        UPDATE model.link
        SET range_id = %(new_type_id)s
        WHERE range_id = %(old_type_id)s AND domain_id IN %(entity_ids)s;
        """,
        data)


def remove_link_type(type_id: int, delete_ids: list[int]) -> None:
    g.cursor.execute(
        """
        UPDATE model.link
        SET type_id = NULL
        WHERE type_id = %(type_id)s AND id IN %(delete_ids)s;
        """,
        {'type_id': type_id, 'delete_ids': tuple(delete_ids)})


def remove_entity_type(type_id: int, delete_ids: list[int]) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link
        WHERE range_id = %(type_id)s AND domain_id IN %(delete_ids)s;
        """,
        {'type_id': type_id, 'delete_ids': tuple(delete_ids)})


def get_class_count(name: str, type_ids: list[int]) -> int:
    g.cursor.execute(
        """
        SELECT COUNT(*) FROM model.link l
        JOIN model.entity e ON l.domain_id = e.id
            AND l.range_id IN %(type_ids)s
        WHERE l.property_code = 'P2'
            AND e.openatlas_class_name = %(class_name)s;
        """,
        {'type_ids': tuple(type_ids), 'class_name': name})
    return g.cursor.fetchone()['count']


def remove_class(hierarchy_id: int, class_name: str) -> None:
    g.cursor.execute(
        """
        DELETE FROM web.hierarchy_openatlas_class
        WHERE hierarchy_id = %(hierarchy_id)s
            AND openatlas_class_name = %(class_name)s;
        """,
        {'hierarchy_id': hierarchy_id, 'class_name': class_name})


def remove_entity_links(type_id: int, entity_id: int) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link
        WHERE domain_id = %(entity_id)s
            AND range_id = %(type_id)s
            AND property_code = 'P2';
        """,
        {'entity_id': entity_id, 'type_id': type_id})


def insert_reference_system(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.reference_system (
            entity_id,
            name,
            website_url,
            resolver_url,
            identifier_example)
        VALUES (
            %(entity_id)s,
            %(name)s,
            %(website_url)s,
            %(resolver_url)s,
            %(identifier_example)s);
        """,
        data)


def update_reference_system(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE web.reference_system
        SET (
            name,
            website_url,
            resolver_url,
            identifier_example
        ) = (
            %(name)s,
            %(website_url)s,
            %(resolver_url)s,
            %(identifier_example)s
        ) WHERE entity_id = %(entity_id)s;
        """,
        data)


def add_reference_system_classes(entity_id: int, names: list[str]) -> None:
    for name in names:
        g.cursor.execute(
            """
            INSERT INTO web.reference_system_openatlas_class (
                reference_system_id, openatlas_class_name
            ) VALUES (%(entity_id)s, %(name)s);
            """,
            {'entity_id': entity_id, 'name': name})


def remove_reference_system_class(entity_id: int, name: str) -> None:
    g.cursor.execute(
        """
        DELETE FROM web.reference_system_openatlas_class
        WHERE reference_system_id = %(reference_system_id)s
            AND openatlas_class_name = %(class_name)s;
        """,
        {'reference_system_id': entity_id, 'class_name': name})


def reference_system_counts() -> dict[str, int]:
    g.cursor.execute(
        """
        SELECT e.id, COUNT(l.id) AS count
        FROM model.entity e
        LEFT JOIN model.link l ON e.id = l.domain_id
            AND l.property_code = 'P67'
        GROUP BY e.id;
        """)
    return {row['id']: row['count'] for row in list(g.cursor)}


def get_reference_systems() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            e.id,
            e.name,
            e.cidoc_class_code,
            e.description,
            e.openatlas_class_name,
            e.created,
            e.modified,
            rs.website_url,
            rs.resolver_url,
            rs.identifier_example,
            rs.system,
            array_to_json(
                array_agg((t.range_id, t.description))
                    FILTER (WHERE t.range_id IS NOT NULL)
            ) AS types
        FROM model.entity e
        JOIN web.reference_system rs ON e.id = rs.entity_id
        LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code = 'P2'
        GROUP BY
            e.id,
            e.name,
            e.cidoc_class_code,
            e.description,
            e.openatlas_class_name,
            e.created,
            e.modified,
            rs.website_url,
            rs.resolver_url,
            rs.identifier_example,
            rs.system,
            rs.entity_id;
        """)
    return list(g.cursor)
