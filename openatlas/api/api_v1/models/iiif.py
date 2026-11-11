from pydantic import Field

from openatlas.api.api_v1.models.util import BaseSchema


class FileIiifPath(BaseSchema):
    id: int = Field(description="The ID of the file.")


class AnnotationIiifPath(BaseSchema):
    id: int = Field(description="The ID of the annotation.")
