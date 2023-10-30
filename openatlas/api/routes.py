from flask_restful import Api

from openatlas.api.endpoints.iiif import \
    (IIIFManifest, IIIFImageV2, IIIFCanvasV2, IIIFSequenceV2)
from openatlas.api.endpoints.content import ClassMapping, \
    GetContent, SystemClassCount, GetBackendDetails
from openatlas.api.endpoints.special import GetGeometricEntities, \
    ExportDatabase, GetSubunits
from openatlas.api.endpoints.display_image import \
    (DisplayImage, LicensedFileOverview)
from openatlas.api.endpoints.entities import GetByCidocClass, \
    GetBySystemClass, GetByViewClass, GetEntitiesLinkedToEntity, GetEntity, \
    GetLatest, GetQuery, GetTypeEntities, GetTypeEntitiesAll
from openatlas.api.endpoints.type import \
    (GetTypeByViewClass, GetTypeOverview, GetTypeTree)


def entity_routes(api: Api) -> None:
    api.add_resource(
        GetByViewClass,
        '/view_class/<string:view_class>',
        endpoint="view_class")
    api.add_resource(
        GetByCidocClass,
        '/cidoc_class/<string:cidoc_class>',
        endpoint="cidoc_class")
    api.add_resource(
        GetEntity,
        '/entity/<int:id_>',
        endpoint='entity')
    api.add_resource(
        GetLatest,
        '/latest/<int:limit>',
        endpoint="latest")
    api.add_resource(
        GetQuery,
        '/query/',
        endpoint="query")
    api.add_resource(
        GetBySystemClass,
        '/system_class/<string:system_class>',
        endpoint="system_class")
    api.add_resource(
        GetTypeEntities,
        '/type_entities/<int:id_>',
        endpoint="type_entities")
    api.add_resource(
        GetTypeEntitiesAll,
        '/type_entities_all/<int:id_>',
        endpoint="type_entities_all")
    api.add_resource(
        GetEntitiesLinkedToEntity,
        '/entities_linked_to_entity/<int:id_>',
        endpoint="entities_linked_to_entity")


def admin_routes(api: Api) -> None:
    api.add_resource(
        GetBackendDetails,
        '/backend_details/',
        endpoint="backend_details")
    api.add_resource(
        ClassMapping,
        '/classes/',
        endpoint='class_mapping')
    api.add_resource(
        SystemClassCount,
        '/system_class_count/',
        endpoint='system_class_count')
    api.add_resource(
        LicensedFileOverview,
        '/licensed_file_overview/',
        endpoint='licensed_file_overview')


def type_routes(api: Api) -> None:
    api.add_resource(
        GetTypeOverview,
        '/type_overview/',
        endpoint="type_overview")
    api.add_resource(
        GetTypeTree,
        '/type_tree/',
        endpoint="type_tree")
    api.add_resource(
        GetTypeByViewClass,
        '/type_by_view_class/',
        endpoint="type_by_view_class")


def special_routes(api: Api) -> None:
    api.add_resource(
        GetSubunits,
        '/subunits/<int:id_>',
        endpoint="subunits")
    api.add_resource(
        GetGeometricEntities,
        '/geometric_entities/',
        endpoint="geometric_entities")
    api.add_resource(
        ExportDatabase,
        '/export_database/<string:format_>',
        endpoint="export_database")


def deprecated_routes(api: Api) -> None:
    api.add_resource(
        GetContent,
        '/content/',
        endpoint="content")


def display_routes(api: Api) -> None:
    api.add_resource(
        DisplayImage,
        '/display/<path:filename>',
        endpoint='display')

    api.add_resource(
        IIIFManifest,
        '/iiif_manifest/<int:version>/<int:id_>',
        endpoint='iiif_manifest')
    api.add_resource(
        IIIFImageV2,
        '/iiif_image/<int:id_>.json',
        endpoint='iiif_image')
    api.add_resource(
        IIIFCanvasV2,
        '/iiif_canvas/<int:id_>.json',
        endpoint='iiif_canvas')
    api.add_resource(
        IIIFSequenceV2,
        '/iiif_sequence/<int:id_>.json',
        endpoint='iiif_sequence')
