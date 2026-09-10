from uuid import UUID

from pydantic import Field, HttpUrl

from openatlas.api.api_v1.models.agent import AgentItem
from openatlas.api.api_v1.models.util import BaseSchema, IiifVersion


class LicenseItem(BaseSchema):
    id: int
    name: str = Field(
        description="Display name of the license.",
        examples=["CC BY 4.0", "Public Domain Mark 1.0"])
    # url: HttpUrl | None = Field(
    #     description="Official link to the legal deed or license text.",
    #     examples=["https://creativecommons.org/licenses/by/4.0/"])


# todo: do we need width, height, size?
class FileItem(BaseSchema):
    id: int
    uuid: UUID
    name: str
    public_shareable: bool = Field(
        description="Flag indicating if the file may be shown publicly.")
    license: LicenseItem | None = Field(
        description="License details for reuse.")
    creators: list[AgentItem] = Field(
        default_factory=list,
        description="Authors, photographers, or creators of the file.")
    license_holders: list[AgentItem] = Field(
        default_factory=list,
        description="Rights holders or copyright owners.")
    mimetype: str | None = Field(
        description="Standard IANA media type.",
        examples=["image/jpeg", "application/pdf"])
    extension: str | None = Field(
        default=None,
        description="File extension without leading dot.",
        examples=["jpg", "pdf"])
    file_url: HttpUrl | None = Field(
        default=None,
        description="Direct URL to the original binary file.",
        examples=["https://example.org/files/original/123.jpg"])
    thumbnail_url: HttpUrl | None = Field(
        default=None,
        description="URL to a static, pre-calculated preview image.",
        examples=["https://example.org/files/thumbs/123.jpg"], )
    iiif_manifest_url: HttpUrl | None = Field(
        default=None,
        description="URL to the IIIF Presentation API Manifest.",
        examples=["https://example.org/iiif/123/manifest.json"])
    iiif_base_url: HttpUrl | None = Field(
        default=None,
        description="Base URL for IIIF Image API operations (without "
                    "trailing slash).",
        examples=["https://example.org/iiif/image/123"], )
    #width: int | None = Field(
    #    default=None,
    #    description="Image or media width in pixels (null for non-raster "
    #                "files).",
    #    examples=[3840])
    #height: int | None = Field(
    #    default=None,
    #    description="Image or media height in pixels (null for non-raster "
    #                "files).",
    #    examples=[2160])
    #size: int | None = Field(
    #    default=None,
    #    description="File size in bytes.",
    #    examples=[5242880])


class LicensedFileOverviewResponse(BaseSchema):
    files: dict[str, FileItem] = Field(
        ...,
        description="Dictionary of licensed files, mapped by their ID")


class FilesByEntitiesQuery(BaseSchema):
    # Für den Endpunkt, der Dateien nach Entitäten sucht
    entity_ids: list[int] = Field(
        ...,
        alias="entityIds",
        description="List of entity IDs to fetch files for")


class FileIdPath(BaseSchema):
    id: int = Field(..., description="The ID of the file.")


class FileIiifPath(BaseSchema):
    id: int = Field(..., description="The ID of the file.")
    version: IiifVersion = Field(..., description="The IIIF version.")


class AnnotationIiifPath(BaseSchema):
    id: int = Field(..., description="The ID of the annotation.")
    version: IiifVersion = Field(..., description="The IIIF version.")
