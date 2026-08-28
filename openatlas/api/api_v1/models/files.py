from typing import Literal
from uuid import UUID

from pydantic import Field

from openatlas.api.api_v1.models.util import BaseSchema


class LicenseItem(BaseSchema):
    name: str
    url: str | None = None


class AgentItem(BaseSchema):
    name: str
    type: Literal['person', 'group'] = Field(
        ...,
        description="If agent is a person or a group")
    description: str | None = None
    # external_url: list[ExtRefSystem] | None


class FileItem(BaseSchema):
    id: int
    uuid: UUID
    public_shareable: bool
    license: LicenseItem | None = None
    creators: list[AgentItem] | None = None
    license_holders: list[AgentItem] | None = None
    mimetype: str | None = None
    extension: str | None = None
    file_url: str | None = Field(
        None,
        description="URL to the raw original file (Image, PDF, MP4, etc.)")
    thumbnail_url: str | None = Field(
        None,
        description="URL to a static, pre-calculated thumbnail image")
    iiif_manifest_url: str | None = Field(
        None,
        description="URL to the IIIF Presentation API Manifest")
    iiif_base_url: str | None = Field(
        None,
        description="Base URL for the IIIF Image API (append "
                    "/full/max/0/default.jpg to use)")


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
    version: str = Field(..., description="The IIIF version.")
