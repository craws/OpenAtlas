import re
from typing import Any, Dict, List, Optional

from openatlas.api.error import APIError


class Default:
    limit: int = 20
    sort: str = 'ASC'
    filter: str = ''
    column: str = 'name'
    last: Optional[str] = None
    first: Optional[str] = None
    count: bool = False
    operators_dict: Dict[str, Any] = {'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>',
                                      'ge': '>=', 'and': 'AND', 'or': 'OR', 'onot': 'OR NOT',
                                      'anot': 'AND NOT', 'like': 'LIKE', 'in': 'IN'}
    column_validation: List[str] = ['id', 'class_code', 'name', 'description', 'created', 'end_to',
                                    'modified', 'system_type', 'begin_from', 'begin_to', 'end_from']
    show_validation: List[str] = ['when', 'types', 'relations', 'names', 'links', 'geometry',
                                  'depictions']


class Validation:

    @staticmethod
    def validate_url_query(query: Any) -> Dict[str, Any]:
        query = {'filter': Validation.validate_filter(query.get('filter')),
                 'limit': Validation.validate_limit(query.get('limit')),
                 'sort': Validation.validate_sort(query.get('sort')),
                 'column': Validation.validate_column(query.get('column')),
                 'last': Validation.validate_last(query.get('last')),
                 'first': Validation.validate_first(query.get('first')),
                 'show': Validation.validate_show(query.get('show')),
                 'count': Validation.validate_count(query.getlist('count'))}
        return query

    @staticmethod
    def validate_filter(filter_: str) -> str:
        if not filter_:
            return Default.filter
        filter_query = ''
        for item in re.findall(r'(\w+)\((.*?)\)', filter_):
            operator = item[0].lower()
            if operator in Default.operators_dict:
                filter_query += Default.operators_dict[operator]
                item = re.split('[,]', item[1])
                if item[0] in Default.operators_dict and item[1] in Default.column:
                    if item[0] == 'like':
                        item[2] = '\'' + item[2] + '%%\''
                        item[1] = item[1] + '::text'
                    elif item[0] == 'in':
                        item[2] = item[2].replace('[', '')
                        item[2] = item[2].replace(']', '')
                        if len(list(map(str, item[2].split(':')))) == 1:
                            tmp = list(map(str, item[2].split(':')))
                            item[2] = '(\'' + tmp[0] + '\')'
                        else:
                            item[2] = str(tuple(map(str, item[2].split(':'))))
                    else:
                        item[2] = '\'' + item[2] + '\''
                    filter_query += ' ' + item[1] + ' ' \
                                    + Default.operators_dict[item[0]] + ' ' + item[2] + ' '
                else:
                    raise APIError('Syntax is incorrect!', status_code=404, payload="404f")
        return filter_query

    @staticmethod
    def validate_limit(limit: Optional[str] = None) -> int:
        return int(limit) if limit and limit.isdigit() else Default.limit

    @staticmethod
    def validate_sort(sort: Optional[str] = None) -> str:
        return Default.sort if not sort or sort.lower() != 'desc' else 'DESC'

    @staticmethod
    def validate_column(column: Optional[str]) -> str:
        return Default.column if not column or column.lower() not in Default.column else column

    @staticmethod
    def validate_last(last: Optional[str]) -> str:
        return Default.last if not last or last.isdigit() is not True else last

    @staticmethod
    def validate_first(first: Optional[str]) -> str:
        return Default.first if not first or first.isdigit() is not True else first

    @staticmethod
    def validate_show(show: Optional[str]) -> List[str]:
        show_ = []
        for pattern in Default.show_validation:
            if show and re.search(pattern, show):
                show_.append(pattern)
        if show and 'none' in show:
            show_.clear()
        return Default.show_validation if not show_ else show_

    @staticmethod
    def validate_count(count: bool) -> bool:
        return Default.count if not count or count is True else True
