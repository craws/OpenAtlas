from typing import Any, Dict, List, Optional

from flask import g

from openatlas.database.entity import Entity


class Search:

    @staticmethod
    def search(term: str,
               classes: List[str],
               desc: bool = False,
               own: bool = False,
               user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        sql = Entity.build_sql() + """
            {user_clause}
            WHERE (UNACCENT(LOWER(e.name)) LIKE UNACCENT(LOWER(%(term)s))
            {description_clause})
            {user_clause2}
            AND e.system_class IN %(classes)s GROUP BY e.id ORDER BY e.name;""".format(
            user_clause="""
                LEFT JOIN web.user_log ul ON e.id = ul.entity_id """ if own else '',
            description_clause="""
                OR UNACCENT(lower(e.description)) LIKE UNACCENT(lower(%(term)s))
                OR UNACCENT(lower(e.begin_comment)) LIKE UNACCENT(lower(%(term)s))
                OR UNACCENT(lower(e.end_comment)) LIKE UNACCENT(lower(%(term)s))"""
            if desc else '',
            user_clause2=' AND ul.user_id = %(user_id)s ' if own else '')
        g.cursor.execute(sql, {
            'term': '%' + term + '%',
            'user_id': user_id,
            'classes': tuple(classes)})
        return [dict(row) for row in g.cursor.fetchall()]
