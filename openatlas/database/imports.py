from typing import Any, Optional

from flask import g


class Import:
    sql = """
        SELECT
            p.id, p.name,
            p.description,
            p.created,
            p.modified,
            COUNT(e.id) AS count
        FROM import.project p
        LEFT JOIN import.entity e ON p.id = e.project_id """

    @staticmethod
    def insert_project(name: str, description: Optional[str]) -> int:
        g.cursor.execute(
            """
            INSERT INTO import.project (name, description)
            VALUES (%(name)s, %(description)s)
            RETURNING id;
            """,
            {'name': name, 'description': description})
        return g.cursor.fetchone()['id']

    @staticmethod
    def get_all_projects() -> list[dict[str, Any]]:
        g.cursor.execute(f'{Import.sql} GROUP BY p.id ORDER BY name;')
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_project_by_id(id_: int) -> dict[str, Any]:
        g.cursor.execute(
            f'{Import.sql} WHERE p.id = %(id)s GROUP BY p.id;',
            {'id': id_})
        return dict(g.cursor.fetchone())

    @staticmethod
    def get_project_by_name(name: str) -> Optional[dict[str, Any]]:
        g.cursor.execute(
            f'{Import.sql} WHERE p.name = %(name)s GROUP BY p.id;',
            {'name': name})
        return dict(g.cursor.fetchone()) if g.cursor.rowcount else None

    @staticmethod
    def delete_project(id_: int) -> None:
        g.cursor.execute(
            'DELETE FROM import.project WHERE id = %(id)s;',
            {'id': id_})

    @staticmethod
    def check_origin_ids(project_id: int, origin_ids: list[str]) -> list[str]:
        g.cursor.execute(
            """
            SELECT origin_id FROM import.entity
            WHERE project_id = %(project_id)s AND origin_id IN %(ids)s;
            """,
            {'project_id': project_id, 'ids': tuple(set(origin_ids))})
        return [row['origin_id'] for row in g.cursor.fetchall()]

    @staticmethod
    def check_duplicates(class_: str, names: list[str]) -> list[str]:
        g.cursor.execute(
            """
            SELECT DISTINCT name FROM model.entity
            WHERE openatlas_class_name = %(class_)s
                AND LOWER(name) IN %(names)s;
            """,
            {'class_': class_, 'names': tuple(names)})
        return [row['name'] for row in g.cursor.fetchall()]

    @staticmethod
    def update_project(id_: int, name: str, description: str) -> None:
        g.cursor.execute(
            """
            UPDATE import.project
            SET (name, description) = (%(name)s, %(description)s)
            WHERE id = %(id)s;
            """,
            {'id': id_, 'name': name, 'description': description})

    @staticmethod
    def import_data(
            project_id: int,
            entity_id: int,
            user_id: int,
            origin_id: Optional[int]) -> None:
        g.cursor.execute(
            """
            INSERT INTO import.entity (
                project_id,
                origin_id,
                entity_id,
                user_id)
            VALUES (
                %(project_id)s,
                %(origin_id)s,
                %(entity_id)s,
                %(user_id)s);
            """, {
                'project_id': project_id,
                'origin_id': origin_id,
                'entity_id': entity_id,
                'user_id': user_id})
