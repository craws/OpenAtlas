import datetime
from typing import Any, Dict, List, Union

from openatlas.api.v02.resources.error import FilterOperatorError, InvalidSearchDateError, \
    InvalidSearchNumberError, NoSearchStringError


class Validation:
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
    def get_filter_from_url_parameter(filter_: List[str]) -> List[List[str]]:
        checked_filter = []
        for f in filter_:
            values = f.split('|')
            for value in values:
                if not value:
                    raise FilterOperatorError  # pragma: no cover
            if not values[3]:
                raise NoSearchStringError  # pragma: no cover
            if values[0] in Validation.logical_operators.keys() \
                    and values[1] in Validation.valid_columns \
                    and values[2] in Validation.compare_operators.keys():
                checked_filter.append([word for word in f.split('|')])
        return checked_filter

    @staticmethod
    def test_date(term):
        try:
            datetime.datetime.strptime(term, "%Y-%m-%d")
        except InvalidSearchDateError:  # pragma: no cover
            raise InvalidSearchDateError

    @staticmethod
    def test_id(term):
        try:
            int(term)
        except InvalidSearchNumberError:  # pragma: no cover
            raise InvalidSearchNumberError
