from flasgger import Swagger
from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api

from openatlas import app
from openatlas.api.routes_2 import add_routes_v02
from openatlas.api.v02.resources.error import errors as error_v02
from openatlas.api.v03.resources.error import errors
from openatlas.api.routes_3 import add_routes_v03

app.config['SWAGGER'] = {
    'openapi': '3.0.2',
    'uiversion': 3,
    "swagger_version": "2.0",
    "specs": [{
        "version": "0.2",
        "title": "OpenAtlas Api",
        "termsOfService":
            "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html",
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
        "endpoint": '02',
        "description": 'This a deprecated version of the OpenAtlas API',
        "route": '/swagger/02',
        "rule_filter": lambda rule: rule.endpoint.startswith('api_02')}, {
        "version": "0.3",
        "title": "OpenAtlas Api",
        "termsOfService":
            "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html",
        "description": 'This is the stable version of the OpenAtlas API',
        "endpoint": '03',
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
        "route": '/swagger/03',
        "rule_filter": lambda rule: rule.endpoint.startswith('api_03')}],
    "specs_route": "/swagger/"}

CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ALLOWANCE']}})

Swagger(app, parse=False, template_file="api/swagger.json")

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, catch_all_404s=False, errors=errors)
add_routes_v03(api)
app.register_blueprint(api_bp)

api_bp_02 = Blueprint('api_02', __name__, url_prefix='/api/0.2')
api_02 = Api(api_bp_02, catch_all_404s=False, errors=error_v02)
add_routes_v02(api_02)
app.register_blueprint(api_bp_02)

api_bp_03 = Blueprint('api_03', __name__, url_prefix='/api/0.3')
api_03 = Api(api_bp_03, catch_all_404s=False, errors=errors)
add_routes_v03(api_03)
app.register_blueprint(api_bp_03)
