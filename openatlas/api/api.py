from flasgger import Swagger
from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api

from openatlas import app
from openatlas.api.routes import (
    entity_routes,  display_routes, type_routes, admin_routes, special_routes)


app.config['SWAGGER'] = {
    'openapi': '3.0.2',
    'uiversion': 3,
    "swagger_version": "2.0",
    # Specs doesn't work this way. Remodel everything:
    # https://github.com/flasgger/flasgger/blob/master/examples/example_app.py
    "specs": [{
        "endpoint": '04',
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
        "route": '/openapi.json',
        "rule_filter": lambda rule: rule.endpoint.startswith('api_04')}, {
        "endpoint": '03',
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
        "route": '/openapi.json',
        "rule_filter": lambda rule: rule.endpoint.startswith('api_03')}],
    "specs_route": "/swagger/"}

app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ALLOWANCE']}})

Swagger(app, parse=False, template_file="api/openapi.json")

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)
entity_routes(api)
display_routes(api)
type_routes(api)
admin_routes(api)
special_routes(api)
app.register_blueprint(api_bp)

api_bp_04 = Blueprint('api_04', __name__, url_prefix='/api/0.4')
api_04 = Api(api_bp_04)
entity_routes(api_04)
display_routes(api_04)
type_routes(api_04)
admin_routes(api_04)
special_routes(api_04)
app.register_blueprint(api_bp_04)
