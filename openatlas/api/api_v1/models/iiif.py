from pydantic import Field

from openatlas.api.api_v1.models.util import BaseSchema, IiifVersion


class FileIiifPath(BaseSchema):
    id: int = Field(..., description="The ID of the file.")
    version: IiifVersion = Field(..., description="The IIIF version.")


class AnnotationIiifPath(BaseSchema):
    id: int = Field(..., description="The ID of the annotation.")
    version: IiifVersion = Field(..., description="The IIIF version.")
