import datetime


class InternalServerError(Exception):
    pass


class EntityDoesNotExistError(Exception):
    pass


class FilterOperatorError(Exception):
    pass


class InvalidSearchDateError(Exception):
    pass


class InvalidSearchNumberError(Exception):
    pass


class InvalidCidocClassCode(Exception):
    pass


class InvalidLimitError(Exception):
    pass


class InvalidSubunitError(Exception):
    pass


class InvalidCodeError(Exception):
    pass


class InvalidSystemClassError(Exception):
    pass


class NoSearchStringError(Exception):
    pass


class AccessDeniedError(Exception):
    pass


class MethodNotAllowedError(Exception):
    pass


class QueryEmptyError(Exception):
    pass


class ResourceGoneError(Exception):
    pass


class NoEntityAvailable(Exception):
    pass


class FilterColumnError(Exception):
    pass


class FilterDelimiterError(Exception):
    pass


class FilterLogicalOperatorError(Exception):
    pass


class TypeIDError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",

        "timestamp": datetime.datetime.now(),
        "status": 500},
    "EntityDoesNotExistError": {
        "message": "requested entity does not exist",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "FilterOperatorError": {
        "message": "Filter operator is wrong.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "FilterLogicalOperatorError": {
        "message": "Filter logical operator is wrong.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSearchDateError": {
        "message": "The search term must be a valid date e.g. 2020-01-01."
                   " A valid date contains yyyy-mm-dd.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSearchNumberError": {
        "message": "The search term must be a valid number.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidCidocClassCode": {
        "message": "This is not a valid CIDOC CRM class code."
                   " Please confer the model.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidLimitError": {
        "message": "Only integers between 1 and 100 are allowed.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSubunitError": {
        "message": "The requested ID is not a node/subunit or doesn't exist."
                   " Try another node ID",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidCodeError": {
        "message": "The code is not valid. Valid codes are: actor, event, "
                   "place, source, reference and object."
                   " For further usage, please confer the help page.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSystemClassError": {
        "message": "System class is not valid. For further usage,"
                   " please confer the help page.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "NoSearchStringError": {
        "message": "The filter parameter has no search string.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "AccessDeniedError": {
        "message": "You don't have access to the API."
                   " Please ask the owner for access.",

        "timestamp": datetime.datetime.now(),
        "status": 403},
    "MethodNotAllowedError": {
        "message": "This method is not allowed for this path."
                   " Please confer the manual.",

        "timestamp": datetime.datetime.now(),
        "status": 405},
    "QueryEmptyError": {
        "message": "Query path needs one or more parameter:"
                   " classes, codes or entities.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "ResourceGoneError": {
        "message": "This resource is gone.",

        "timestamp": datetime.datetime.now(),
        "status": 410},
    "NoEntityAvailable": {
        "message": "No entity exist for this category.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "FilterColumnError": {
        "message": "Column name doesn't exist.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "FilterDelimiterError": {
        "message": "Filter delimiter are wrong.",

        "timestamp": datetime.datetime.now(),
        "status": 404},
    "TypeIDError": {
        "message": "One type ID is wrong.",

        "timestamp": datetime.datetime.now(),
        "status": 404}
}
