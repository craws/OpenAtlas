from flask import g
from flask_restful import Api

from openatlas import app
from openatlas.api.v02.common.class_ import GetByClass
from openatlas.api.v02.common.code import GetByCode
from openatlas.api.v02.common.content import GetContent
from openatlas.api.v02.common.entity import GetEntity
from openatlas.api.v02.common.latest import GetLatest
from openatlas.api.v02.common.node_entities import GetNodeEntities
from openatlas.api.v02.common.node_entities_all import GetNodeEntitiesAll
from openatlas.api.v02.common.subunit import GetSubunit
from openatlas.api.v02.common.subunit_hierarchy import GetSubunitHierarchy
from openatlas.api.v02.common.query import GetQuery

api = Api(app)  # Establish connection between API and APP

api.add_resource(GetEntity, '/api/0.2/entity/<int:id_>', endpoint='entity')
api.add_resource(GetByClass, '/api/0.2/class/<string:class_code>', endpoint="class")
api.add_resource(GetByCode, '/api/0.2/code/<string:item>', endpoint="code")
api.add_resource(GetContent, '/api/0.2/content/', endpoint="content")
api.add_resource(GetLatest, '/api/0.2/latest/<int:latest>', endpoint="latest")
api.add_resource(GetNodeEntities, '/api/0.2/node_entities/<int:id_>', endpoint="node_entities")
api.add_resource(GetNodeEntitiesAll, '/api/0.2/node_entities_all/<int:id_>', endpoint="node_entities_all")
api.add_resource(GetSubunit, '/api/0.2/subunit/<int:id_>', endpoint="subunit")
api.add_resource(GetSubunitHierarchy, '/api/0.2/subunit_hierarchy/<int:id_>', endpoint="subunit_hierarchy")
api.add_resource(GetQuery, '/api/0.2/query/', endpoint="query")
