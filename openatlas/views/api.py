# Created by Alexander Watzinger and others. Please see README.md for licensing information


from flask import render_template, json

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.util.util import required_group


@app.route('/api/<version>/entity/<int:id_>')
@required_group('manager')
def api_entity(version: str, id_: int) -> str:
    entity = EntityMapper.get_by_id(id_)
    data = {"Entity": {'id': entity.id, 'name': entity.name}}
    return json.dumps(data)


@app.route('/api')
@required_group('manager')
def api_index() -> str:

    return render_template('api/index.html')