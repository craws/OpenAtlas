from pydantic import Field

from openatlas.api.api_v1.models.util import BaseSchema


class ApiIndexResponse(BaseSchema):
    name: str = Field(
        default="OpenAtlas API",
        description="Name of the API service.",
        examples=["OpenAtlas API"])
    version: str = Field(
        description="Active API major version.",
        examples=["1"])
    openapi_schema: str = Field(
        description="Full URL to the OpenAPI v3 JSON specification.",
        examples=["https://example.org/api/1/docs/openapi.json"])
    documentation: str = Field(
        description="Full URL to the interactive API documentation UI.",
        examples=["https://example.org/api/1/docs/swagger"])
    manual: str = Field(
        description="Full URL to the technical reference manual.",
        examples=["https://example.org/static/manual/technical/api.html"])
