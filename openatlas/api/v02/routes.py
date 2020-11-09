from flask_restful import Api

from openatlas import app
from openatlas.api.v02.common.class_ import GetClass
from openatlas.api.v02.common.content import GetContent
from openatlas.api.v02.common.entity import GetEntity

api = Api(app)  # Establish connection between API and APP

api.add_resource(GetEntity, '/api/0.2/entity/<int:id_>', endpoint='entity')
api.add_resource(GetClass, '/api/0.2/class/<string:class_code>', endpoint="class")
api.add_resource(GetContent, '/api/0.2/content/', endpoint="content")
