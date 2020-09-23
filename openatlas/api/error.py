from datetime import datetime
from typing import Dict

from flask import request


class APIError(Exception):
    status_code = 400

    error_detail = {
        "400": "The request is invalid. The body or parameters are wrong.",
        "401": "You failed to authenticate with the server.",
        "403": "You don't have the permission to access the requested resource. "
                   "Please authenticate with the server, either through login via the "
                   "user interface or token based authentication.",
        "404": "Something went wrong! Maybe only digits are allowed. Please check the URL",
        "404a":  "The requested entity doesn't exist. Try another ID",
        "404b": "The syntax is incorrect. Only digits are allowed. "
                      "For further usage, please confer the help page",
        "404c": "The syntax is incorrect. Valid codes are: actor, event, place, source,"
                      " reference and object. For further usage, please confer the help page.",
        "404d": "The syntax is incorrect. These class code is not supported. "
                      "For the classes please confer the model.",
        "404e": "The syntax is incorrect. Only integers between 1 and 100 are allowed.",
        "404f": "The syntax is incorrect. Only valid operators are allowed.",
        "405": "The method used is not supported. Right now only GET is allowed.",
        "500": "Please notify the administrator. Sorry for the inconvenience."}

    def __init__(self, message: str, status_code: int, payload: str) -> None:
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.error_code = status_code

    def to_dict(self) -> Dict[str, str]:
        rv = {'title': self.message,
              'status': str(self.status_code),
              'intern-status': self.payload,
              'detail': str(self.error_detail[self.payload]),
              'instance': request.base_url,
              'timestamp': str(datetime.now())}
        if self.status_code in [403, 401]:
            rv['wiki'] = "https://redmine.openatlas.eu/projects/uni/wiki/API_Authentication"
        else:
            rv['wiki'] = "https://redmine.openatlas.eu/projects/uni/wiki/Api"
        return rv
