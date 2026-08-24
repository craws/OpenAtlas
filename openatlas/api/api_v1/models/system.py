from uuid import UUID

from pydantic import BaseModel, Field
from typing import Dict

from openatlas.api.api_v1.models.util import OpenAtlasClassEnum


class ImageProcessingInfo(BaseModel):
    enabled: bool
    available_image_sizes: Dict[str, str] = Field(
        ...,
        alias="availableImageSizes",
        json_schema_extra={"example": {"thumbnail": "200px", "table": "100px"}}
    )


class IiifInfo(BaseModel):
    enabled: bool
    url: str | None = None
    version: str | None = None


class SystemInfoResponse(BaseModel):
    version: str = Field(..., description="OpenAtlas Core Version")
    api_versions: list[str] = Field(..., alias="apiVersions")
    site_name: str = Field(..., alias="siteName")
    image_processing: ImageProcessingInfo = Field(..., alias="imageProcessing")
    iiif: IiifInfo = Field(..., alias="IIIF")


class LicensedFileItem(BaseModel):
    display: str | None = None
    thumbnail: str | None = None
    extension: str | None = None
    mimetype: str | None = None
    license: str | None = None
    creator: str | None = None
    license_holder: str | None = Field(None, alias="licenseHolder")
    public_shareable: bool | None = Field(None, alias="publicShareable")
    iiif_manifest: str | None = Field(None, alias="IIIFManifest")


class LicensedFileOverviewQuery(BaseModel):
    file_id: int | None = Field(None, alias="fileId",
                                description="Filter by a specific file ID.")


class LicensedFileOverviewResponse(BaseModel):
    # Key ist die ID als String (JSON-Standard), Value ist das FileItem
    files: Dict[str, LicensedFileItem]


class EntityStatsQuery(BaseModel):
    case_study: UUID | int | None = Field(
        None,
        alias="caseStudy",
        description="Filter entity counts by a specific case study ID or UUID."
    )


class EntityStatsResponse(BaseModel):
    # Dictionary mit den OpenAtlas-Klassen als Keys und Integern als Values
    counts: Dict[OpenAtlasClassEnum, int] = Field(
        ...,
        description="Count of entities grouped by OpenAtlas system class.")
