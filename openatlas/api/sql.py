from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Dict, List, TYPE_CHECKING, Union

from flask import g
from flask_login import current_user

from openatlas import app
from openatlas.models.entity import Entity

if TYPE_CHECKING:  # pragma: no cover - Type checking is disabled in tests
    pass


class Query(Entity):

    @staticmethod
    def get_by_class_code_api(code: Union[str, List[str]], meta: Dict[str, Any]) -> List[Query]:
        clause = ""
        parameters = {'codes': tuple(code if isinstance(code, list) else [code])}
        for filter_ in meta['filter']:
            if 'LIKE' in filter_['clause']:
                clause += ' ' + filter_['clause'] + ' LOWER(%(' + str(filter_['idx']) + ')s)'
            else:
                clause += ' ' + filter_['clause'] + ' %(' + str(filter_['idx']) + ')s'
            parameters[str(filter_['idx'])] = filter_['term']
        sql = Query.build_sql() + """
            WHERE class_code IN %(codes)s {clause} 
            ORDER BY {order} {sort};""".format(clause=clause,
                                               order=', '.join(meta['column']),
                                               sort=meta['sort'])
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_menu_item_api(menu_item: str,
                             meta: Dict[str, Any]) -> List[Query]:  # pragma: no cover
        # Possible class names: actor, event, place, reference, source, object
        clause = ""
        parameters = {'codes': tuple(app.config['CLASS_CODES'][menu_item])}
        for filter_ in meta['filter']:
            if 'LIKE' in filter_['clause']:
                clause += ' ' + filter_['clause'] + ' LOWER(%(' + str(filter_['idx']) + ')s)'
            else:
                clause += ' ' + filter_['clause'] + ' %(' + str(filter_['idx']) + ')s'
            parameters[str(filter_['idx'])] = filter_['term']
        if menu_item == 'source':
            sql = Query.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type = 'source content' {clause}
                 GROUP BY e.id ORDER BY {order} {sort};""".format(clause=clause,
                                                                  order=', '.join(meta['column']),
                                                                  sort=meta['sort'])
        elif menu_item == 'reference':
            sql = Query.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type != 'file' {clause} 
                 GROUP BY e.id ORDER BY {order} {sort};""".format(clause=clause,
                                                                  order=', '.join(meta['column']),
                                                                  sort=meta['sort'])
        else:
            aliases = True if menu_item == 'actor' and current_user.is_authenticated and \
                              current_user.settings['table_show_aliases'] else False
            sql = Query.build_sql(nodes=True if menu_item == 'event' else False,
                                  aliases=aliases) + """
                WHERE e.class_code IN %(codes)s {clause} GROUP BY e.id
                ORDER BY {order} {sort};""".format(clause=clause,
                                                   order=', '.join(meta['column']),
                                                   sort=meta['sort'])
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]
