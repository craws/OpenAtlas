from typing import Any, Dict, List, Union

from flask import g
from flask_login import current_user

from openatlas import app
from openatlas.api.v02.resources.filter import Filter
from openatlas.models.entity import Entity


class Query(Entity):

    @staticmethod
    def get_by_class_code_api(code: Union[str, List[str]], parser: Dict[str, Any]) -> List[Entity]:
        parameters = {'codes': tuple(code if isinstance(code, list) else [code])}
        clause = Filter.get_filter(parameters=parameters, parser=parser)
        sql = Query.build_sql() + """
            WHERE class_code IN %(codes)s {clause} 
            ORDER BY {order} {sort};""".format(clause=clause,
                                               order=', '.join(parser['column']),
                                               sort=parser['sort'])
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_menu_item_api(menu_item: str,
                             parser: Dict[str, Any]) -> List[Entity]:  # pragma: no cover
        # Possible class names: actor, event, place, reference, source, object
        parameters = {'codes': tuple(app.config['CLASS_CODES'][menu_item])}
        clause = Filter.get_filter(parameters=parameters, parser=parser)
        if menu_item == 'source':
            sql = Query.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type = 'source content' {clause}
                 GROUP BY e.id ORDER BY {order} {sort};""".format(clause=clause,
                                                                  order=', '.join(parser['column']),
                                                                  sort=parser['sort'])
        elif menu_item == 'reference':
            sql = Query.build_sql(nodes=True) + """
                WHERE e.class_code IN %(codes)s AND e.system_type != 'file' {clause} 
                 GROUP BY e.id ORDER BY {order} {sort};""".format(clause=clause,
                                                                  order=', '.join(parser['column']),
                                                                  sort=parser['sort'])
        else:
            aliases = True if menu_item == 'actor' and current_user.is_authenticated and \
                              current_user.settings['table_show_aliases'] else False
            sql = Query.build_sql(nodes=True if menu_item == 'event' else False,
                                  aliases=aliases) + """
                WHERE e.class_code IN %(codes)s {clause} GROUP BY e.id
                ORDER BY {order} {sort};""".format(clause=clause,
                                                   order=', '.join(parser['column']),
                                                   sort=parser['sort'])
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]
