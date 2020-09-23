import re
from typing import Any, Dict, List, Optional, Union


class Default:
    limit: int = 20
    sort: str = 'ASC'
    filter: str = ''
    column: str = 'name'


class Validation:
    default = {'last': None,
               'first': None,
               'show': ['when', 'types', 'relations', 'names', 'links', 'geometry', 'depictions'],
               'count': False,
               'subtype': False}
    column = ['id', 'class_code', 'name', 'description', 'created', 'modified', 'system_type',
              'begin_from', 'begin_to', 'end_from', 'end_to']
    operators = ['eq', 'ne', 'lt', 'le', 'gt', 'ge', 'and', 'or', 'not', 'contains', 'startsWith',
                 'in', 'match']
    operators_dict = {'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>', 'ge': '>=',
                      'and': 'AND', 'or': 'OR', 'onot': 'OR NOT', 'anot': 'AND NOT', 'like': 'LIKE',
                      'in': 'IN'}

    @staticmethod
    def validate_url_query(query: Any) -> Dict[str, Any]:
        query = {'filter': Validation.validate_filter(query.get('filter')),
                 'limit': Validation.validate_limit(query.get('limit')),
                 'sort': Validation.validate_sort(query.get('sort')),
                 'column': Validation.validate_column(query.get('column')),
                 'last': Validation.validate_last(query.getlist('last')),
                 'first': Validation.validate_first(query.getlist('first')),
                 'show': Validation.validate_show(query.getlist('show')),
                 'count': Validation.validate_count(query.getlist('count')),
                 'subtype': Validation.validate_subtype(query.get('subtype'))}
        return query

    @staticmethod
    def validate_filter(filter_: str) -> str:
        if not filter_:
            return Default.filter

        filter_query = ''
        for item in re.findall(r'(\w+)\((.*?)\)', filter_):
            operator = item[0].lower()
            if operator in Validation.operators_dict:
                filter_query += Validation.operators_dict[operator]
                item = re.split('[,]', item[1])
                if item[0] in Validation.operators_dict and item[1] in Validation.column:
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
                                    + Validation.operators_dict[item[0]] + ' ' + item[2] + ' '
        return filter_query

    @staticmethod
    def validate_limit(limit: Optional[str] = None) -> int:
        return int(limit) if limit and limit.isdigit() else Default.limit

    @staticmethod
    def validate_sort(sort: Optional[str] = None) -> str:
        return Default.sort if not sort or sort.lower() != 'desc' else 'DESC'

    @staticmethod
    def validate_column(column: Optional[str]) -> str:
        return Default.column if not column and column.lower() in Validation.column else column

    @staticmethod
    def validate_last(last: List[Any]) -> Union[bool, List[str], str, None]:
        last_ = [Validation.default['last']]
        if last:
            for item in last:
                if item.isdigit():
                    last_ = [item]
        return last_[0]

    @staticmethod
    def validate_first(first: List[Any]) -> Union[bool, List[str], str, None]:
        first_ = [Validation.default['first']]
        if first:
            for item in first:
                if item.isdigit():
                    first_ = [item]
        return first_[0]

    @staticmethod
    def validate_show(show: List[str]) -> List[str]:
        show_ = []
        valid = ['when', 'types', 'relations', 'names', 'links', 'geometry', 'depictions']
        for pattern in valid:
            if re.search(pattern, str(show)):
                show_.append(pattern)
        if not show_:
            show_.extend(valid)
        if 'none' in show:
            show_.clear()
        return show_

    @staticmethod
    def validate_count(count: bool) -> bool:
        count_ = False
        if count:
            count_ = True
        return count_

    @staticmethod
    def validate_subtype(subtype: str) -> bool:
        subtype_ = True if subtype == 'show' else False
        return subtype_
