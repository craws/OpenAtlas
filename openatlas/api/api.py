from flask import Blueprint, render_template, send_file
from flask_cors import CORS
from flask_restful import Api

from openatlas import app
from openatlas.api.api_v04.routes import routes
from openatlas.api.api_v1.routes import api_v1_files, api_v1_lod, \
    api_v1_loud, api_v1_root, api_v1_system, api_v1_vocabulary
from openatlas.api.api_v1.routes.metadata import api_v1_metadata

app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ALLOWANCE']}})

app.register_api(api_v1_root)
app.register_api(api_v1_system)
app.register_api(api_v1_vocabulary)
app.register_api(api_v1_lod)
app.register_api(api_v1_loud)
app.register_api(api_v1_files)
app.register_api(api_v1_metadata)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
for route in routes:
    api.add_resource(route[0], route[1], endpoint=route[2])
app.register_blueprint(blueprint)

blueprint_04 = Blueprint('api_04', __name__, url_prefix='/api/0.4')
api_04 = Api(blueprint_04)
for route in routes:
    api_04.add_resource(route[0], route[1], endpoint=route[2])
app.register_blueprint(blueprint_04)


@app.route('/openapi.json')
def get_openapi_json():
    openapi_file = app.config['OPENAPI_FILE']
    if app.config['OPENAPI_INSTANCE_FILE'].exists():
        openapi_file = app.config['OPENAPI_INSTANCE_FILE']
    return send_file(openapi_file, mimetype='application/json')


@app.route('/swagger')
def get_swagger_ui():
    return render_template("swagger.html")
