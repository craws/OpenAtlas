from werkzeug.datastructures import ImmutableMultiDict
import re


class Validation:
    default = {'filter': '', 'limit': '20', 'sort': 'ASC', 'column': 'name'}
    column = ['id', 'class_code', 'name', 'description', 'created', 'modified', 'system_type',
              'begin_from', 'begin_to', 'end_from', 'end_to']
    operators = ['eq', 'ne', 'lt', 'le', 'gt', 'ge', 'and', 'or', 'not', 'contains', 'startsWith',
                 'in', 'match']
    operators_dict = {'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>', 'ge': '>=',
                      'and': 'AND', 'or': 'OR', 'onot': 'OR NOT', 'anot': 'AND NOT',
                      'contains': 'CONTAINS', 'like': 'LIKE', 'in': 'IN'}

    @staticmethod
    def validate_url_query(query):
        query = {'filter': Validation.validate_filter(query.getlist('filter')),
                 'limit': Validation.validate_limit(query.getlist('limit')),
                 'sort': Validation.validate_sort(query.getlist('sort')),
                 'column': Validation.validate_column(query.getlist('column'))}
        return query

    @staticmethod
    def validate_filter(filter):
        filter = re.findall(r'(\w+)\((.*?)\)', ''.join(filter))
        filter_query = ''
        for item in filter:
            operator = item[0].lower()
            if operator in Validation.operators_dict:
                filter_query += Validation.operators_dict[operator]
                item = re.split('[,]', item[1])
                if item[0] in Validation.operators_dict and item[1] in Validation.column:
                    if item[0] == 'like':
                        item[2] = '\'' + item[2] + '%%\''
                        item[1] = item[1] + '::text'
                    if item[0] == 'in':
                        # remove [] and get all values between : re.split(':', item[2])
                        pass
                    filter_query += ' ' + item[1] + ' ' \
                                    + Validation.operators_dict[item[0]] + ' ' + item[2] + ' '

                else:
                    filter_query = Validation.default['filter']
            else:
                filter_query = Validation.default['filter']
        print(filter_query)
        return filter_query

    @staticmethod
    def validate_limit(limit):
        limit_ = []
        if limit:
            for item in limit:
                if item.isdigit():
                    limit_.append(item)
        else:
            limit_.append(Validation.default['limit'])
        if not limit_:
            limit_.append(Validation.default['limit'])
        return limit_[0]

    @staticmethod
    def validate_sort(sort):
        sort_ = []
        if sort:
            for item in reversed(sort):
                if isinstance(item, str) and item.lower() in ['asc', 'desc']:
                    sort_.append(item)
        else:
            sort_.append(Validation.default['sort'])
        if not sort_:
            sort_.append(Validation.default['sort'])
        return sort_[0]

    @staticmethod
    def validate_column(column):
        column_ = []
        if column:
            for item in column:
                if isinstance(item, str) and item.lower() in Validation.column:
                    column_.append(item)
        else:
            column_.append(Validation.default['column'])
        if not column_:
            column_.append(Validation.default['column'])
        return column_
