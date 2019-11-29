from pprint import pprint

from flask import json, render_template

from openatlas import app
from openatlas.models.api import Api
from openatlas.util.util import required_group


@app.route('/api/0.1/entity/<int:id_>')
@required_group('manager')
def api_entity(id_: int) -> str:
    # pprint(Api.get_entity(id_))
    return json.dumps(Api.get_entity(id_=id_))


@app.route('/api')
@required_group('manager')
def api_index() -> str:
    return render_template('api/index.html')
