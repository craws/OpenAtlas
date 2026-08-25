from flask import g, session
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from openatlas import app
from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.models.util import OpenAtlasClassEnum
from openatlas.api.api_v1.models.system import EntityStatsQuery, \
    EntityStatsResponse, IiifInfo, ImageProcessingInfo, \
    LicensedFileOverviewQuery, LicensedFileOverviewResponse, MapConfig, \
    SystemClassItem, SystemClassesResponse, SystemInfoResponse, PropertyDetail, SystemPropertiesResponse, \
    SystemTypeTreeResponse, SystemTypesResponse, SystemStandardTypesResponse, TypeFlatItem, TypeTreeItem
from openatlas.api.api_v1.openapi_tags import system_tag


class LocaleQuery(BaseModel):
    locale: str = Field("en", description="Choose language for labels (e.g., 'en', 'de')."    )



class TypeTreePath(BaseModel):
    openatlas_class: OpenAtlasClassEnum = Field(
        ...,
        description="Filter the tree by a specific OpenAtlas class.")

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

@api_v1_system.get(
    '/crm-properties',
    summary="Get CIDOC properties",
    responses={200: SystemPropertiesResponse},
    tags=[system_tag])
def get_system_properties() -> dict:
    """
    Retrieves all OpenAtlas CIDOC properties actively used by the system.
    
    Returns a dictionary keyed by the CIDOC property code (e.g. 'P1', 'P2') containing 
    the domain and range class codes, inheritance structures (sub/super properties), 
    and internationalized labels for both directions (forward and inverse).
    """
    # Gather used properties from OpenAtlas class relations, plus essential base properties
    used_codes = {'P1', 'P2', 'P3'}
    for class_ in g.classes.values():
        for relation in class_.relations.values():
            if relation.property:
                used_codes.add(relation.property)

    # Automatically include sub-properties of any used property
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
        properties=results
            ).model_dump(by_alias=True)


# --- 3. TYPES & VOKABULARE ---

@api_v1_system.get(
    '/types',
    summary="Get flat types list",
    responses={200: SystemTypesResponse},
    tags=[system_tag])
def get_system_types() -> dict:
    """Retrieves a flat list of all OpenAtlas types."""
    types_dict = {}
    for id_, type_ in g.types.items():
        types_dict[str(id_)] = TypeFlatItem(
            id=type_.id,
            name=type_.name,
            description=type_.description,
            classes=type_.classes,
            selectable=type_.selectable,
            image_id=type_.image_id,
            first=type_.dates.first
                if hasattr(type_, 'dates') and type_.dates else None,
            last=type_.dates.last
                if hasattr(type_, 'dates') and type_.dates else None,
            root=type_.root,
            subs=type_.subs,
            count=type_.count,
            count_subs=type_.count_subs,
            category=getattr(type_, 'category', None))
    return SystemTypesResponse(types=types_dict).model_dump(by_alias=True)

def _generate_type_tree(openatlas_class: str | None = None) -> dict:
    def walk_tree(type_ids: list[int]) -> list[TypeTreeItem]:
        items = []
        for id_ in type_ids:
            item = g.types[id_]
            items.append(TypeTreeItem(
                id=item.id,
                name=item.name.replace("'", "&apos;"),
                classes=item.classes or None,
                children=walk_tree(item.subs)))
        return items

    types_tree_dict = {
        'standard': [],
        'custom': [],
        'place': [],
        'value': [],
        'system': [],
        'tools': []}
    
    for type_ in g.types.values():
        if type_.root:
            continue

        if type_.category in types_tree_dict:
            if openatlas_class and openatlas_class not in type_.classes:
                continue
                
            types_tree_dict[type_.category].append(TypeTreeItem(
                id=type_.id,
                name=type_.name.replace("'", "&apos;"),
                classes= type_.classes or None,
                children=walk_tree(type_.subs)))
            
    return SystemTypeTreeResponse(**types_tree_dict).model_dump(by_alias=True)

@api_v1_system.get(
    '/types/tree',
    summary="Get types tree",
    responses={200: SystemTypeTreeResponse},
    tags=[system_tag])
def get_system_type_tree() -> dict:
    """Retrieves all OpenAtlas types sorted hierarchically into standard,
    place, custom, value, and system categories."""
    return _generate_type_tree()

@api_v1_system.get(
    '/types/tree/<string:openatlas_class>',
    summary="Get types tree by OpenAtlas class",
    responses={200: SystemTypeTreeResponse},
    tags=[system_tag])
def get_system_type_tree_by_class(path: TypeTreePath) -> dict:
    """Retrieves all OpenAtlas types filtered by a specific OpenAtlas class."""
    class_ = path.openatlas_class
    if hasattr(path.openatlas_class, 'value') :
        class_ = path.openatlas_class.value
    return _generate_type_tree(openatlas_class=class_)

#todo: make this faster! maybe don't use g.types? Also look into other type functions
@api_v1_system.get(
    '/types/standard/<string:openatlas_class>',
    summary="Get standard types tree by OpenAtlas class",
    responses={200: SystemStandardTypesResponse},
    tags=[system_tag])
def get_system_standard_types_by_class(path: TypeTreePath) -> dict:
    """Retrieves standard OpenAtlas types filtered by a specific
    OpenAtlas class, formatted for hierarchical UI components."""

    class_ = path.openatlas_class
    if hasattr(path.openatlas_class, 'value') :
        class_ = path.openatlas_class.value

    def walk_tree(type_ids: list[int]) -> list[TypeTreeItem]:
        items = []
        for id_ in type_ids:
            item = g.types[id_]
            items.append(TypeTreeItem(
                id=item.id,
                name=item.name.replace("'", "&apos;"),
                classes=item.classes or None,
                children=walk_tree(item.subs)))
        return items

    standard_types = []
    
    for type_ in g.types.values():
        if type_.root:
            continue
            
        cat = getattr(type_, 'category', None)
        if cat == 'standard':
            if class_ and hasattr(type_, 'classes') and class_ not in type_.classes:
                continue
                
            standard_types.append(TypeTreeItem(
                id=type_.id,
                name=type_.name.replace("'", "&apos;"),
                classes= type_.classes or None,
                children=walk_tree(type_.subs) ))
            
    return SystemStandardTypesResponse(results=standard_types).model_dump(by_alias=True)
