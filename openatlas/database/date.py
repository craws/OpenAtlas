from typing import Any

from flask import g


def invalid_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id
        FROM model.entity
        WHERE begin_from > begin_to
            OR end_from > end_to
            OR (
                begin_from IS NOT NULL
                AND end_from IS NOT NULL
                AND begin_from > end_from)
            OR (
                begin_to IS NOT NULL
                AND end_to IS NOT NULL
                AND begin_to > end_to);
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def invalid_link_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id
        FROM model.link
        WHERE begin_from > begin_to
            OR end_from > end_to
            OR (
                begin_from IS NOT NULL
                AND end_from IS NOT NULL
                AND begin_from > end_from)
            OR (
                begin_to IS NOT NULL
                AND end_to IS NOT NULL
                AND begin_to > end_to);
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def invalid_involvement_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT involvement.id
        FROM model.entity actor
        JOIN model.link involvement ON actor.id = involvement.range_id
            AND involvement.property_code IN ('P11', 'P14', 'P22', 'P23')
        JOIN model.entity event ON involvement.domain_id = event.id
        WHERE
            (actor.begin_from IS NOT NULL
                AND involvement.end_from IS NOT NULL
                AND actor.end_from < involvement.end_from)
            OR (actor.begin_to IS NOT NULL
                AND involvement.end_to IS NOT NULL
                AND actor.begin_to > involvement.end_to)
            OR (actor.begin_from IS NOT NULL
                AND event.end_from IS NOT NULL
                AND actor.begin_from > event.end_from)
            OR (actor.begin_to IS NOT NULL
                AND event.end_to IS NOT NULL
                AND actor.begin_to > event.end_to)
            OR (involvement.begin_from IS NOT NULL
                AND involvement.end_from IS NOT NULL
                AND involvement.begin_from > involvement.end_from)
            OR (involvement.begin_to IS NOT NULL
                AND involvement.end_to IS NOT NULL
                AND involvement.begin_to > involvement.end_to)
            OR (involvement.begin_from IS NOT NULL
                AND event.end_from IS NOT NULL
                AND involvement.begin_from > event.end_from)
            OR (involvement.begin_to IS NOT NULL
                AND event.end_to IS NOT NULL
                AND involvement.begin_to > event.end_to)
            OR (involvement.end_from IS NOT NULL
                AND event.end_to IS NOT NULL
                AND involvement.end_from > event.end_to)
            OR (involvement.begin_from IS NOT NULL
                AND event.begin_from IS NOT NULL
                AND involvement.begin_from < event.begin_from);
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def invalid_preceding_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT link.id
        FROM model.entity preceding
        JOIN model.link ON preceding.id = link.range_id
            AND link.property_code = 'P134'
        JOIN model.entity succeeding ON link.domain_id = succeeding.id
        WHERE
            preceding.begin_from IS NOT NULL
                AND succeeding.begin_from IS NOT NULL
                AND succeeding.begin_from < preceding.begin_from;
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def invalid_sub_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT link.id
        FROM model.entity super
        JOIN model.link ON super.id = link.domain_id
            AND link.property_code = 'P9'
        JOIN model.entity sub ON link.range_id = sub.id
        WHERE
            (super.begin_from IS NOT NULL
                AND sub.begin_from IS NOT NULL
                AND sub.begin_from < super.begin_from)
            OR (super.end_from IS NOT NULL AND sub.end_from IS NOT NULL
                AND (super.end_to IS NULL AND sub.end_to IS NULL AND
                    sub.end_from > super.end_from)
                OR (super.end_to IS NULL AND sub.end_to IS NOT NULL AND
                    sub.end_from > super.end_to)
                OR (super.end_to IS NOT NULL AND sub.end_to IS NULL AND
                    sub.end_to > super.end_from)
                OR (super.end_to IS NOT NULL AND sub.end_to IS NOT NULL AND
                    sub.end_to > super.end_to));
        """)
    return [dict(row) for row in g.cursor.fetchall()]
