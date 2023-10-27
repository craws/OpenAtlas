from flasgger import Swagger
from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api

from openatlas import app
from openatlas.api.routes import add_routes_v03

app.config['SWAGGER'] = {
    'openapi': '3.0.2',
    'uiversion': 3,
    "swagger_version": "2.0",
    "specs": [{
        "endpoint": '03',
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
        "route": '/swagger/03',
        "rule_filter": lambda rule: rule.endpoint.startswith('api_03')},{
        "endpoint": '04',
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
        "route": '/swagger/04',
        "rule_filter": lambda rule: rule.endpoint.startswith('api_03')}],
    "specs_route": "/swagger/"}

app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ALLOWANCE']}})

Swagger(app, parse=False, template_file="api/swagger.json")

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)
add_routes_v03(api)
app.register_blueprint(api_bp)

api_bp_03 = Blueprint('api_03', __name__, url_prefix='/api/0.3')
api_03 = Api(api_bp_03)
add_routes_v03(api_03)
app.register_blueprint(api_bp_03)
