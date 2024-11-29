from typing import Any, Optional

from flask import g

SQL = """
    SELECT
        p.id,
        p.name,
        p.description,
        p.created,
        p.modified,
        COUNT(e.id) AS count
    FROM import.project p
    LEFT JOIN import.entity e ON p.id = e.project_id """


def insert_project(name: str, description: Optional[str]) -> int:
    g.cursor.execute(
        """
        INSERT INTO import.project (name, description)
        VALUES (%(name)s, %(description)s)
        RETURNING id;
        """,
        {'name': name, 'description':  description})
    return g.cursor.fetchone()['id']


def get_all_projects() -> list[dict[str, Any]]:
    g.cursor.execute(f'{SQL} GROUP BY p.id ORDER BY name;')
    return list(g.cursor)


def get_project_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(f'{SQL} WHERE p.id = %(id)s GROUP BY p.id;', {'id': id_})
    return g.cursor.fetchone()


def get_project_by_name(name: str) -> dict[str, Any]:
    g.cursor.execute(
        f'{SQL} WHERE p.name = %(name)s GROUP BY p.id;',
        {'name': name})
    return g.cursor.fetchone()


def delete_project(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM import.project WHERE id = %(id)s;',
        {'id': id_})


def check_origin_ids(project_id: int, origin_ids: list[str]) -> list[str]:
    g.cursor.execute(
        """
        SELECT origin_id
        FROM import.entity
        WHERE project_id = %(project_id)s AND origin_id IN %(ids)s;
        """,
        {'project_id': project_id, 'ids': tuple(set(origin_ids))})
    return [row[0] for row in list(g.cursor)]


def get_id_from_origin_id(project_id: int, origin_id: str) -> list[str]:
    g.cursor.execute(
        """
        SELECT entity_id FROM import.entity
        WHERE project_id = %(project_id)s AND origin_id = %(ids)s;
        """,
        {'project_id': project_id, 'ids': origin_id})
    return g.cursor.fetchone()


def check_duplicates(class_: str, names: list[str]) -> list[str]:
    g.cursor.execute(
        """
        SELECT DISTINCT name FROM model.entity
        WHERE openatlas_class_name = %(class_)s AND LOWER(name) IN %(names)s;
        """,
        {'class_': class_, 'names': tuple(names)})
    return [row[0] for row in list(g.cursor)]


def update_project(id_: int, name: str, description: Optional[str]) -> None:
    g.cursor.execute(
        """
        UPDATE import.project
        SET (name, description) = (%(name)s, %(description)s)
        WHERE id = %(id)s;
        """,
        {'id': id_, 'name': name, 'description': description})


def import_data(
        project_id: int,
        entity_id: int,
        user_id: int,
        origin_id: Optional[int]) -> None:
    g.cursor.execute(
        """
        INSERT INTO import.entity (
            project_id, origin_id, entity_id, user_id
        ) VALUES (
            %(project_id)s, %(origin_id)s, %(entity_id)s, %(user_id)s);
        """, {
            'project_id': project_id,
            'origin_id': origin_id,
            'entity_id': entity_id,
            'user_id': user_id})
