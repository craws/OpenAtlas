from flask import g, session
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from openatlas import app
from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.models.system import EntityCountQuery, \
    EntityCountResponse, IiifInfo, ImageProcessingInfo, MapConfig, \
    PropertyDetail, SystemClassItem, SystemClassesResponse, SystemInfoResponse, \
    SystemPropertiesResponse
from openatlas.api.api_v1.models.util import OpenAtlasClassEnum
from openatlas.api.api_v1.openapi_tags import system_tag
from openatlas.api.api_v1.responses.system import (entity_count_response,
                                                   system_classes_response,
                                                   system_info_response,
                                                   system_properties_response)
from openatlas.database.api import get_overview_counts_by_case_study

api_v1_system = APIBlueprint(
    'api_v1_system',
    __name__,
    url_prefix='/api/1/system')
register_error_handlers(api_v1_system)


class LocaleQuery(BaseModel):
    locale: str = Field(
        "en",
        description="Choose language for labels (e.g., 'en', 'de').")


@api_v1_system.get(
    '/info',
    endpoint='system_info',
    summary="Get presentation frontend configuration",
    responses=system_info_response,
    tags=[system_tag]
)
def get_system_info() -> dict:
    """
    Retrieves the public configuration required to initialize the presentation
    frontend.

    This includes global settings like map configurations (zoom, clustering),
    enabled features (time module, IIIF), and localization defaults.
    Internal or sensitive backend configurations are explicitly excluded.
    """

    logo_id = g.settings.get('logo_file_id')
    logo_id_clean = int(logo_id) if logo_id else None
    img_enabled = bool(g.settings['image_processing'])
    iiif_version_raw = g.settings.get('iiif_version')

    map_conf = MapConfig(
        zoom_default=int(g.settings['map_zoom_default']),
        zoom_max=int(g.settings['map_zoom_max']),
        cluster_max_radius=int(g.settings['map_cluster_max_radius']),
        cluster_disable_at_zoom=int(g.settings['map_cluster_disable_at_zoom']))

    img_conf = ImageProcessingInfo(
        enabled=img_enabled,
        available_image_sizes=app.config['IMAGE_SIZE'] if img_enabled else {})

    iiif_conf = IiifInfo(
        enabled=bool(g.settings['iiif']),
        url=g.settings.get('iiif_url'),
        version=str(iiif_version_raw) if iiif_version_raw else None)

    response = SystemInfoResponse(
        version=app.config['VERSION'],
        api_versions=app.config['API_VERSIONS'],
        site_name=g.settings['site_name'],
        logo_file_id=logo_id_clean,
        default_language=g.settings['default_language'],
        module_time=bool(g.settings['module_time']),
        map_config=map_conf,
        image_processing=img_conf,
        iiif=iiif_conf)

    return response.model_dump(by_alias=True)


@api_v1_system.get(
    '/count/entities',
    endpoint='entity_count',
    summary="Get entity counts",
    responses=entity_count_response,
    tags=[system_tag])
def get_entity_count(query: EntityCountQuery):
    """Retrieves system classes with a count of their instances, optionally
    filtered by case study."""
    valid_classes = [e.value for e in OpenAtlasClassEnum]

    counts = get_overview_counts_by_case_study(
        classes=valid_classes,
        case_study_id=query.case_study)

    return EntityCountResponse(counts=counts).model_dump(by_alias=True)


@api_v1_system.get(
    '/classes',
    endpoint='system_classes',
    summary="Get system classes",
    responses=system_classes_response,
    tags=[system_tag])
def get_system_classes(query: LocaleQuery) -> dict:
    """Retrieves all OpenAtlas classes with their labels,
    CIDOC CRM mapping, and frontend configurations."""
    locale = query.locale if query.locale else session.get('language', 'en')
    results = []
    for class_ in g.classes.values():
        results.append(SystemClassItem(
            label=str(class_.label),
            openatlas_class=class_.name,
            crm=class_.cidoc_class.code if class_.cidoc_class else None,
            standard_type_id=class_.standard_type_id,
            group=class_.group.get('name') if class_.group else None,
            icon=class_.group.get('icon') if class_.group else None))
    return SystemClassesResponse(
        locale=locale,
        results=results).model_dump(by_alias=True)


@api_v1_system.get(
    '/crm-properties',
    endpoint='system_crm_properties',
    summary="Get CIDOC properties",
    responses=system_properties_response,
    tags=[system_tag])
def get_system_properties() -> dict:
    """
    Retrieves all OpenAtlas CIDOC properties actively used by the system.
    
    Returns a dictionary keyed by the CIDOC property code (e.g. 'P1', 'P2')
    containing the domain and range class codes, inheritance structures
    (sub/super properties), and internationalized labels for both directions
    (forward and inverse).
    """
    used_codes = {'P1', 'P2', 'P3'}
    for class_ in g.classes.values():
        for relation in class_.relations.values():
            if relation.property:
                used_codes.add(relation.property)

    sub_codes = set()
    for code in used_codes:
        if code in g.properties and g.properties[code].sub:
            sub_codes.update(g.properties[code].sub)
    used_codes.update(sub_codes)

    results = {}
    for code, property_ in g.properties.items():
        if code in used_codes:
            results[code] = PropertyDetail(
                name=property_.name,
                name_inverse=property_.name_inverse,
                code=property_.code,
                domain_class_code=property_.domain_class_code,
                range_class_code=property_.range_class_code,
                count=property_.count,
                sub=property_.sub,
                super=property_.super,
                i18n=property_.i18n,
                i18n_inverse=property_.i18n_inverse)

    return SystemPropertiesResponse(
        properties=results).model_dump(by_alias=True)
