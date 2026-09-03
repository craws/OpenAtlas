from flask import url_for
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.models.root import ApiIndexResponse
from openatlas.api.api_v1.openapi_tags import system_tag
from openatlas.api.api_v1.responses.root import index_response

api_v1_root = APIBlueprint('api_v1_root', __name__, url_prefix='/api/1')


@api_v1_root.get(
    '/',
    endpoint='index',
    summary="API Index",
    responses=index_response,
    tags=[system_tag],
    strict_slashes=False)
def api_v1_index() -> dict:
    """
    Returns the OpenAtlas API V1 root index pointing to documentation and schemas.
    """
    response = ApiIndexResponse(
        name="OpenAtlas API V1",
        version="1.0.0",
        # todo: only schema dynamic link
        openapi_schema="/openapi/openapi.json",
        documentation=url_for('custom_swagger_ui', _external=True),
        manual=url_for(
            'static',
            filename='manual/technical/api.html',
            _external=True))
    return response.model_dump(by_alias=True)
