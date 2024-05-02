from typing import Any

from flask import g


def update(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE model.link SET (
            property_code,
            domain_id,
            range_id,
            description,
            type_id,
            begin_from, begin_to, begin_comment,
            end_from, end_to, end_comment
        ) = (
            %(property_code)s,
            %(domain_id)s,
            %(range_id)s,
            %(description)s,
            %(type_id)s,
            %(begin_from)s, %(begin_to)s, %(begin_comment)s,
            %(end_from)s, %(end_to)s, %(end_comment)s)
        WHERE id = %(id)s;
        """,
        data)


def get_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(
        """
        SELECT
            l.id,
            l.property_code,
            l.domain_id,
            l.range_id,
            l.description,
            l.created,
            l.modified,
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
        WHERE l.id = %(id)s;
        """,
        {'id': id_})
    return dict(g.cursor.fetchone())


def get_links_by_type(type_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id, domain_id, range_id
        FROM model.link
        WHERE type_id = %(type_id)s;
        """,
        {'type_id': type_id})
    return [dict(row) for row in g.cursor.fetchall()]


def get_entity_ids_by_type_ids(type_ids: list[int]) -> list[int]:
    g.cursor.execute(
        """
        SELECT domain_id
        FROM model.link
        WHERE range_id IN %(type_ids)s AND property_code IN ('P2', 'P89')
        GROUP BY id
        ORDER BY id;
        """,
        {'type_ids': tuple(type_ids)})
    return [row[0] for row in g.cursor.fetchall()]


def delete_(id_: int) -> None:
    g.cursor.execute('DELETE FROM model.link WHERE id = %(id)s;', {'id': id_})


def get_all_links() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            l.id,
            l.property_code,
            l.domain_id,
            l.range_id,
            l.description,
            COALESCE(to_char(l.created, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS created,
            COALESCE(to_char(l.modified, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS modified,
            l.type_id,
            COALESCE(to_char(l.begin_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS begin_from,
            l.begin_comment,
            COALESCE(to_char(l.begin_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS begin_to,
            COALESCE(to_char(l.end_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS end_from,
            l.end_comment,
            COALESCE(to_char(l.end_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS end_to
        FROM model.link l;
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def check_link_duplicates() -> list[dict[str, int]]:
    g.cursor.execute(
        """
        SELECT
            COUNT(*) AS count,
            domain_id,
            range_id,
            property_code,
            description,
            type_id,
            begin_from, begin_to, begin_comment,
            end_from, end_to, end_comment
        FROM model.link
        GROUP BY
            domain_id,
            range_id,
            property_code,
            description,
            type_id,
            begin_from, begin_to, begin_comment,
            end_from, end_to, end_comment
        HAVING COUNT(*) > 1;
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def delete_link_duplicates() -> int:
    g.cursor.execute(
        """
        DELETE FROM model.link l
        WHERE l.id NOT IN (
            SELECT id FROM (
                SELECT DISTINCT ON (
                    domain_id,
                    range_id,
                    property_code,
                    description,
                    type_id,
                    begin_from, begin_to, begin_comment,
                    end_from, end_to, end_comment) *
                FROM model.link) AS temp_table);
        """)
    return g.cursor.rowcount


def get_all_links_for_network(
        system_classes: list[str]) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            l.id,
            l.property_code,
            l.domain_id,
            de.name AS domain_name,
            de.openatlas_class_name AS domain_system_class,
            l.range_id,
            re.name AS range_name,
            re.openatlas_class_name AS range_system_class,
            l.description,
            l.type_id
        FROM model.link l
        JOIN model.entity de ON l.domain_id = de.id
        JOIN model.entity re ON l.range_id = re.id
        WHERE de.openatlas_class_name IN  %(system_classes)s
            AND re.openatlas_class_name IN  %(system_classes)s
        """,
        {'system_classes': tuple(system_classes)})
    return [dict(row) for row in g.cursor.fetchall()]
