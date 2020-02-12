from pprint import pprint

from flask import json, render_template, request

from openatlas import app
from openatlas.models.api import Api
from openatlas.util.util import required_group


@app.route('/api/0.1/entity/<int:id_>')
@required_group('manager')
def api_entity(id_: int) -> str:
    # pprint(Api.get_entity(id_))
    return json.dumps(Api.get_entity(id_=id_))


# Todo: Make more versatile.
@app.route('/api/0.1')
@required_group('manager')
def api_test():
    entity = request.args['entity']
    return json.dumps(Api.get_entity(id_=entity))


# Todo: Not finished! Wie kann str übergeben werden? <str: code_> funktioniert nicht!
@app.route('/api/0.1/entity/<code>')
@required_group('manager')
def api_collection(code):
    return json.dumps(Api.get_entity_by_code(code_=code))


@app.route('/api')
@required_group('manager')
def api_index() -> str:
    return render_template('api/index.html')
