from pydantic import BaseModel, Field

from openatlas.api.api_v1.models.util import BaseSchema


class ImageProcessingInfo(BaseSchema):
    enabled: bool = Field(
        description="Whether image processing "
                    "(thumbnail creation) is enabled.")
    available_image_sizes: dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary mapping size names to image dimensions.",
        json_schema_extra={
            "example": {"thumbnail": "200px", "table": "100px"}})


class IiifInfo(BaseSchema):
    enabled: bool = Field(
        description="Whether IIIF integration is enabled.")
    url: str | None = Field(
        None,
        description="Base URL of the IIIF Image API server.")
    version: str | None = Field(
        None,
        description="IIIF Presentation API specification "
                    "version (e.g. '2' or '3').")


class MapConfig(BaseSchema):
    zoom_default: int = Field(description="Default map zoom level.")
    zoom_max: int = Field(description="Maximum allowed map zoom level.")
    cluster_max_radius: int = Field(
        description="Maximum radius for marker clustering in pixels.")
    cluster_disable_at_zoom: int = Field(
        description="Zoom level at which marker clustering is disabled.")


class SystemInfoResponse(BaseSchema):
    version: str = Field(description="OpenAtlas Core Version")
    api_versions: dict[str, str] = Field(
        description="Mapping of supported API major versions to "
                    "full release strings.")
    site_name: str = Field(
        description="Name of the OpenAtlas project instance.")
    logo_file_id: int | None = Field(
        None,
        description="Entity ID of the logo image file, if configured.")
    default_language: str = Field(
        description="Default ISO language code of the project.")
    module_time: bool = Field(
        description="Whether the time module "
                    "(hours, minutes, seconds) is enabled.")
    map_config: MapConfig = Field(description="Map configuration parameters.")
    image_processing: ImageProcessingInfo = Field(
        description="Image processing features and sizes.")
    iiif: IiifInfo = Field(description="IIIF server settings.")


class EntityCountQuery(BaseSchema):
    case_study: int | None = Field(
        None,
        description="Filter entity counts by a specific case study ID.")


class EntityCountResponse(BaseSchema):
    counts: dict[str, int] = Field(
        description="Count of entities grouped by OpenAtlas system class.")


class SystemClassItem(BaseSchema):
    label: str = Field(description="Translated label of the class.")
    openatlas_class: str = Field(
        description="Internal OpenAtlas system class name "
                    "(e.g. 'place', 'person').")
    crm: str | None = Field(
        None,
        description="CIDOC CRM class code (e.g. 'E21', 'E53').")
    standard_type_id: int | None = Field(
        None,
        description="ID of the root type in the hierarchy used "
                    "for this class.")
    group: str | None = Field(
        None,
        description="UI grouping category (e.g. 'actor', 'reference').")
    icon: str | None = Field(
        None,
        description="Icon identifier for frontend display.")


class SystemClassesResponse(BaseSchema):
    locale: str = Field(
        default="en",
        description="The language used for labels.")
    results: list[SystemClassItem] = Field(
        description="List of available system classes.")


class PropertyI18n(BaseSchema):
    de: str | None = Field(None, description="German translation.")
    en: str | None = Field(None, description="English translation.")
    fr: str | None = Field(None, description="French translation.")


class PropertyDetail(BaseSchema):
    name: str = Field(description="Canonical property name.")
    name_inverse: str | None = Field(
        None,
        description="Canonical inverse property name.")
    code: str = Field(description="CIDOC CRM property code (e.g. 'P1').")
    domain_class_code: str | None = Field(
        None,
        description="CIDOC CRM domain class code.")
    range_class_code: str | None = Field(
        None,
        description="CIDOC CRM range class code.")
    count: int | None = Field(
        None,
        description="Number of link instances using this property.")
    sub: list[str] | None = Field(
        None,
        description="List of sub-property codes "
                    "inheriting from this property.")
    super: list[str] | None = Field(
        None,
        description="List of super-property codes this "
                    "property inherits from.")
    i18n: PropertyI18n | None = Field(
        None,
        description="Internationalized forward labels.")
    i18n_inverse: PropertyI18n | None = Field(
        None,
        description="Internationalized inverse labels.")


class SystemPropertiesResponse(BaseSchema):
    properties: dict[str, PropertyDetail] = Field(
        description="Dictionary mapping CIDOC property codes "
                    "to their details.")


class LocaleQuery(BaseModel):
    locale: str = Field(
        "en",
        description="Choose language for labels (e.g., 'en', 'de').")
