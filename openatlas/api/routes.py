from openatlas.api.endpoints.content import (
    ClassMapping, Classes, GetBackendDetails, SystemClassCount)
from openatlas.api.endpoints.display_image import (
    DisplayImage, LicensedFileOverview)
from openatlas.api.endpoints.entities import (
    GetByCidocClass, GetBySystemClass, GetByViewClass,
    GetEntitiesLinkedToEntity, GetEntity, GetLatest, GetQuery, GetTypeEntities,
    GetTypeEntitiesAll)
from openatlas.api.endpoints.iiif import (
    IIIFAnnotationList, IIIFAnnotation, IIIFCanvas, IIIFImage,
    IIIFManifest, IIIFSequence)
from openatlas.api.endpoints.special import (
    ExportDatabase, GetGeometricEntities, GetSubunits)
from openatlas.api.endpoints.type import (
    GetTypeByViewClass, GetTypeOverview, GetTypeTree)

entity = [
    [GetByViewClass, '/view_class/<string:view_class>', "view_class"],
    [GetByCidocClass, '/cidoc_class/<string:cidoc_class>', "cidoc_class"],
    [GetEntity, '/entity/<int:id_>', 'entity'],
    [GetLatest, '/latest/<int:limit>', "latest"],
    [GetQuery, '/query/', "query"],
    [GetBySystemClass, '/system_class/<string:system_class>', "system_class"],
    [GetTypeEntities, '/type_entities/<int:id_>', "type_entities"],
    [GetTypeEntitiesAll, '/type_entities_all/<int:id_>', "type_entities_all"],
    [GetEntitiesLinkedToEntity,
     '/entities_linked_to_entity/<int:id_>',
     "entities_linked_to_entity"]]

admin = [
    [SystemClassCount, '/system_class_count/', 'system_class_count'],
    [GetBackendDetails, '/backend_details/', "backend_details"],
    [ClassMapping, '/class_mapping/', 'class_mapping'],
    [LicensedFileOverview, '/licensed_file_overview/',
     'licensed_file_overview'],
    [Classes, '/classes/', 'classes']]

types = [
    [GetTypeByViewClass, '/type_by_view_class/', "type_by_view_class"],
    [GetTypeOverview, '/type_overview/', "type_overview"],
    [GetTypeTree, '/type_tree/', "type_tree"]]

special = [
    [ExportDatabase, '/export_database/<string:format_>', "export_database"],
    [GetGeometricEntities, '/geometric_entities/', "geometric_entities"],
    [GetSubunits, '/subunits/<int:id_>', "subunits"]]

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
