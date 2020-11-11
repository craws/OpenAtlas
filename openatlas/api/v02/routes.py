from flask_restful import Api

from openatlas import app
from openatlas.api.v02.common.class_ import GetByClass
from openatlas.api.v02.common.code import GetByCode
from openatlas.api.v02.common.content import GetContent
from openatlas.api.v02.common.entity import GetEntity
from openatlas.api.v02.common.latest import GetLatest

api = Api(app)  # Establish connection between API and APP

api.add_resource(GetEntity, '/api/0.2/entity/<int:id_>', endpoint='entity')
api.add_resource(GetByClass, '/api/0.2/class/<string:class_code>', endpoint="class")
api.add_resource(GetByCode, '/api/0.2/code/<string:item>', endpoint="code")
api.add_resource(GetContent, '/api/0.2/content/', endpoint="content")
api.add_resource(GetLatest, '/api/0.2/latest/<int:latest>', endpoint="latest")
