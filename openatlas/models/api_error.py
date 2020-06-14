from datetime import datetime
from typing import Dict

from flask import jsonify, request


class APIError(Exception):
    status_code = "400"
    error_code = "200"

    error_detail = {
        "400": [400, "The request is invalid. The body or parameters are wrong."],
        "401": [401, "You failed to authenticate with the server."],
        "403": [403, "You don't have the permission to access the requested resource. "
                   "Please authenticate with the server, either through login via the "
                   "user interface or token based authentication."],
        "404": [404, "Something went wrong! Maybe only digits are allowed. Please check the URL"],
        "404a": [404, "The requested entity doesn't exist. Try another ID"],
        "404b": [404, "The syntax is incorrect. Only digits are allowed. "
                      "For further usage, please confer the help page"],
        "404c": [404, "The syntax is incorrect. Valid codes are: actor, event, place, source,"
                      " reference and object. For further usage, please confer the help page"],
        "404d": [404, "The syntax is incorrect. This class code is not supported. "
                      "For the classes please confer the model"],
        "404e": [404, "The syntax is incorrect. Only integers between 1 and 100 are allowed."],
        "405": [405, "The method used is not supported. Right now only GET is allowed."],
        "500": [500, "Please notify the administrator. Sorry for the inconvenience!"]}

    def __init__(self, message: str, status_code: str, payload: None = None) -> None:
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.error_code = status_code

    def to_dict(self) -> Dict[str, str]:
        rv = dict(self.payload or ())
        rv['title'] = self.message
        rv['status'] = str(self.error_detail[self.error_code][0])
        rv['intern-status'] = self.error_code
        rv['detail'] = str(self.error_detail[self.error_code][1])
        rv['instance'] = request.base_url
        rv['timestamp'] = str(datetime.now())
        if self.error_code in ["403", "401"]:
            rv['help'] = "https://redmine.craws.net/projects/uni/wiki/API_Authentication"
        else:
            rv['help'] = "https://redmine.craws.net/projects/uni/wiki/Api"

        return jsonify(rv)
