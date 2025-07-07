from typing import Any


class AccessDeniedError(Exception):
    pass


class DisplayFileNotFoundError(Exception):
    pass


class EntityDoesNotExistError(Exception):
    pass


class EntityNotAnEventError(Exception):
    pass


class InvalidCidocClassCodeError(Exception):
    pass


class InvalidLimitError(Exception):
    pass


class InvalidSearchSyntax(Exception):
    pass


class InvalidSystemClassError(Exception):
    pass


class InvalidViewClassError(Exception):
    pass


class LastEntityError(Exception):
    pass


class InvalidPropertiesError(Exception):
    pass


class LogicalOperatorError(Exception):
    pass


class NoLicenseError(Exception):
    pass


class NotPublicError(Exception):
    pass


class NoSearchStringError(Exception):
    def __init__(self, category: str) -> None:
        super().__init__()
        self.category = category


class NotATypeError(Exception):
    pass


class NotAPlaceError(Exception):
    pass


class OperatorError(Exception):
    pass


class OperatorNotSupported(Exception):
    pass


class QueryEmptyError(Exception):
    pass


class InvalidSearchCategoryError(Exception):
    pass


class InvalidSearchValueError(Exception):
    def __init__(self, category: str, values: Any) -> None:
        super().__init__()
        self.category = category
        self.values = values


class TypeIDError(Exception):
    pass


class ValueNotIntegerError(Exception):
    pass


class UrlNotValid(Exception):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url
