class AccessDeniedError(Exception):
    pass


class DisplayFileNotFoundError(Exception):
    pass


class EntityDoesNotExistError(Exception):
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


class LogicalOperatorError(Exception):
    pass


class NoEntityAvailable(Exception):
    pass


class NoLicenseError(Exception):
    pass


class NoSearchStringError(Exception):
    pass


class NotATypeError(Exception):
    pass


class NotAPlaceError(Exception):
    pass


class OperatorError(Exception):
    pass


class QueryEmptyError(Exception):
    pass


class SearchCategoriesError(Exception):
    pass


class TypeIDError(Exception):
    pass


class ValueNotIntegerError(Exception):
    pass
