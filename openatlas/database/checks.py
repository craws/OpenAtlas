from typing import Any

from flask import g


def check_single_type_duplicates(ids: list[int]) -> list[int]:
    g.cursor.execute(
        """
        SELECT domain_id
        FROM model.link
        WHERE property_code = 'P2' AND range_id IN %(ids)s
        GROUP BY domain_id
        HAVING COUNT(*) > 1;
        """,
        {'ids': tuple(ids)})
    return [row['domain_id'] for row in g.cursor.fetchall()]


def get_orphaned_subunits() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT e.id
        FROM model.entity e
        LEFT JOIN model.link l ON e.id = l.range_id AND l.property_code = 'P46'
        WHERE l.domain_id IS NULL
            AND e.openatlas_class_name IN ('feature', 'stratigraphic_unit')
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def get_orphans() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT e.id
        FROM model.entity e
        LEFT JOIN model.link l1 ON e.id = l1.domain_id
            AND l1.range_id NOT IN
                (SELECT id FROM model.entity WHERE cidoc_class_code = 'E55')
        LEFT JOIN model.link l2 ON e.id = l2.range_id
        WHERE l1.domain_id IS NULL
            AND l2.range_id IS NULL
            AND e.cidoc_class_code != 'E55'
            AND e.openatlas_class_name != 'reference_system';
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def get_circular() -> list[dict[str, Any]]:
    g.cursor.execute(
        'SELECT domain_id FROM model.link WHERE domain_id = range_id;')
    return [dict(row) for row in g.cursor.fetchall()]


def get_cidoc_links() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT DISTINCT
            l.property_code,
            d.cidoc_class_code AS domain_code,
            r.cidoc_class_code AS range_code
        FROM model.link l
        JOIN model.entity d ON l.domain_id = d.id
        JOIN model.entity r ON l.range_id = r.id;
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def get_invalid_links(data: dict[str, Any]) -> list[dict[str, int]]:
    g.cursor.execute(
        """
        SELECT
            l.id,
            l.property_code,
            l.domain_id,
            l.range_id,
            l.description,
            l.created,
            l.modified
        FROM model.link l
        JOIN model.entity d ON l.domain_id = d.id
        JOIN model.entity r ON l.range_id = r.id
        WHERE l.property_code = %(property_code)s
            AND d.cidoc_class_code = %(domain_code)s
            AND r.cidoc_class_code = %(range_code)s;
        """,
        data)
    return [dict(row) for row in g.cursor.fetchall()]
