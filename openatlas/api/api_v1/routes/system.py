from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from openatlas.api.api_v1.error_handlers import register_error_handlers
# Hier importierst du deine ganzen Modelle aus models/system.py
from openatlas.api.api_v1.models.system import (EntityStatsQuery,
                                                EntityStatsResponse,
                                                LicensedFileOverviewQuery,
                                                LicensedFileOverviewResponse,
                                                SystemClassesResponse,
                                                SystemInfoResponse,
                                                SystemPropertiesResponse,
                                                SystemTypeTreeResponse,
                                                SystemTypesResponse)
from openatlas.api.api_v1.openapi_tags import system_tag


# Optional: Kleine Query-Modelle, falls du Parameter wie 'locale' oder 'viewClass' brauchst
class LocaleQuery(BaseModel):
    locale: str = Field("en", description="Choose language for labels (e.g., 'en', 'de')."    )

class TypeTreeQuery(BaseModel):
    view_class: str | None = Field(None, alias="viewClass", description="Filter the tree by a specific view class.")


api_v1_system = APIBlueprint('system', __name__, url_prefix='/api/1/system')
register_error_handlers(api_v1_system)


# --- 1. SYSTEM-STATUS & STATISTIK ---

@api_v1_system.get('/info', summary="Get system info", responses={200: SystemInfoResponse}, tags=[system_tag])
def get_system_info():
    """Retrieves backend configuration, API versions, and enabled features (e.g., IIIF)."""
    pass

@api_v1_system.get('/stats/entities', summary="Get entity counts", responses={200: EntityStatsResponse}, tags=[system_tag])
def get_entity_stats(query: EntityStatsQuery):
    """Retrieves system classes with a count of their instances, optionally filtered by case study."""
    pass

@api_v1_system.get('/licensed-files', summary="Get licensed files", responses={200: LicensedFileOverviewResponse}, tags=[system_tag])
def get_licensed_files(query: LicensedFileOverviewQuery):
    """Retrieves all existing files with a license, their display URLs, and metadata."""
    pass


# --- 2. KLASSEN & PROPERTIES ---

@api_v1_system.get('/classes', summary="Get system classes", responses={200: SystemClassesResponse}, tags=[system_tag])
def get_system_classes(query: LocaleQuery):
    """Retrieves all OpenAtlas classes with their labels, CIDOC CRM mapping, and frontend configurations."""
    pass

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