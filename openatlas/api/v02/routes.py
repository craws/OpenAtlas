from flasgger import Swagger
from flask_cors import CORS
from flask_restful import Api

from openatlas import app
from openatlas.api.v02.common.class_ import GetByClass
from openatlas.api.v02.common.code import GetByCode
from openatlas.api.v02.common.content import GetContent
from openatlas.api.v02.common.entity import GetEntity
from openatlas.api.v02.common.latest import GetLatest
from openatlas.api.v02.common.node_entities import GetNodeEntities
from openatlas.api.v02.common.node_entities_all import GetNodeEntitiesAll
from openatlas.api.v02.common.query import GetQuery
from openatlas.api.v02.common.subunit import GetSubunit
from openatlas.api.v02.common.subunit_hierarchy import GetSubunitHierarchy
from openatlas.api.v02.common.usage import ShowUsage
from openatlas.api.v02.resources.error import errors

app.config['SWAGGER'] = {
    'openapi': '3.0.2',
    'uiversion': 3
}
cors = CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ALLOWANCE']}})
api = Api(app, catch_all_404s=False, errors=errors)  # Establish connection between API and APP
swagger = Swagger(app, parse=False, template_file="api/v02/swagger.json")
# swagger = Swagger(app, parse=False, template=template)

api.add_resource(ShowUsage, '/api/0.2/', '/api/0.2/entity/', '/api/0.2/class/', '/api/0.2/code/',
                 '/api/0.2/latest/', '/api/0.2/node_entities/', '/api/0.2/node_entities_all/',
                 '/api/0.2/subunit/', '/api/0.2/subunit_hierarchy/', endpoint='usage')
api.add_resource(GetEntity, '/api/0.2/entity/<int:id_>', endpoint='entity')
api.add_resource(GetByClass, '/api/0.2/class/<string:class_code>', endpoint="class")
api.add_resource(GetByCode, '/api/0.2/code/<string:code>', endpoint="code")
api.add_resource(GetContent, '/api/0.2/content/', endpoint="content")
api.add_resource(GetLatest, '/api/0.2/latest/<int:latest>', endpoint="latest")
api.add_resource(GetNodeEntities, '/api/0.2/node_entities/<int:id_>', endpoint="node_entities")
api.add_resource(GetNodeEntitiesAll, '/api/0.2/node_entities_all/<int:id_>',
                 endpoint="node_entities_all")
api.add_resource(GetSubunit, '/api/0.2/subunit/<int:id_>', endpoint="subunit")
api.add_resource(GetSubunitHierarchy, '/api/0.2/subunit_hierarchy/<int:id_>',
                 endpoint="subunit_hierarchy")
api.add_resource(GetQuery, '/api/0.2/query/', endpoint="query")
