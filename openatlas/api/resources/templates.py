from __future__ import annotations

from collections import defaultdict
from typing import Any, TYPE_CHECKING, Type

from flask import g
from flask_restful import fields
from flask_restful.fields import Integer, List, Nested, String

from openatlas import app
from openatlas.models.entity import Entity

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.api.endpoints.parser import Parser

start = {
    'earliest': fields.String,
    'latest': fields.String,
    'comment': fields.String}
end = {
    'earliest': fields.String,
    'latest': fields.String,
    'comment': fields.String}
description = {'value': fields.String}
timespans = {'start': fields.Nested(start), 'end': fields.Nested(end)}

external_references = {
    'type': fields.String,
    'identifier': fields.String,
    'referenceSystem': fields.String,
    'resolverURL': fields.String,
    'referenceURL': fields.String,
    'id': fields.String}


def geojson_template() -> dict[str, Any]:
    types = {
        'typeName': fields.String,
        'typeHierarchy': fields.String,
        'typeId': fields.Integer}

    properties = {
        '@id': fields.Integer,
        'systemClass': fields.String,
        'viewClass': fields.String,
        'name': fields.String,
        'description': fields.String,
        'begin_earliest': fields.String,
        'begin_latest': fields.String,
        'begin_comment': fields.String,
        'end_earliest': fields.String,
        'end_latest': fields.String,
        'end_comment': fields.String,
        'types': fields.List(fields.Nested(types))}

    return {
        'type': fields.String,
        'geometry': fields.Raw,
        'properties': fields.Nested(properties)}


def geojson_collection_template() -> dict[str, Any]:
    return {
        'type': fields.String,
        'features': fields.List(
            fields.Nested(geojson_template()))}


def geometries_template() -> dict[str, Any]:
    properties = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'locationId': fields.Integer,
        'objectId': fields.Integer,
        'objectDescription': fields.String,
        'objectName': fields.String,
        'objectType': fields.String,
        'shapeType': fields.String}

    feature = {
        'type': fields.String,
        'geometry': fields.Raw,
        'properties': fields.Nested(properties)}

    return {'type': fields.String, 'features': fields.Nested(feature)}


def linked_places_template(parser: Parser) -> dict[str, Type[String]]:
    title = {'title': fields.String}
    depictions = {
        '@id': fields.String,
        'title': fields.String,
        'license': fields.String,
        'licenseHolder': fields.String,
        'creator': fields.String,
        'publicShareable': fields.Boolean,
        'url': fields.String,
        'mimetype': fields.String,
        'IIIFBasePath': fields.String,
        'IIIFManifest': fields.String}
    links = {
        'referenceURL': fields.String,
        'id': fields.String,
        'resolverURL': fields.String,
        'type': fields.String,
        'identifier': fields.String,
        'referenceSystem': fields.String}
    types = {
        'identifier': fields.String,
        'label': fields.String,
        'descriptions': fields.String,
        'hierarchy': fields.String,
        'typeHierarchy': fields.List(fields.Nested({
            'identifier': fields.String,
            'label': fields.String,
            'description': fields.String})),
        'value': fields.String,
        'unit': fields.String}

    names = {'alias': fields.String}

    when = {'timespans': fields.List(fields.Nested(timespans))}
    relations = {
        'label': fields.String,
        'relationTo': fields.String,
        'relationType': fields.String,
        'relationSystemClass': fields.String,
        'relationDescription': fields.String,
        'type': fields.String,
        'when': fields.Nested(when)}
    if parser.format == 'lpx':
        relations['relationTypeLabel'] = fields.String
    feature = {
        '@id': fields.String,
        'type': fields.String,
        'crmClass': fields.String,
        'systemClass': fields.String,
        'viewClass': fields.String,
        'properties': fields.Nested(title),
        'descriptions': fields.List(fields.Nested(description))}
    show = parser.show
    if 'when' in show:
        feature['when'] = fields.Nested(when)
    if 'types' in show:
        feature['types'] = fields.List(fields.Nested(types))
    if 'relations' in show:
        feature['relations'] = fields.List(fields.Nested(relations))
    if 'names' in show:
        feature['names'] = fields.List(fields.Nested(names))
    if 'links' in show:
        feature['links'] = fields.List(fields.Nested(links))
    if 'depictions' in show:
        feature['depictions'] = fields.List(fields.Nested(depictions))
    feature['geometry'] = fields.Raw

    return {
        '@context': fields.String,
        'type': fields.String,
        'features': fields.List(fields.Nested(feature))}


def pagination() -> dict[str, List | Nested]:
    page_index = {"page": fields.Integer, "startId": fields.Integer}
    return {
        "entities": fields.Integer,
        "entitiesPerPage": fields.Integer,
        "index": fields.List(fields.Nested(page_index)),
        "totalPages": fields.Integer}


def linked_place_pagination(parser: Parser) -> dict[str, Any]:
    return {
        "results": fields.List(fields.Nested(
            linked_places_template(parser))),
        "pagination": fields.Nested(pagination())}


def geojson_pagination() -> dict[str, Any]:
    return {
        "results": fields.List(fields.Nested(geojson_collection_template())),
        "pagination": fields.Nested(pagination())}


def loud_pagination() -> dict[str, Any]:
    return {
        "results": fields.List(fields.Raw),
        "pagination": fields.Nested(pagination())}


def loud_template(result: dict[str, Any]) -> dict[str, Any]:
    template = {}
    for item in result:
        template[item] = fields.Raw
    return template


def presentation_template() -> dict[str, Any]:
    hierarchy = {
        'label': fields.String,
        'descriptions': fields.String,
        'identifier': fields.String}
    types = {
        'id': fields.Integer,
        'title': fields.String,
        'descriptions': fields.String,
        'isStandard': fields.Boolean,
        'typeHierarchy': fields.List(fields.Nested(hierarchy)),
        'value': fields.Float,
        'unit': fields.String}
    references = {
        'id': fields.Integer,
        'systemClass': fields.String,
        'title': fields.String,
        'type': fields.String,
        'typeId': fields.Integer,
        'citation': fields.String,
        'pages': fields.String}
    files = {
        'id': fields.Integer,
        'title': fields.String,
        'license': fields.String,
        'creator': fields.String,
        'licenseHolder': fields.String,
        'publicShareable': fields.Boolean,
        'mimetype': fields.String,
        'url': fields.String,
        'fromSuperEntity': fields.Boolean,
        'IIIFManifest': fields.String,
        'IIIFBasePath': fields.String,
        'overlay': fields.String}
    relation_types = {
        'property': fields.String,
        'relationTo': fields.Integer,
        'type': fields.String,
        'description': fields.String,
        'when': fields.Nested(timespans)}
    relations = {
        'id': fields.Integer,
        'systemClass': fields.String,
        'title': fields.String,
        'description': fields.String,
        'aliases': fields.List(fields.String),
        'geometries': fields.Raw,
        'when': fields.Nested(timespans),
        'standardType': fields.Nested({
            'id': fields.Integer,
            'title': fields.String}),
        'relationTypes': fields.List(fields.Nested(relation_types))}

    def get_relations() -> fields:
        dict_ = {}
        for name in g.classes:
            if name in app.config['API_PRESENTATION_EXCLUDE_RELATION']:
                continue
            dict_[name] = fields.List(fields.Nested(relations))
        return fields.Nested(dict_)

    return {
        'id': fields.Integer,
        'systemClass': fields.String,
        'viewClass': fields.String,
        'title': fields.String,
        'description': fields.String,
        'aliases': fields.List(fields.String),
        'geometries': fields.Raw,
        'when': fields.Nested(timespans),
        'types': fields.List(fields.Nested(types)),
        'externalReferenceSystems': fields.List(
            fields.Nested(external_references)),
        'references': fields.List(fields.Nested(references)),
        'files': fields.List(fields.Nested(files)),
        'relations': get_relations()}


def subunit_template(id_: str) -> dict[str, List]:
    timespan = {
        'earliestBegin': fields.String,
        'latestBegin': fields.String,
        'earliestEnd': fields.String,
        'latestEnd': fields.String}
    standard_type = {
        'name': fields.String,
        'id': fields.Integer,
        'rootId': fields.Integer,
        'path': fields.String,
        'externalReferences': fields.List(fields.Nested(external_references))}
    references = {
        'id': fields.Integer,
        'abbreviation': fields.String,
        'title': fields.String,
        'pages': fields.String}
    files = {
        'id': fields.Integer,
        'name': fields.String,
        'fileName': fields.String,
        'license': fields.String,
        'source': fields.String}
    types = {
        'id': fields.Integer,
        'rootId': fields.Integer,
        'name': fields.String,
        'path': fields.String,
        'value': fields.Float,
        'unit': fields.String,
        'externalReferences': fields.List(fields.Nested(external_references))}
    properties = {
        'name': fields.String,
        'aliases': fields.List(fields.String),
        'description': fields.String,
        'standardType': fields.Nested(standard_type),
        'timespan': fields.Nested(timespan),
        'externalReferences': fields.List(
            fields.Nested(external_references)),
        'references': fields.List(fields.Nested(references)),
        'files': fields.List(fields.Nested(files)),
        'types': fields.List(fields.Nested(types))}
    json = {
        'id': fields.Integer,
        'parentId': fields.Integer,
        'rootId': fields.Integer,
        'openatlasClassName': fields.String,
        'crmClass': fields.String,
        'created': fields.String,
        'modified': fields.String,
        'latestModRec': fields.String,
        'geometry': fields.Raw,
        'children': fields.List(fields.Integer),
        'properties': fields.Nested(properties)}

    return {id_: fields.List(fields.Nested(json))}


def overview_template() -> dict[str, Type[String | Integer]]:
    return {
        'acquisition': fields.Integer,
        'activity': fields.Integer,
        'administrative_unit': fields.Integer,
        'artifact': fields.Integer,
        'bibliography': fields.Integer,
        'creation': fields.Integer,
        'edition': fields.Integer,
        'external_reference': fields.Integer,
        'event': fields.Integer,
        'feature': fields.Integer,
        'file': fields.Integer,
        'group': fields.Integer,
        'human_remains': fields.Integer,
        'modification': fields.Integer,
        'move': fields.Integer,
        'person': fields.Integer,
        'place': fields.Integer,
        'production': fields.Integer,
        'reference_system': fields.Integer,
        'type': fields.Integer,
        'source_translation': fields.Integer,
        'stratigraphic_unit': fields.Integer,
        'source': fields.Integer}


def type_tree_template() -> dict[str, Any]:
    return {'typeTree': fields.Raw}


def type_overview_template() -> dict[str, Any]:
    children = {
        'id': fields.Integer,
        'url': fields.String,
        'name': fields.String,
        'children': fields.List(fields.Raw)}
    type_details = {
        'id': fields.Integer,
        'name': fields.String,
        'viewClass': fields.List(fields.String),
        'children': fields.List(fields.Nested(children))}

    return {
        'standard': fields.List(fields.Nested(type_details)),
        'place': fields.List(fields.Nested(type_details)),
        'custom': fields.List(fields.Nested(type_details)),
        'value': fields.List(fields.Nested(type_details)),
        'system': fields.List(fields.Nested(type_details))}


def type_by_view_class_template(types: dict[str, Any]) -> dict[str, Any]:
    children = {
        'id': fields.Integer,
        'url': fields.String,
        'name': fields.String,
        'children': fields.List(fields.Raw)}
    type_details = {
        'id': fields.Integer,
        'name': fields.String,
        'category': fields.String,
        'children': fields.List(fields.Nested(children))}

    dict_: dict[str, Any] = defaultdict()
    for key in types:
        dict_[key] = fields.List(fields.Nested(type_details))
    return dict_


def class_overview_template() -> dict[str, Type[String]]:
    return {
        'systemClass': fields.String,
        'crmClass': fields.String,
        'view': fields.String,
        'standardTypeId': fields.String,
        'icon': fields.String,
        'en': fields.String}


def class_mapping_template() -> dict[str, Type[String]]:
    return {
        'locale': fields.String,
        'results': fields.List(fields.Nested({
            'label': fields.String,
            'systemClass': fields.String,
            'crmClass': fields.String,
            'view': fields.String,
            'standardTypeId': fields.String,
            'icon': fields.String}))}


def properties_template(properties: dict[str, Any]) -> dict[str, Type[String]]:
    properties_dict = {
        'id': fields.String,
        'name': fields.String,
        'nameInverse': fields.String,
        'code': fields.String,
        'domainClassCode': fields.String,
        'rangeClassCode': fields.String,
        'count': fields.String,
        'sub': fields.String,
        'super': fields.String,
        'i18n': fields.Raw,
        'i18nInverse': fields.Raw}
    dict_: dict[str, Any] = defaultdict()
    for key in properties:
        dict_[key] = fields.Nested(properties_dict)
    return dict_


def backend_details_template() -> dict[str, Type[String]]:
    return {
        'version': fields.String,
        'apiVersions': fields.Raw,
        'siteName': fields.String,
        'imageProcessing': fields.Nested({
            'enabled': fields.String,
            'availableImageSizes': fields.Raw}),
        'IIIF': fields.Nested({
            'enabled': fields.String,
            'url': fields.String,
            'version': fields.String})}


def licensed_file_template(entities: list[Entity]) -> dict[str, Any]:
    template: dict[str, Any] = defaultdict()
    file = {
        'display': fields.String,
        'thumbnail': fields.String,
        'extension': fields.String,
        'mimetype': fields.String,
        'license': fields.String,
        'creator': fields.String,
        'licenseHolder': fields.String,
        'publicShareable': fields.Boolean,
        'IIIFManifest': fields.String}
    for entity in entities:
        template[str(entity.id)] = fields.Nested(file)
    return template


def network_visualisation_template() -> dict[str, Any]:
    return {'results': fields.List(fields.Nested({
        'id': fields.Integer,
        'label': fields.String,
        'systemClass': fields.String,
        'relations': fields.List(fields.Integer)}))}
