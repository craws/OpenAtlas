from openatlas.api.endpoints.content import (
    ClassMapping, Classes, GetBackendDetails, GetProperties, SystemClassCount)
from openatlas.api.endpoints.display_image import (
    DisplayImage, LicensedFileOverview)
from openatlas.api.endpoints.entities import (
    GetByCidocClass, GetBySystemClass, GetByViewClass,
    GetEntitiesLinkedToEntity, GetEntity, GetLatest,
    GetLinkedEntitiesByPropertyRecursive, GetQuery, GetTypeEntities,
    GetTypeEntitiesAll)
from openatlas.api.endpoints.iiif import (
    IIIFAnnotation, IIIFAnnotationList, IIIFCanvas, IIIFImage, IIIFManifest,
    IIIFSequence)
from openatlas.api.endpoints.special import (
    ExportDatabase, GetGeometricEntities, GetNetworkVisualisation, GetSubunits)
from openatlas.api.endpoints.type import (
    GetTypeByViewClass, GetTypeOverview, GetTypeTree)

entity = [
    [GetByViewClass, '/view_class/<string:class_>', 'view_class'],
    [GetByCidocClass, '/cidoc_class/<string:class_>', 'cidoc_class'],
    [GetEntity, '/entity/<int:id_>', 'entity'],
    [GetLatest, '/latest/<int:limit>', 'latest'],
    [GetQuery, '/query/', 'query'],
    [GetBySystemClass, '/system_class/<string:class_>', 'system_class'],
    [GetTypeEntities, '/type_entities/<int:id_>', 'type_entities'],
    [GetTypeEntitiesAll, '/type_entities_all/<int:id_>', 'type_entities_all'],
    [GetLinkedEntitiesByPropertyRecursive,
     '/linked_entities_by_properties_recursive/<int:id_>',
     'linked_entities_by_properties_recursive'],
    [GetEntitiesLinkedToEntity,
     '/entities_linked_to_entity/<int:id_>',
     'entities_linked_to_entity']]

admin = [
    [SystemClassCount, '/system_class_count/', 'system_class_count'],
    [GetBackendDetails, '/backend_details/', 'backend_details'],
    [ClassMapping, '/class_mapping/', 'class_mapping'],
    [GetProperties, '/properties/', 'properties'],
    [LicensedFileOverview, '/licensed_file_overview/',
     'licensed_file_overview'],
    [Classes, '/classes/', 'classes']]

types = [
    [GetTypeByViewClass, '/type_by_view_class/', 'type_by_view_class'],
    [GetTypeOverview, '/type_overview/', 'type_overview'],
    [GetTypeTree, '/type_tree/', 'type_tree']]

special = [
    [ExportDatabase, '/export_database/<string:format_>', 'export_database'],
    [GetGeometricEntities, '/geometric_entities/', 'geometric_entities'],
    [GetSubunits, '/subunits/<int:id_>', 'subunits'],
    [GetNetworkVisualisation,
     '/network_visualisation/',
     'network_visualisation'],]

display = [
    [DisplayImage, '/display/<path:filename>', 'display'],
    [IIIFManifest, '/iiif_manifest/<int:version>/<int:id_>', 'iiif_manifest'],
    [IIIFImage, '/iiif_image/<int:id_>.json', 'iiif_image'],
    [IIIFCanvas, '/iiif_canvas/<int:id_>.json', 'iiif_canvas'],
    [IIIFSequence, '/iiif_sequence/<int:id_>.json', 'iiif_sequence'],
    [IIIFAnnotationList, '/iiif_annotation_list/<int:image_id>.json',
     'iiif_annotation_list'],
    [IIIFAnnotation, '/iiif_annotation/<int:annotation_id>.json',
     'iiif_annotation']]

routes = entity + admin + types + special + display
