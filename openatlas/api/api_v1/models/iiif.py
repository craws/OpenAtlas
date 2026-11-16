from pydantic import AnyHttpUrl, Field

from openatlas.api.api_v1.models.util import BaseSchema


class FileIiifPath(BaseSchema):
    id: int = Field(description="The ID of the file.")


class AnnotationIiifPath(BaseSchema):
    id: int = Field(description="The ID of the annotation.")


class IiifQuery(BaseSchema):
    url: AnyHttpUrl | None = Field(
        default=None,
        description="Base URL used to override entity links (e.g. for "
                    "presentation sites); the entity ID is appended.")
