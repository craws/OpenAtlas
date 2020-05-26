from typing import Dict, Tuple

from flask import request


class APIError(Exception):
    status_code = 400
    error_code = 200

    error_detail = {
        400: "The request ist invalid. The body or parameters are wrong."
             " Please confer https://redmine.craws.net/projects/uni/wiki/Api",
        401: "You failed to authenticate with the server."
             " Please confer https://redmine.craws.net/projects/uni/wiki/API_Authentication",
        403: "You don't have the permission to access the requested resource."
             " Please authenticate with the server, either through login via the unser interface or"
             " token based authentication. Please confer"
             " https://redmine.craws.net/projects/uni/wiki/API_Authentication",
        404: "The requested entity doesn't exist. Try another ID"}

    def __init__(self, message: str, status_code: int, payload: None = None) -> None:
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.error_code = status_code

    def to_dict(self) -> Dict[str, str]:
        rv = dict(self.payload or ())
        rv['title'] = self.message
        rv['status'] = self.error_code
        rv['detail'] = self.error_detail[self.error_code]
        rv['instance'] = request.base_url
        return rv
