from typing import Dict

from pydantic import Field

from openatlas.api.api_v1.models.util import BaseSchema, OpenAtlasClassEnum


class ImageProcessingInfo(BaseSchema):
    enabled: bool
    available_image_sizes: Dict[str, str] = Field(
        ...,
        json_schema_extra={
            "example": {"thumbnail": "200px", "table": "100px"}})


class IiifInfo(BaseSchema):
    enabled: bool
    url: str | None = None
    version: str | None = None


class MapConfig(BaseSchema):
    zoom_default: int
    zoom_max: int
    cluster_max_radius: int
    cluster_disable_at_zoom: int


class SystemInfoResponse(BaseSchema):
    version: str = Field(
        ...,
        description="OpenAtlas Core Version")
    api_versions: list[str]
    site_name: str
    logo_file_id: int | None = None
    default_language: str
    module_time: bool = Field(
        ...,
        description="Whether the time module (hours, minutes, seconds) is "
                    "enabled.")

    map_config: MapConfig
    image_processing: ImageProcessingInfo
    iiif: IiifInfo


class EntityCountQuery(BaseSchema):
    case_study: int | None = Field(
        None,
        description="Filter entity counts by a specific case study ID.")


class EntityCountResponse(BaseSchema):
    counts: Dict[OpenAtlasClassEnum, int] = Field(
        ...,
        description="Count of entities grouped by OpenAtlas system class.")


class SystemClassItem(BaseSchema):
    label: str = Field(..., description="Translated label of the class.")
    openatlas_class: str
    crm: str | None = None
    standard_type_id: int | None = None
    group: str | None = None
    icon: str | None = None


class SystemClassesResponse(BaseSchema):
    locale: str = Field(
        default="en",
        description="The language used for labels.")
    results: list[SystemClassItem]


class PropertyI18n(BaseSchema):
    de: str | None = None
    en: str | None = None
    fr: str | None = None


class PropertyDetail(BaseSchema):
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


class SystemPropertiesResponse(BaseSchema):
    properties: Dict[str, PropertyDetail]
