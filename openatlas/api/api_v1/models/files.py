from uuid import UUID

from pydantic import Field

from openatlas.api.api_v1.models.agent import AgentItem
from openatlas.api.api_v1.models.util import BaseSchema


class LicenseItem(BaseSchema):
    id: int
    name: str = Field(
        description="Display name of the license.",
        examples=["CC BY 4.0", "Public Domain Mark 1.0"])
    url: str | None = Field(
        default=None,
        description="Official link to the legal deed or license text.",
        examples=["https://creativecommons.org/licenses/by/4.0/"])


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
    file_url: str | None = Field(
        default=None,
        description="Direct URL to the original binary file.",
        examples=["https://example.org/files/original/123.jpg"])
    thumbnail_url: str | None = Field(
        default=None,
        description="URL to a static, pre-calculated preview image.",
        examples=["https://example.org/files/thumbs/123.jpg"], )
    iiif_manifest_url: str | None = Field(
        default=None,
        description="URL to the IIIF Presentation API Manifest.",
        examples=["https://example.org/iiif/123/manifest.json"])
    iiif_base_url: str | None = Field(
        default=None,
        description="Base URL for IIIF Image API operations (without "
                    "trailing slash).",
        examples=["https://example.org/iiif/image/123"])
    bounds: list[list[float]] | None = Field(
        default=None,
        description="Leaflet rotated image overlay bounds as three "
                    "[lat, lon] corner coordinates in the form "
                    "[[top_left_lat, top_left_lon], "
                    "[top_right_lat, top_right_lon], "
                    "[bottom_left_lat, bottom_left_lon]].",
        examples=[[
            [48.791618385483204, 15.505868280413463],
            [48.791630290810446, 15.5147623351736],
            [48.78714630103536, 15.505882388158021]]])
    inherited_from: int | None = Field(
        default=None,
        description="The ID of the parent entity in the archaeological "
                    "hierarchy from which this image is inherited.",
        examples=[12345])


class PublicFilesQuery(BaseSchema):
    limit: int = Field(
        100,
        ge=1,
        le=100,
        description="Number of records to return (max 100).")
    page: int = Field(
        1,
        ge=1,
        le=100000,
        description="Page number (starting at 1).")


class PublicFileOverviewResponse(BaseSchema):
    data: list[FileItem] = Field(
        description="Page of publicly shareable, licensed files.")
    total_items: int = Field(
        description="Total number of matching licensed files.")
    first: str = Field(description="URL to the first page of results.")
    previous: str | None = Field(
        None,
        description="URL to the previous page of results, if available.")
    next: str | None = Field(
        None,
        description="URL to the next page of results, if available.")
    last: str = Field(description="URL to the last page of results.")


class OverlayFilesResponse(BaseSchema):
    data: list[FileItem] = Field(
        description="List of publicly shareable, licensed files "
                    "with a map overlay.")


class FileIdPath(BaseSchema):
    id: int = Field(description="The ID of the file.")


class EntityFilesPath(BaseSchema):
    id: int = Field(description="The ID of the entity.")
