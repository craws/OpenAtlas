from werkzeug.datastructures import ImmutableMultiDict
import re


class Validation:
    default = {'filter': '', 'limit': '20', 'sort': 'ASC', 'column': 'name'}
    column = ['id', 'class_code', 'name', 'description', 'created', 'modified', 'system_type',
              'begin_from', 'begin_to', 'end_from', 'end_to']
    operators = ['eq', 'ne', 'lt', 'le', 'gt', 'ge', 'and', 'or', 'not', 'contains', 'startsWith',
                 'in', 'match']

    @staticmethod
    def validate_url_query(query):
        query = {'filter': Validation.validate_filter(query.getlist('filter')),
                 'limit': Validation.validate_limit(query.getlist('limit')),
                 'sort': Validation.validate_sort(query.getlist('sort')),
                 'column': Validation.validate_column(query.getlist('column'))}

        return query

    @staticmethod
    def validate_filter(filter):
        filter = re.findall(r'\(.*?\)', ''.join(filter))
        print(type(filter))
        for item in filter:
            print(item)
            if item[0] in Validation.operators and item[1] in Validation.column:
                print(item)
            else:
                filter = Validation.default['filter']
        return Validation.default['filter']

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
