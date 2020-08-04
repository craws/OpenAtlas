import re

from typing import Any, Dict, List, Sequence, Union



class Validation:
    default = {'filter': '', 'limit': '20', 'sort': 'ASC', 'column': 'name', 'last': None,
               'first': None}
    column = ['id', 'class_code', 'name', 'description', 'created', 'modified', 'system_type',
              'begin_from', 'begin_to', 'end_from', 'end_to']
    operators = ['eq', 'ne', 'lt', 'le', 'gt', 'ge', 'and', 'or', 'not', 'contains', 'startsWith',
                 'in', 'match']
    operators_dict = {'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>', 'ge': '>=',
                      'and': 'AND', 'or': 'OR', 'onot': 'OR NOT', 'anot': 'AND NOT', 'like': 'LIKE',
                      'in': 'IN'}

    @staticmethod
    def validate_url_query(query: Any) -> Dict[str, Any]:
        query = {'filter': Validation.validate_filter(query.getlist('filter')),
                 'limit': Validation.validate_limit(query.getlist('limit')),
                 'sort': Validation.validate_sort(query.getlist('sort')),
                 'column': Validation.validate_column(query.getlist('column')),
                 'last': Validation.validate_last(query.getlist('last')),
                 'first': Validation.validate_first(query.getlist('first'))}
        return query

    @staticmethod
    def validate_filter(filter_: str) -> str:
        filter_ = re.findall(r'(\w+)\((.*?)\)', ''.join(filter_))
        filter_query = ''
        for item in filter_:
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
    def validate_limit(limit: list) -> str:
        limit_ = []
        if limit:
            for item in limit:
                if item.isdigit():
                    limit_.append(item)
        else:
            limit_.append(Validation.default['limit'])
        return limit_[0]

    @staticmethod
    def validate_sort(sort: list) -> str:
        sort_ = []
        if sort:
            for item in reversed(sort):
                if isinstance(item, str) and item.lower() in ['asc', 'desc']:
                    sort_.append(item)
        else:
            sort_.append(Validation.default['sort'])
        return sort_[0]

    @staticmethod
    def validate_column(column: list) -> List[str]:
        column_ = []
        if column:
            for item in column:
                if isinstance(item, str) and item.lower() in Validation.column:
                    column_.append(item)
        else:
            column_.append(Validation.default['column'])
        return column_

    @staticmethod
    def validate_last(last: list) -> List[str]:
        last_ = []
        if last:
            for item in last:
                if item.isdigit():
                    last_.append(item)
        else:
            last_.append(Validation.default['last'])
        return last_[0]

    @staticmethod
    def validate_first(first: list) -> List[str]:
        first_ = []
        if first:
            for item in first:
                if item.isdigit():
                    first_.append(item)
        else:
            first_.append(Validation.default['first'])
        return first_[0]
