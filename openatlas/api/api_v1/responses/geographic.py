from http import HTTPStatus

from openatlas.api.api_v1.models.geographic import GeoJsonFeatureCollection
from openatlas.api.api_v1.models.util import ErrorResponse

bbox_response = {
    HTTPStatus.OK: GeoJsonFeatureCollection,
    HTTPStatus.BAD_REQUEST: {
        'description': 'Invalid request parameter value.',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
