from flasgger import Swagger
from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api

from openatlas import app
from openatlas.api.v02.endpoints.content.class_mapping import ClassMapping
from openatlas.api.v02.endpoints.content.content import GetContent
from openatlas.api.v02.endpoints.content.geometric_entities import \
    GetGeometricEntities
from openatlas.api.v02.endpoints.content.overview_count import OverviewCount
from openatlas.api.v02.endpoints.content.systemclass_count import \
    SystemClassCount
from openatlas.api.v02.endpoints.display_image import DisplayImage
from openatlas.api.v02.endpoints.entity.class_ import GetByClass
from openatlas.api.v02.endpoints.entity.code import GetByCode
from openatlas.api.v02.endpoints.entity.entity import GetEntity
from openatlas.api.v02.endpoints.entity.latest import GetLatest
from openatlas.api.v02.endpoints.entity.linked_entities import GetLinkedEntities
from openatlas.api.v02.endpoints.entity.query import GetQuery
from openatlas.api.v02.endpoints.entity.system_class import GetBySystemClass
from openatlas.api.v02.endpoints.entity.type_entities import GetTypeEntities
from openatlas.api.v02.endpoints.entity.type_entities_all import \
    GetTypeEntitiesAll
from openatlas.api.v02.endpoints.node.node_entities import GetNodeEntities
from openatlas.api.v02.endpoints.node.node_entities_all import \
    GetNodeEntitiesAll
from openatlas.api.v02.endpoints.node.node_overview import GetNodeOverview
from openatlas.api.v02.endpoints.node.subunit import GetSubunit
from openatlas.api.v02.endpoints.node.subunit_hierarchy import \
    GetSubunitHierarchy
from openatlas.api.v02.endpoints.node.type_tree import GetTypeTree
from openatlas.api.v02.resources.error import errors

app.config['SWAGGER'] = {'openapi': '3.0.2', 'uiversion': 3}

cors = CORS(
    app,
    resources={r"/api/*": {"origins": app.config['CORS_ALLOWANCE']}})
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, catch_all_404s=False, errors=errors)  # Establish connection between API and APP
swagger = Swagger(app, parse=False, template_file="api/v02/swagger.json")
# swagger = Swagger(app, parse=False, template=template)

api.add_resource(GetByCode, '/0.2/code/<string:code>', endpoint="code")
api.add_resource(GetByClass, '/0.2/class/<string:class_code>', endpoint="class")
api.add_resource(GetEntity, '/0.2/entity/<int:id_>', endpoint='entity')
api.add_resource(GetLatest, '/0.2/latest/<int:latest>', endpoint="latest")
api.add_resource(GetQuery, '/0.2/query/', endpoint="query")
api.add_resource(
    GetBySystemClass,
    '/0.2/system_class/<string:system_class>',
    endpoint="system_class")
api.add_resource(
    GetTypeEntities,
    '/0.2/type_entities/<int:id_>',
    endpoint="type_entities")
api.add_resource(
    GetTypeEntitiesAll,
    '/0.2/type_entities_all/<int:id_>',
    endpoint="type_entities_all")
api.add_resource(
    GetGeometricEntities,
    '/0.2/geometric_entities/',
    endpoint="geometric_entities")
api.add_resource(
    GetLinkedEntities, '/0.2/entities_linked_to_entity/<int:id_>',
    endpoint="entities_linked_to_entity")

api.add_resource(
    GetNodeEntities,
    '/0.2/node_entities/<int:id_>',
    endpoint="node_entities")
api.add_resource(GetNodeEntitiesAll, '/0.2/node_entities_all/<int:id_>',
                 endpoint="node_entities_all")
api.add_resource(
    GetNodeOverview,
    '/0.2/node_overview/',
    endpoint="node_overview")
api.add_resource(GetSubunit, '/0.2/subunit/<int:id_>', endpoint="subunit")
api.add_resource(
    GetSubunitHierarchy,
    '/0.2/subunit_hierarchy/<int:id_>',
    endpoint="subunit_hierarchy")
api.add_resource(GetTypeTree, '/0.2/type_tree/', endpoint="type_tree")

api.add_resource(GetContent, '/0.2/content/', endpoint="content")
api.add_resource(
    OverviewCount,
    '/0.2/overview_count/',
    endpoint='overview_count')  # Deprecated
api.add_resource(ClassMapping, '/0.2/classes/', endpoint='class_mapping')
api.add_resource(
    SystemClassCount,
    '/0.2/system_class_count/',
    endpoint='system_class_count')

api.add_resource(DisplayImage, '/display/<path:filename>', endpoint='display')

app.register_blueprint(api_bp)
