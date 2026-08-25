from flask import g, session
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from openatlas import app
from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.models.system import EntityStatsQuery, \
    EntityStatsResponse, IiifInfo, ImageProcessingInfo, \
    LicensedFileOverviewQuery, LicensedFileOverviewResponse, MapConfig, \
    SystemClassItem, SystemClassesResponse, SystemInfoResponse, SystemPropertiesResponse, \
    SystemTypeTreeResponse, SystemTypesResponse
from openatlas.api.api_v1.openapi_tags import system_tag


class LocaleQuery(BaseModel):
    locale: str = Field("en", description="Choose language for labels (e.g., 'en', 'de')."    )

class TypeTreeQuery(BaseModel):
    view_class: str | None = Field(None, alias="viewClass", description="Filter the tree by a specific view class.")


api_v1_system = APIBlueprint('system', __name__, url_prefix='/api/1/system')
register_error_handlers(api_v1_system)


# --- 1. SYSTEM-STATUS & STATISTIK ---

@api_v1_system.get(
    '/info',
    summary="Get presentation frontend configuration",
    responses={200: SystemInfoResponse},
    tags=[system_tag])
def get_system_info() -> dict:
    """
    Retrieves the public configuration required to initialize the presentation frontend.
    
    This includes global settings like map configurations (zoom, clustering), 
    enabled features (time module, IIIF), and localization defaults.
    Internal or sensitive backend configurations are explicitly excluded.
    """
    return SystemInfoResponse(
        version=app.config['VERSION'],
        api_versions=app.config['API_VERSIONS'],
        site_name=g.settings['site_name'],
        logo_file_id=int(g.settings['logo_file_id'])
            if g.settings.get('logo_file_id') else None,
        default_language=g.settings['default_language'],
        module_time=
            g.settings.get('module_time', False) in (True, 'True', '1', 1),
        map_config=MapConfig(
            zoom_default=int(g.settings['map_zoom_default']),
            zoom_max=int(g.settings['map_zoom_max']),
            cluster_max_radius=int(g.settings['map_cluster_max_radius']),
            cluster_disable_at_zoom=int(g.settings['map_cluster_disable_at_zoom'])),
        image_processing=ImageProcessingInfo(
            enabled=bool(g.settings['image_processing']),
            available_image_sizes=app.config['IMAGE_SIZE'] if g.settings['image_processing'] else {}
        ),
        iiif=IiifInfo(
            enabled=bool(g.settings['iiif']),
            url=g.settings.get('iiif_url'),
            version=str(g.settings['iiif_version'])
                if g.settings.get('iiif_version') else None)).model_dump(by_alias=True)

@api_v1_system.get('/stats/entities', summary="Get entity counts", responses={200: EntityStatsResponse}, tags=[system_tag])
def get_entity_stats(query: EntityStatsQuery):
    """Retrieves system classes with a count of their instances, optionally filtered by case study."""
    pass

@api_v1_system.get('/licensed-files', summary="Get licensed files", responses={200: LicensedFileOverviewResponse}, tags=[system_tag])
def get_licensed_files(query: LicensedFileOverviewQuery):
    """Retrieves all existing files with a license, their display URLs, and metadata."""
    pass


@api_v1_system.get(
    '/classes',
    summary="Get system classes",
    responses={200: SystemClassesResponse},
    tags=[system_tag])
def get_system_classes(query: LocaleQuery) -> dict:
    """Retrieves all OpenAtlas classes with their labels,
    CIDOC CRM mapping, and frontend configurations."""
    results = []
    for class_ in g.classes.values():
        results.append(SystemClassItem(
            label=str(class_.label),
            openatlas_class=class_.name,
            crm=class_.cidoc_class.code if class_.cidoc_class else None,
            standard_type_id=class_.standard_type_id,
            group=class_.group.get('name') if class_.group else None,
            icon=class_.group.get('icon') if class_.group else None
        ))
    return SystemClassesResponse(
        locale=query.locale if query.locale else session.get('language', 'en'),
        results=results
    ).model_dump(by_alias=True)

@api_v1_system.get('/properties', summary="Get CIDOC properties", responses={200: SystemPropertiesResponse}, tags=[system_tag])
def get_system_properties(query: LocaleQuery):
    """Retrieves all OpenAtlas CIDOC properties with their domain/range classes and translations."""
    pass


# --- 3. TYPES & VOKABULARE ---

@api_v1_system.get('/types', summary="Get flat types list", responses={200: SystemTypesResponse}, tags=[system_tag])
def get_system_types():
    """Retrieves a flat list of all OpenAtlas types."""
    pass

@api_v1_system.get('/types/tree', summary="Get types tree", responses={200: SystemTypeTreeResponse}, tags=[system_tag])
def get_system_type_tree(query: TypeTreeQuery):
    """Retrieves all OpenAtlas types sorted hierarchically into standard, place, custom, value, and system categories."""
    pass