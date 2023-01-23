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


class DisplayFileNotFoundError(Exception):
    pass


class FilterLogicalOperatorError(Exception):
    pass


class TypeIDError(Exception):
    pass


class LastEntityError(Exception):
    pass


class WrongOperatorError(Exception):
    pass


class InvalidSearchSyntax(Exception):
    pass


class ValueNotIntegerError(Exception):
    pass


class NotAPlaceError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "title": "Internal Server Error",
        "timestamp": datetime.datetime.now(),
        "status": 500},
    "EntityDoesNotExistError": {
        "message": "requested entity does not exist",
        "title": "Entity Does Not Exist Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "FilterOperatorError": {
        "message": "Filter operator is wrong.",
        "title": "Filter Operation Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "FilterLogicalOperatorError": {
        "message": "Filter logical operator is wrong.",
        "title": "Filter Logical Operation Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSearchDateError": {
        "message": "The search term must be a valid date e.g. 2020-01-01."
                   " A valid date contains yyyy-mm-dd.",
        "title": "Invalid Search Date Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSearchNumberError": {
        "message": "The search term must be a valid number.",
        "title": "Invalid Search Number Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidCidocClassCode": {
        "message": "This is not a valid CIDOC CRM class code."
                   " Please confer the model.",
        "title": "Invalid Cidoc Class Code",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidLimitError": {
        "message": "Only integers between 1 and 100 are allowed.",
        "title": "Invalid Limit Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSubunitError": {
        "message": "The requested ID is not a node/subunit or doesn't exist."
                   " Try another node ID",
        "title": "Invalid Subunit Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidCodeError": {
        "message": "The code is not valid. Valid codes are: actor, event, "
                   "place, source, reference and object."
                   " For further usage, please confer the help page.",
        "title": "Invalid Code Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSystemClassError": {
        "message": "System class is not valid. For further usage,"
                   " please confer the help page.",
        "title": "Invalid System Class Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "NoSearchStringError": {
        "message": "The filter parameter has no search string.",
        "title": "No Search String Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "AccessDeniedError": {
        "message": "You don't have access to the API."
                   " Please ask the owner for access.",
        "title": "Access Denied Error",
        "timestamp": datetime.datetime.now(),
        "status": 403},
    "QueryEmptyError": {
        "message": "Query path needs one or more parameter:"
                   " classes, codes or entities.",
        "title": "Query Empty Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "ResourceGoneError": {
        "message": "This resource is gone.",
        "title": "Resource Gone Error",
        "timestamp": datetime.datetime.now(),
        "status": 410},
    "NoEntityAvailable": {
        "message": "No entity exist for this category.",
        "title": "No Entity Available",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "FilterColumnError": {
        "message": "Column name doesn't exist.",
        "title": "Filter Column Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "FilterDelimiterError": {
        "message": "Filter delimiter are wrong.",
        "title": "Filter Delimiter Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "TypeIDError": {
        "message": "One type ID is wrong.",
        "title": "Type ID Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "LastEntityError": {
        "message": "The ID is the last entity, please choose another ID",
        "title": "Last ID Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "WrongOperatorError": {
        "message": "The used operator is not available within this category",
        "title": "Wrong Operator Error",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "InvalidSearchSyntax": {
        "message":
            "The search syntax contains errors. Please read the manual.",
        "title": "Incorrect search syntax",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "ValueNotIntegerError": {
        "message": "The value is not a valid integer.",
        "title": "Not valid integer",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "NotAPlaceError": {
        "message": "The give ID is not a place. Please provide a valid place "
                   "ID",
        "title": "ID is not a place",
        "timestamp": datetime.datetime.now(),
        "status": 404},
    "DisplayFileNotFoundError": {
        "message": "For the given ID not file could be retrieved",
        "title": "File not found",
        "timestamp": datetime.datetime.now(),
        "status": 404}
}
