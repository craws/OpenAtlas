import json
from typing import Any, Dict, List, Type, Union

from flask import Response
from flask_restful import marshal
from flask_restful.fields import List as RestList, String

from openatlas.models.entity import Entity


class Download:

    @staticmethod
    def download(data: Union[List[Dict[str, Any]], Dict[str, Any], List[Entity]],
                 template: Union[Dict[str, Type[String]], Dict[str, RestList]],
                 name: Union[str, int]):
        return Response(json.dumps(marshal(data, template)),
                        mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=' + str(name) + '.json'})
