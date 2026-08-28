from openatlas.api.api_v1.models.util import BaseSchema


class ApiIndexResponse(BaseSchema):

    name: str
    version: str
    openapi_schema: str
    documentation: str
    manual: str
