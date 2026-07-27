from flasgger import Swagger
from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api

from openatlas import app
from openatlas.api.routes import routes

app.config['SWAGGER'] = {
    'openapi': '3.0.2',
    'uiversion': 3,
    "swagger_version": "2.0",
    "specs": [{
        "endpoint": 'openapi_04',
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
        "route": '/openapi.json',
        "rule_filter": lambda rule: rule.endpoint.startswith('api_04')}],
    "specs_route": "/swagger/"}

app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ALLOWANCE']}})

openapi_file = app.config['OPENAPI_FILE']
if app.config['OPENAPI_INSTANCE_FILE'].exists():
    openapi_file = app.config['OPENAPI_INSTANCE_FILE']
Swagger(app, parse=False, template_file=str(openapi_file))

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
