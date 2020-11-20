from __future__ import annotations  # Needed for Python 4.0 type annotations

import datetime
from typing import Any, Dict, List, Union

from openatlas.api.v01.error import APIError


class Filter:
    operators_logical: Dict[str, Any] = {'and': 'AND', 'or': 'OR', 'onot': 'OR NOT',
                                         'anot': 'AND NOT'}

    column_validation: Dict[str, str] = {'id': 'e.id', 'class_code': 'e.class_code',
                                         'name': 'e.name', 'description': 'e.description',
                                         'system_type': 'e.system_type',
                                         'begin_from': 'e.begin_from', 'begin_to': 'e.begin_to',
                                         'created': 'e.created', 'modified': 'e.modified',
                                         'end_to': 'e.end_to', 'end_from': 'e.end_from'}
    operators_compare: Dict[str, Any] = {'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>',
                                         'ge': '>=', 'like': 'LIKE'}
    date_column_validation: Dict[str, str] = {'begin_from': 'e.begin_from',
                                              'begin_to': 'e.begin_to',
                                              'created': 'e.created', 'modified': 'e.modified',
                                              'end_to': 'e.end_to', 'end_from': 'e.end_from'}

    @staticmethod
    def validate_filter(filter_: List[str]) -> List[Dict[str, Union[str, Any]]]:
        out = []
        if not filter_:
            return [{'clause': 'and e.id >=', 'term': 1, 'idx': '0'}]
        # Validate operators and add unsanitized 4th value
        data = [[word for word in f.split('|')
                 if f.split('|')[0] in Filter.operators_logical.keys()
                 and f.split('|')[1] in Filter.column_validation
                 and f.split('|')[2] in Filter.operators_compare.keys()]
                for f in filter_]

        for i in data:
            if not i:
                raise APIError('Filter operators is not implemented or wrong.', status_code=404,
                               payload="404j")

        for idx, filter_ in enumerate(data):
            if not filter_[3]:
                raise APIError('No search term.', status_code=404, payload="404i")
            column = 'LOWER(' + Filter.column_validation[filter_[1]] + ')' if \
                Filter.operators_compare[filter_[2]] == 'LIKE' else Filter.column_validation[
                filter_[1]]
            out.append({
                'idx': idx,
                'term': Filter.validate_term(filter_),
                'clause': Filter.operators_logical[filter_[0]] + ' ' + column + ' ' +
                          Filter.operators_compare[filter_[2]]})
        return out

    @staticmethod
    def validate_term(filter_: List[str]) -> Union[int, str]:
        # Check if search term is a valid date if needed
        if Filter.column_validation[filter_[1]] in Filter.date_column_validation.values():
            try:
                datetime.datetime.strptime(filter_[3], "%Y-%m-%d")
            except:
                raise APIError('Invalid search term: ' + filter_[3], status_code=404,
                               payload="404k")
        # Check if search term is an integer if column is id
        if Filter.column_validation[filter_[1]] == 'e.id':
            try:
                int(filter_[3])
            except:
                raise APIError('Invalid search term: ' + filter_[3], status_code=404,
                               payload="404l")
        # If operator is LIKE then % are needed
        term = '%' + filter_[3] + '%' if Filter.operators_compare[filter_[2]] == 'LIKE' else \
            filter_[3]
        return term
