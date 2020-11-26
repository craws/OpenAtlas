import json

from flask import Response
from flask_restful import marshal
from typing import Any, Dict, List, Type, Union

from flask_restful.fields import String


class Download:

    @staticmethod
    def download(data: List[List[Dict[str, Any]]], template: Dict[str, Type[String]], name: Union[str, int]):
        return Response(json.dumps(marshal(data, template)),
                        mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=' + str(name) + '.json'})
