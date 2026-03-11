from typing import Any

from flask import g


def get_rights_holder() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id,
               name,
               class as openatlas_class_name,
               description,
               created,
               modified
        FROM model.rights_holder
        """)
    return list(g.cursor)


def get_rights_holder_by_id(id_: int) -> dict[str, Any] | None:
    g.cursor.execute(
        """
        SELECT id,
               name,
               class as openatlas_class_name,
               description,
               created,
               modified
        FROM model.rights_holder
        WHERE id = %(id)s
        """,
        {'id': id_})
    return g.cursor.fetchone()


def insert_rights_holder(entry: dict[str, Any]) -> int:
    g.cursor.execute(
        """
        INSERT INTO model.rights_holder (name, class, description)
        VALUES (%(name)s, %(role)s, %(description)s)
        RETURNING id;
        """,
        entry)
    return g.cursor.fetchone()['id']


def rights_holder_delete(id_: int) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.rights_holder
        WHERE id = %(id)s
        """,
        {'id': id_})


def update_rights_holder(id_: int, entry: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE model.rights_holder
        SET name        = %(name)s,
            class       = %(role)s,
            description = %(description)s
        WHERE id = %(id)s
        """,
        {'id': id_, **entry})


def get_rights_holder_links() -> dict[int, dict[str, list[int]]]:
    g.cursor.execute(
        """
        SELECT entity_id, 
               description, 
               array_agg(rights_holder_id) as ids
        FROM model.rights_holder_file
        GROUP BY entity_id, description
        """)
    result: dict[int, dict[str, list[int]]] = {}
    for row in g.cursor:
        eid = row['entity_id']
        if eid not in result:
            result[eid] = {'creator': [], 'license_holder': []}
        result[eid][row['description']] = row['ids']
    return result


def get_rights_holders_by_entity_and_role(
        entity_id: int,
        role: str) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT rh.id,
               rh.name,
               rh.class as openatlas_class_name,
               rh.description,
               rh.created,
               rh.modified
        FROM model.rights_holder_file rhl
        LEFT JOIN model.rights_holder rh ON rhl.rights_holder_id = rh.id
        WHERE rhl.entity_id = %(entity_id)s
          AND rhl.description = %(description)s;
        """, {
            'entity_id': entity_id,
            'description': role})
    return list(g.cursor)


def insert_rights_holder_link(
        entity_id: int, rights_holder_id: int, role: str) -> None:
    g.cursor.execute(
        """
        INSERT INTO model.rights_holder_file (entity_id,
                                              rights_holder_id,
                                              description)
        VALUES (%(entity_id)s,
                %(rights_holder_id)s,
                %(description)s)
        """, {
            'entity_id': entity_id,
            'rights_holder_id': rights_holder_id,
            'description': role})


def delete_rights_holder_links(entity_id: int) -> None:
    g.cursor.execute(
        'DELETE FROM model.rights_holder_file WHERE entity_id = %(id)s;',
        {'id': entity_id})
