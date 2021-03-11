from typing import Any, Dict, List, Union

from flask import g

from openatlas.api.v02.resources.filter import Filter
from openatlas.models.entity import Entity


class Query(Entity):

    @staticmethod
    def get_by_class_code_api(code: Union[str, List[str]], parser: Dict[str, Any]) -> List[Entity]:
        parameters = {'codes': tuple(code if isinstance(code, list) else [code])}
        sql = Query.build_sql(nodes=True) + """
            WHERE class_code IN %(codes)s {clause} 
            GROUP BY e.id
            ORDER BY {order} {sort};""".format(
            clause=Filter.get_filter(parameters=parameters, parser=parser),
            order=', '.join(parser['column']),
            sort=parser['sort'])
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_system_class(classes: str, parser: Dict[str, Any]) -> List[Entity]:
        parameters = {'class': tuple(classes if isinstance(classes, list) else [classes])}
        sql = Query.build_sql(nodes=True, aliases=True) + """
            WHERE e.system_class
            IN %(class)s {clause}
            GROUP BY e.id ORDER BY {order} {sort};""".format(
            clause=Filter.get_filter(parameters=parameters, parser=parser),
            order=', '.join(parser['column']),
            sort=parser['sort'])
        g.execute(sql, parameters)
        return [Query(row) for row in g.cursor.fetchall()]
