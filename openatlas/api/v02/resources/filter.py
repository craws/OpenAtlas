import datetime
from typing import Any, Dict, List, Union

from openatlas.api.v02.resources.error import FilterOperatorError, InvalidSearchDateError, \
    InvalidSearchNumberError, NoSearchStringError


class Filter:
    logical_operators: Dict[str, Any] = {
        'and': 'AND', 'or': 'OR', 'onot': 'OR NOT', 'anot': 'AND NOT'}

    valid_columns: Dict[str, str] = {
        'id': 'e.id', 'class_code': 'e.class_code', 'name': 'e.name',
        'description': 'e.description', 'system_class': 'e.system_class',
        'begin_from': 'e.begin_from', 'begin_to': 'e.begin_to',
        'created': 'e.created', 'modified': 'e.modified', 'end_to': 'e.end_to',
        'end_from': 'e.end_from'}
    compare_operators: Dict[str, Any] = {
        'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>', 'ge': '>=', 'like': 'LIKE'}
    valid_date_column: Dict[str, str] = {
        'begin_from': 'e.begin_from', 'begin_to': 'e.begin_to', 'created': 'e.created',
        'modified': 'e.modified', 'end_to': 'e.end_to', 'end_from': 'e.end_from'}

    @staticmethod
    def get_filter(parameters: Dict[str, Any], parser: Dict[str, Any]) -> str:
        clause = ''
        filters = Filter.validate_filter(parser['filter'])
        for filter_ in filters:
            if 'LIKE' in filter_['clause']:
                clause += ' ' + filter_['clause'] + ' LOWER(%(' + str(filter_['idx']) + ')s)'
            else:
                clause += ' ' + filter_['clause'] + ' %(' + str(filter_['idx']) + ')s'
            parameters[str(filter_['idx'])] = filter_['term']
        return clause

    @staticmethod
    def validate_filter(filter_: List[str]) -> List[Dict[str, Union[str, Any]]]:
        out = []
        if not filter_:
            return [{'clause': 'and e.id >=', 'term': 1, 'idx': '0'}]
        # Validate operators and add unsanitized 4th value
        data = [[word for word in f.split('|')
                 if f.split('|')[0] in Filter.logical_operators.keys()
                 and f.split('|')[1] in Filter.valid_columns
                 and f.split('|')[2] in Filter.compare_operators.keys()]
                for f in filter_]

        for i in data:
            if not i:
                raise FilterOperatorError  # pragma: no cover

        for idx, filter_ in enumerate(data):
            if not filter_[3]:
                raise NoSearchStringError  # pragma: no cover
            column = 'LOWER(' + Filter.valid_columns[filter_[1]] + ')' if \
                Filter.compare_operators[filter_[2]] == 'LIKE' else Filter.valid_columns[
                filter_[1]]
            out.append({
                'idx': idx,
                'term': Filter.validate_term(filter_),
                'clause': Filter.logical_operators[filter_[0]] + ' ' + column + ' ' +
                          Filter.compare_operators[filter_[2]]})
        return out

    @staticmethod
    def validate_term(filter_: List[str]) -> Union[int, str]:
        # Check if search term is a valid date if needed
        if Filter.valid_columns[filter_[1]] in Filter.valid_date_column.values():
            try:
                datetime.datetime.strptime(filter_[3], "%Y-%m-%d")
            except InvalidSearchDateError:  # pragma: no cover
                raise InvalidSearchDateError
        # Check if search term is an integer if column is id
        if Filter.valid_columns[filter_[1]] == 'e.id':
            try:
                int(filter_[3])
            except InvalidSearchNumberError:  # pragma: no cover
                raise InvalidSearchNumberError
        # If operator is LIKE then % are needed
        term = '%' + filter_[3] + '%' if Filter.compare_operators[filter_[2]] == 'LIKE' else \
            filter_[3]
        return term
