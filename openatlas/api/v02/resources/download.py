import json

from flask import Response
from flask_restful import marshal


class Download:

    @staticmethod
    def download(data, template, name):
        return Response(json.dumps(marshal(data, template)),
                        mimetype='application/json',
                        headers={
                            'Content-Disposition': 'attachment;filename=' + str(name) + '.json'})
