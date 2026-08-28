from pydantic import Field

from openatlas.api.api_v1.models.util import BaseSchema


class FileItem(BaseSchema):
    creator: str | None = None
    display: str | None = Field(None, description="URL to view the full image")
    extension: str | None = None
    iiif_manifest: str | None = Field(None, description="URL to the IIIF Manifest")
    license: str | None = None
    license_holder: str | None = None
    mimetype: str | None = None
    public_shareable: bool | None = None
    thumbnail: str | None = Field(None, description="URL to the thumbnail image")

class LicensedFileOverviewResponse(BaseSchema):
    files: dict[str, FileItem] = Field(
        ...,
        description="Dictionary of licensed files, mapped by their ID"
    )

class FilesByEntitiesQuery(BaseSchema):
    # Für den Endpunkt, der Dateien nach Entitäten sucht
    entity_ids: list[int] = Field(
        ...,
        alias="entityIds",
        description="List of entity IDs to fetch files for"
    )