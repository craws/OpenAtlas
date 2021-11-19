from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api

from openatlas import app
from openatlas.api.v03.resources.error import errors
from openatlas.api.routes import add_routes
from openatlas.api.v02.resources.error import errors as error_v02
from openatlas.api.v02.routes_02 import add_routes_v02
from openatlas.api.v03.routes_03 import add_routes_v03

app.config['SWAGGER'] = {'openapi': '3.0.2', 'uiversion': 3}

cors = CORS(
    app,
    resources={r"/api/*": {"origins": app.config['CORS_ALLOWANCE']}})
api_bp = Blueprint('api', __name__, url_prefix='/api')
api_bp_02 = Blueprint('api_02', __name__, url_prefix='/api/0.2')
api_bp_03 = Blueprint('api_03', __name__, url_prefix='/api/0.3')

api = Api(
    api_bp,
    catch_all_404s=False,
    errors=errors)  # Establish connection between API and APP
api_02 = Api(
    api_bp_02,
    catch_all_404s=False,
    errors=error_v02)
api_03 = Api(
    api_bp_03,
    catch_all_404s=False,
    errors=errors)

add_routes(api)
app.register_blueprint(api_bp)
add_routes_v02(api_02)
app.register_blueprint(api_bp_02)
add_routes_v03(api_03)
app.register_blueprint(api_bp_03)