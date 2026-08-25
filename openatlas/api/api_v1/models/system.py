from uuid import UUID

from pydantic import BaseModel, Field
from typing import Dict

from openatlas.api.api_v1.models.util import OpenAtlasClassEnum


class ImageProcessingInfo(BaseModel):
    enabled: bool
    available_image_sizes: Dict[str, str] = Field(
        ...,
        alias="availableImageSizes",
        json_schema_extra={"example": {"thumbnail": "200px", "table": "100px"}}    )


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


# --- KLASSEN ---
class SystemClassItem(BaseModel):
    label: str = Field(..., description="Translated label of the class.")
    system_class: str = Field(..., alias="systemClass")
    crm_class: str | None = Field(None, alias="crmClass")
    view: str | None = None
    icon: str | None = None

class SystemClassesResponse(BaseModel):
    locale: str = Field(default="en", description="The language used for labels.")
    results: list[SystemClassItem]

# --- PROPERTIES ---
class PropertyI18n(BaseModel):
    de: str | None = None
    en: str | None = None
    fr: str | None = None

class PropertyDetail(BaseModel):
    name: str
    name_inverse: str | None = Field(None, alias="nameInverse")
    code: str
    domain_class_code: str | None = Field(None, alias="domainClassCode")
    range_class_code: str | None = Field(None, alias="rangeClassCode")
    count: int | None = None
    sub: list[str] | None = None
    super: list[str] | None = None
    i18n: PropertyI18n | None = None
    i18n_inverse: str | None = Field(None, alias="i18nInverse")

class SystemPropertiesResponse(BaseModel):
    # Dictionary mit den CIDOC-Codes (z.B. 'P1', 'OA7') als Keys
    properties: Dict[str, PropertyDetail]

# --- TYPES (FLACH) ---
class TypeFlatItem(BaseModel):
    id: int
    name: str
    description: str | None = None
    origin_id: int | None = Field(None, alias="originId")
    first: int | None = None
    last: int | None = None
    root: list[int] | None = None
    subs: list[int] | None = None
    count: int | None = None
    count_subs: int | None = Field(None, alias="countSubs")
    category: str | None = None

class SystemTypesResponse(BaseModel):
    # Key ist die Typ-ID als String, Value ist das FlatItem
    types: Dict[str, TypeFlatItem]

    # --- TYPES (BAUM) ---

class TypeTreeItem(BaseModel):
    id: int
    name: str
    view_class: list[str] | None = Field(None, alias="viewClass")
    # Rekursiver Aufruf für beliebig tiefe Verschachtelung
    children: list['TypeTreeItem'] = Field(default_factory=list)

class SystemTypeTreeResponse(BaseModel):
    standard: list[TypeTreeItem] = Field(default_factory=list)
    place: list[TypeTreeItem] = Field(default_factory=list)
    custom: list[TypeTreeItem] = Field(default_factory=list)
    value: list[TypeTreeItem] = Field(default_factory=list)
    system: list[TypeTreeItem] = Field(default_factory=list)