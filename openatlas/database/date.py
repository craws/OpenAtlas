from typing import Any

from flask import g


def invalid_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id
        FROM model.entity
        WHERE begin_from > begin_to
            OR end_from > end_to
            OR begin_from > end_from
            OR begin_to > end_to
            OR COALESCE(begin_from, begin_to) > COALESCE(end_to, end_from);
        """)
    return list(g.cursor)


def invalid_link_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id
        FROM model.link
        WHERE begin_from > begin_to
            OR end_from > end_to
            OR begin_from > end_from
            OR begin_to > end_to
            OR COALESCE(begin_from, begin_to) > COALESCE(end_to, end_from);
        """)
    return list(g.cursor)


def invalid_involvement_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT involvement.id
        FROM model.entity actor
        JOIN model.link involvement ON actor.id = involvement.range_id
            AND involvement.property_code IN ('P11', 'P14', 'P22', 'P23')
        JOIN model.entity event ON involvement.domain_id = event.id
        WHERE
            COALESCE(actor.end_to, actor.end_from)
                < COALESCE(involvement.end_from, involvement.end_to)
            OR actor.begin_to > involvement.end_to
            OR COALESCE(actor.begin_from, actor.begin_to)
                > COALESCE(event.end_to, event.end_from)
            OR actor.begin_to > event.end_to
            OR involvement.begin_from > involvement.end_from
            OR involvement.begin_to > involvement.end_to
            OR COALESCE(involvement.begin_from, involvement.begin_to)
                > COALESCE(involvement.end_to, involvement.end_from)
            OR COALESCE(involvement.begin_from, involvement.begin_to)
                > COALESCE(event.end_to, event.end_from)
            OR involvement.begin_to > event.end_to
            OR COALESCE(involvement.end_from, involvement.end_to)
                > COALESCE(event.end_to, event.end_from)
            OR COALESCE(involvement.begin_from, involvement.begin_to)
                < COALESCE(event.begin_from, event.begin_to);
        """)
    return list(g.cursor)


def invalid_preceding_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT link.id
        FROM model.entity preceding
        JOIN model.link ON preceding.id = link.range_id
            AND link.property_code = 'P134'
        JOIN model.entity succeeding ON link.domain_id = succeeding.id
        WHERE
            COALESCE(preceding.begin_from, preceding.begin_to) IS NOT NULL
                AND COALESCE(succeeding.begin_from, succeeding.begin_to)
                    IS NOT NULL
                AND COALESCE(succeeding.begin_from, succeeding.begin_to)
                    < COALESCE(preceding.begin_from, preceding.begin_to);
        """)
    return list(g.cursor)


def invalid_sub_dates() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT link.id
        FROM model.entity super
        JOIN model.link ON super.id = link.domain_id
            AND link.property_code = 'P9'
        JOIN model.entity sub ON link.range_id = sub.id
        WHERE
            (COALESCE(super.begin_from, super.begin_to) IS NOT NULL
                AND COALESCE(sub.begin_from, sub.begin_to) IS NOT NULL
                AND COALESCE(sub.begin_from, sub.begin_to)
                    < COALESCE(super.begin_from, super.begin_to))
            OR (COALESCE(super.end_to, super.end_from) IS NOT NULL
                AND COALESCE(sub.end_to, sub.end_from) IS NOT NULL
                AND COALESCE(sub.end_to, sub.end_from)
                    > COALESCE(super.end_to, super.end_from));
        """)
    return list(g.cursor)
