import re
import datetime
from typing import Any, Dict, List, Optional, Union

from openatlas.api.error import APIError


class Default:
    limit: int = 20
    sort: str = 'ASC'
    filter: List = [{'clause': 'and e.id >=', 'term': 1, 'idx': '0'}]
    column: List = ['name']
    last: Optional[str] = None
    first: Optional[str] = None
    count: bool = False
    download: bool = False
    operators_compare: Dict[str, Any] = {'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>',
                                         'ge': '>=', 'like': 'LIKE'}
    operators_logical: Dict[str, Any] = {'and': 'AND', 'or': 'OR', 'onot': 'OR NOT',
                                         'anot': 'AND NOT'}
    column_validation: Dict[str, str] = {'id': 'e.id', 'class_code': 'e.class_code',
                                         'name': 'e.name', 'description': 'e.description',
                                         'system_type': 'e.system_type',
                                         'begin_from': 'e.begin_from', 'begin_to': 'e.begin_to',
                                         'created': 'e.created', 'modified': 'e.modified',
                                         'end_to': 'e.end_to', 'end_from': 'e.end_from'}
    date_column_validation: Dict[str, str] = {'begin_from': 'e.begin_from',
                                              'begin_to': 'e.begin_to',
                                              'created': 'e.created', 'modified': 'e.modified',
                                              'end_to': 'e.end_to', 'end_from': 'e.end_from'}
    show_validation: List[str] = ['when', 'types', 'relations', 'names', 'links', 'geometry',
                                  'depictions', 'geonames']


class Validation:

    @staticmethod
    def validate_url_query(query: Any) -> Dict[str, Any]:
        return {'filter': Validation.validate_filter(query.getlist('filter')),  # has to be list
                'limit': Validation.validate_limit(query.get('limit')),
                'sort': Validation.validate_sort(query.get('sort')),
                'column': Validation.validate_column(query.getlist('column')),  # has to be list
                'last': Validation.validate_last(query.get('last')),
                'first': Validation.validate_first(query.get('first')),
                'show': Validation.validate_show(query.getlist('show')),  # has to be list
                'count': Validation.validate_count(query.getlist('count')),  # has to be list
                'download': Validation.validate_download(
                    query.getlist('download'))}  # has to be list

    @staticmethod
    def validate_filter(filter_: List[str]) -> List[Dict[str, Union[str, Any]]]:  # pragma: no cover
        out = []
        if not filter_:
            return Default.filter
        # Validate operators and add unsanitized 4th value
        data = [[word for word in f.split('|')
                 if f.split('|')[0] in Default.operators_logical.keys()
                 and f.split('|')[1] in Default.column_validation
                 and f.split('|')[2] in Default.operators_compare.keys()]
                for f in filter_]

        for i in data:
            if not i:
                raise APIError('Filter operators is not implemented or wrong.', status_code=404,
                               payload="404j")

        for idx, filter_ in enumerate(data):
            if not filter_[3]:
                raise APIError('No search term.', status_code=404, payload="404i")
             # column = Default.column_validation[filter_[1]] \
             #    if filter_[3].isdigit() else 'LOWER(' + Default.column_validation[filter_[1]] + ')'
            column = 'LOWER(' + Default.column_validation[filter_[1]] + ')' if filter_[2] == 'LIKE' else Default.column_validation[filter_[1]]
            print(column)
            out.append({
                'idx': idx,
                'term': Validation.validate_term(filter_),
                'clause': Default.operators_logical[filter_[0]] + ' ' +
                          column + ' ' +
                          Default.operators_compare[filter_[2]]})
        print(out)
        return out

    @staticmethod
    def validate_term(filter_: List[str]) -> Union[int, str]:
        # Check if search term is a valid date if needed
        if Default.column_validation[filter_[1]] in Default.date_column_validation.values():
            try:
                datetime.datetime.strptime(filter_[3], "%Y-%m-%d")
            except:
                raise APIError('Invalid search term: ' + filter_[3], status_code=404,
                               payload="404k")
        # Check if search term is an integer if column is id
        if Default.column_validation[filter_[1]] == 'e.id':
            try:
                int(filter_[3])
            except:
                raise APIError('Invalid search term: ' + filter_[3], status_code=404, payload="404l")

        operator = Default.operators_compare[filter_[2]]
        # int(filter_[3]) if filter_[3].isdigit() else '%%' + filter_[3] + '%%',

        return filter_[3]

    @staticmethod
    def validate_limit(limit: Optional[str] = None) -> int:
        return int(limit) if limit and limit.isdigit() else Default.limit

    @staticmethod
    def validate_sort(sort: Optional[str] = None) -> str:
        return Default.sort if not sort or sort.lower() != 'desc' else 'DESC'

    @staticmethod
    def validate_column(column: List[str]) -> List[str]:
        return Default.column if not column or [c.lower() for c in
                                                column] in Default.column else column

    @staticmethod
    def validate_last(last: Optional[str]) -> Optional[str]:
        return Default.last if not last or last.isdigit() is not True else last

    @staticmethod
    def validate_first(first: Optional[str]) -> Optional[str]:
        return Default.first if not first or first.isdigit() is not True else first

    @staticmethod
    def validate_show(show: List[str]) -> List[str]:
        data = [True] if 'none' in show else [valid for valid in show if
                                              valid in Default.show_validation]
        return Default.show_validation if not data else data

    @staticmethod
    def validate_count(count: bool) -> bool:
        return Default.count if not count or count is True else True

    @staticmethod
    def validate_download(download: bool) -> bool:
        return Default.download if not download or download is True else True
