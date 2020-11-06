from flask_restful import Api, Resource

from openatlas import app

api = Api(app)  # Establish connection between API and APP


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/api/0.1/testing')
