from typing import Any, Union

from flask import g

from openatlas.database.entity import Entity


class Api:

    @staticmethod
    def get_by_class_code(
            code: Union[str, list[str]],
            parser: dict[str, Any]) -> list[dict[str, Any]]:
        sql_parts = Filter.get_filter(
            parameters={
                'codes': tuple(code if isinstance(code, list) else [code])},
            parser=parser)
        sql = Entity.build_sql(types=True) + f"""
            WHERE cidoc_class_code IN %(codes)s {sql_parts['clause']} 
            GROUP BY e.id
            ORDER BY {', '.join(parser['column'])} {parser['sort']};"""
        g.cursor.execute(sql, sql_parts['parameters'])
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_system_class(
            classes: Union[str, list[str]],
            parser: dict[str, Any]) -> list[dict[str, Any]]:
        sql_parts = Filter.get_filter(
            parameters={
                'class': tuple(
                    classes if isinstance(classes, list) else [classes])},
            parser=parser)
        sql = Entity.build_sql(types=True, aliases=True) + f"""
            WHERE e.openatlas_class_name IN %(class)s {sql_parts['clause']}
            GROUP BY e.id
            ORDER BY {', '.join(parser['column'])} {parser['sort']};"""
        g.cursor.execute(sql, sql_parts['parameters'])
        return [dict(row) for row in g.cursor.fetchall()]


class Filter:
    logical_operators: dict[str, Any] = {
        'and': 'AND', 'or': 'OR', 'onot': 'OR NOT', 'anot': 'AND NOT'}
    valid_columns: dict[str, str] = {
        'id': 'e.id',
        'class_code': 'e.class_code',
        'name': 'e.name',
        'description': 'e.description',
        'system_class': 'e.openatlas_class_name',
        'begin_from': 'e.begin_from',
        'begin_to': 'e.begin_to',
        'created': 'e.created',
        'modified': 'e.modified',
        'end_to': 'e.end_to',
        'end_from': 'e.end_from'}
    compare_operators: dict[str, Any] = {
        'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>', 'ge': '>=',
        'like': 'LIKE'}
    valid_date_column: dict[str, str] = {
        'begin_from': 'e.begin_from', 'begin_to': 'e.begin_to',
        'created': 'e.created',
        'modified': 'e.modified', 'end_to': 'e.end_to',
        'end_from': 'e.end_from'}

    @staticmethod
    def get_filter(
            parameters: dict[str, Any],
            parser: dict[str, Any]) -> dict[str, Any]:
        filters: list[dict[str, Any]] = [
            {'clause': 'and e.id >=', 'term': 1, 'idx': '0'}]
        if parser['filter']:
            filters = Filter.prepare_sql(parser['filter'])
        clause = ''
        for filter_ in filters:
            if 'LIKE' in filter_['clause']:
                clause += ' ' + filter_['clause'] + ' LOWER(%(' + str(
                    filter_['idx']) + ')s)'
            else:
                clause += ' ' + filter_['clause'] + ' %(' + str(
                    filter_['idx']) + ')s'
            parameters[str(filter_['idx'])] = filter_['term']
        return {'clause': clause, 'parameters': parameters}

    @staticmethod
    def prepare_sql(filter_: list[str]) -> list[dict[str, Any]]:
        from openatlas.api.v02.resources.filter_validation import Validation
        filter_clean = Validation.get_filter_from_url_parameter(filter_)
        out = []
        for key, value in enumerate(filter_clean):
            column = Filter.valid_columns[value[1]]
            if Filter.compare_operators[value[2]] == 'LIKE':
                column = 'LOWER(' + Filter.valid_columns[value[1]] + ')'
            out.append({
                'idx': key,
                'term': Filter.validate_term(value),
                'clause':
                    Filter.logical_operators[value[0]] + ' ' + column + ' ' +
                    Filter.compare_operators[value[2]]})
        return out

    @staticmethod
    def validate_term(filter_: list[str]) -> Union[int, str]:
        from openatlas.api.v02.resources.filter_validation import Validation
        # Check if search term is a valid date if needed
        if Filter.valid_columns[
                filter_[1]] in Filter.valid_date_column.values():
            Validation.test_date(filter_[3])
        # Check if search term is an integer if column is id
        if Filter.valid_columns[filter_[1]] == 'e.id':
            Validation.test_id(filter_[3])
        # If operator is LIKE then % are needed
        term = '%' + filter_[3] + '%' \
            if Filter.compare_operators[filter_[2]] == 'LIKE' else filter_[3]
        return term
