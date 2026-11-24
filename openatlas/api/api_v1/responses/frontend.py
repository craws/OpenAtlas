from http import HTTPStatus

from openatlas.api.api_v1.models.frontend import SearchResponse
from openatlas.api.api_v1.models.util import ErrorResponse

search_response = {
    HTTPStatus.OK: SearchResponse,
    HTTPStatus.BAD_REQUEST: {
        'description': 'Invalid request parameter value.',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
