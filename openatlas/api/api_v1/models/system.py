from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Dict

from openatlas.api.api_v1.models.util import OpenAtlasClassEnum


class ImageProcessingInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    enabled: bool
    available_image_sizes: Dict[str, str] = Field(
        ...,
        json_schema_extra={"example": {"thumbnail": "200px", "table": "100px"}}    )


class IiifInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    enabled: bool
    url: str | None = None
    version: str | None = None


class MapConfig(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    zoom_default: int
    zoom_max: int
    cluster_max_radius: int
    cluster_disable_at_zoom: int


class SystemInfoResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    version: str = Field(
        ...,
        description="OpenAtlas Core Version")
    api_versions: list[str]
    site_name: str
    logo_file_id: int | None = None
    default_language: str
    module_time: bool = Field(
        ...,
        description="Whether the time module (hours, minutes, seconds) is enabled.")
    
    map_config: MapConfig
    image_processing: ImageProcessingInfo
    iiif: IiifInfo  


class LicensedFileItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    display: str | None = None
    thumbnail: str | None = None
    extension: str | None = None
    mimetype: str | None = None
    license: str | None = None
    creator: str | None = None
    license_holder: str | None = None
    public_shareable: bool | None = None
    iiif_manifest: str | None = None


class LicensedFileOverviewQuery(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    file_id: int | None = Field(None,
                                description="Filter by a specific file ID.")


class LicensedFileOverviewResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # Key ist die ID als String (JSON-Standard), Value ist das FileItem
    files: Dict[str, LicensedFileItem]


class EntityStatsQuery(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    case_study: UUID | int | None = Field(
        None,
        description="Filter entity counts by a specific case study ID or UUID."
    )


class EntityStatsResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # Dictionary mit den OpenAtlas-Klassen als Keys und Integern als Values
    counts: Dict[OpenAtlasClassEnum, int] = Field(
        ...,
        description="Count of entities grouped by OpenAtlas system class.")


# --- KLASSEN ---
class SystemClassItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    label: str = Field(..., description="Translated label of the class.")
    openatlas_class: str
    crm: str | None = None
    standard_type_id: int | None = None
    group: str | None = None
    icon: str | None = None

class SystemClassesResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    locale: str = Field(default="en", description="The language used for labels.")
    results: list[SystemClassItem]

# --- PROPERTIES ---
class PropertyI18n(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    de: str | None = None
    en: str | None = None
    fr: str | None = None

class PropertyDetail(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    name_inverse: str | None = None
    code: str
    domain_class_code: str | None = None
    range_class_code: str | None = None
    count: int | None = None
    sub: list[str] | None = None
    super: list[str] | None = None
    i18n: PropertyI18n | None = None
    i18n_inverse: PropertyI18n | None = None

class SystemPropertiesResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # Dictionary mit den CIDOC-Codes (z.B. 'P1', 'OA7') als Keys
    properties: Dict[str, PropertyDetail]

# --- TYPES (FLACH) ---
class TypeFlatItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    name: str
    description: str | None = None
    image_id: int | None = None
    selectable: bool | None = None
    classes: list[str] | None = None
    first: int | None = None
    last: int | None = None
    root: list[int] | None = None
    subs: list[int] | None = None
    count: int | None = None
    count_subs: int | None = None
    category: str | None = None

class SystemTypesResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # Key ist die Typ-ID als String, Value ist das FlatItem
    types: Dict[str, TypeFlatItem]

    # --- TYPES (BAUM) ---

class TypeTreeItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    name: str
    classes: list[str] | None = None
    children: list['TypeTreeItem'] = Field(default_factory=list)

class SystemTypeTreeResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    standard: list[TypeTreeItem] = Field(default_factory=list)
    place: list[TypeTreeItem] = Field(default_factory=list)
    custom: list[TypeTreeItem] = Field(default_factory=list)
    value: list[TypeTreeItem] = Field(default_factory=list)
    system: list[TypeTreeItem] = Field(default_factory=list)
class SystemStandardTypesResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    results: list[TypeTreeItem] = Field(default_factory=list)
