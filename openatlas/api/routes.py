from flask_restful import Api

from openatlas.api.v02.endpoints.content.class_mapping import ClassMapping
from openatlas.api.v02.endpoints.content.content import GetContent
from openatlas.api.v02.endpoints.content.geometric_entities import (
    GetGeometricEntities)
from openatlas.api.v02.endpoints.content.overview_count import OverviewCount
from openatlas.api.v02.endpoints.content.systemclass_count import (
    SystemClassCount)
from openatlas.api.v02.endpoints.display_image import DisplayImage
from openatlas.api.v02.endpoints.entity.class_ import GetByClass
from openatlas.api.v02.endpoints.entity.code import GetByCode
from openatlas.api.v02.endpoints.entity.entity import GetEntity
from openatlas.api.v02.endpoints.entity.latest import GetLatest
from openatlas.api.v02.endpoints.entity.linked_entities import GetLinkedEntities
from openatlas.api.v02.endpoints.entity.query import GetQuery
from openatlas.api.v02.endpoints.entity.system_class import GetBySystemClass
from openatlas.api.v02.endpoints.entity.type_entities import GetTypeEntities
from openatlas.api.v02.endpoints.entity.type_entities_all import (
    GetTypeEntitiesAll)
from openatlas.api.v02.endpoints.node.node_entities import GetNodeEntities
from openatlas.api.v02.endpoints.node.node_entities_all import (
    GetNodeEntitiesAll)
from openatlas.api.v02.endpoints.node.node_overview import GetNodeOverview
from openatlas.api.v02.endpoints.node.subunit import GetSubunit
from openatlas.api.v02.endpoints.node.subunit_hierarchy import (
    GetSubunitHierarchy)
from openatlas.api.v02.endpoints.node.type_tree import GetTypeTree


def add_routes(api: Api) -> None:
    api.add_resource(
        GetByCode,
        '/code/<string:code>',
        endpoint="code")
    api.add_resource(
        GetByClass,
        '/class/<string:class_code>',
        endpoint="class")
    api.add_resource(
        GetEntity,
        '/entity/<int:id_>',
        endpoint='entity')
    api.add_resource(
        GetLatest,
        '/latest/<int:latest>',
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
        GetGeometricEntities,
        '/geometric_entities/',
        endpoint="geometric_entities")
    api.add_resource(
        GetLinkedEntities,
        '/entities_linked_to_entity/<int:id_>',
        endpoint="entities_linked_to_entity")
    api.add_resource(
        GetNodeEntities,
        '/node_entities/<int:id_>',
        endpoint="node_entities")
    api.add_resource(
        GetNodeEntitiesAll,
        '/node_entities_all/<int:id_>',
        endpoint="node_entities_all")
    api.add_resource(
        GetNodeOverview,
        '/node_overview/',
        endpoint="node_overview")
    api.add_resource(
        GetSubunit,
        '/subunit/<int:id_>',
        endpoint="subunit")
    api.add_resource(
        GetSubunitHierarchy,
        '/subunit_hierarchy/<int:id_>',
        endpoint="subunit_hierarchy")
    api.add_resource(
        GetTypeTree,
        '/type_tree/',
        endpoint="type_tree")

    api.add_resource(
        GetContent,
        '/content/',
        endpoint="content")
    api.add_resource(
        OverviewCount,
        '/overview_count/',
        endpoint='overview_count')  # Deprecated
    api.add_resource(
        ClassMapping,
        '/classes/',
        endpoint='class_mapping')
    api.add_resource(
        SystemClassCount,
        '/system_class_count/',
        endpoint='system_class_count')

    api.add_resource(
        DisplayImage,
        '/display/<path:filename>',
        endpoint='display')
