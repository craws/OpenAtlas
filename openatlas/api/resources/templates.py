from collections import defaultdict
from typing import Any, Type, Union

from flask_restful import fields
from flask_restful.fields import Integer, List, Nested, String


def geojson_template() -> dict[str, Any]:
    types = {
        'typeName': fields.String,
        'typeHierarchy': fields.String,
        'typeId': fields.Integer}

    properties = {
        '@id': fields.Integer,
        'systemClass': fields.String,
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


def linked_places_template(show: str) -> dict[str, Type[String]]:
    title = {'title': fields.String}
    depictions = {
        '@id': fields.String,
        'title': fields.String,
        'license': fields.String,
        'url': fields.String}
    links = {
        'type': fields.String,
        'identifier': fields.String,
        'referenceSystem': fields.String}
    types = {
        'identifier': fields.String,
        'label': fields.String,
        'descriptions': fields.String,
        'hierarchy': fields.String,
        'value': fields.Float,
        'unit': fields.String}

    names = {'alias': fields.String}
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
    when = {'timespans': fields.List(fields.Nested(timespans))}
    relations = {
        'label': fields.String,
        'relationTo': fields.String,
        'relationType': fields.String,
        'relationSystemClass': fields.String,
        'relationDescription': fields.String,
        'type': fields.String,
        'when': fields.Nested(when)}
    feature = {
        '@id': fields.String,
        'type': fields.String,
        'crmClass': fields.String,
        'systemClass': fields.String,
        'properties': fields.Nested(title),
        'descriptions': fields.List(fields.Nested(description))}

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


def pagination() -> dict[str, Union[List, Nested]]:
    page_index = {"page": fields.Integer, "startId": fields.Integer}

    return {
        "entities": fields.Integer,
        "entitiesPerPage": fields.Integer,
        "index": fields.List(fields.Nested(page_index)),
        "totalPages": fields.Integer}


def linked_place_pagination(parser: dict[str, str]) -> dict[str, Any]:
    return {
        "results": fields.List(fields.Nested(
            linked_places_template(parser['show']))),
        "pagination": fields.Nested(pagination())}


def geojson_pagination() -> dict[str, Any]:
    return {
        "results": fields.List(fields.Nested(geojson_collection_template())),
        "pagination": fields.Nested(pagination())}


def loud_pagination() -> dict[str, Any]:
    return {
        "results": fields.Raw,
        "pagination": fields.Nested(pagination())}


def loud_template() -> dict[str, Any]:
    return {'': fields.Raw}


def subunit_template(id_: str) -> dict[str, List]:
    timespan = {
        'earliestBegin': fields.String,
        'latestBegin': fields.String,
        'earliestEnd': fields.String,
        'latestEnd': fields.String}
    external_references = {
        'type': fields.String,
        'identifier': fields.String,
        'referenceSystem': fields.String,
        'resolverURL': fields.String,
        'referenceURL': fields.String,
        'id': fields.String}
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


def overview_template() -> dict[str, Type[Union[String, Integer]]]:
    return {
        'move': fields.Integer,
        'bibliography': fields.Integer,
        'person': fields.Integer,
        'acquisition': fields.Integer,
        'reference_system': fields.Integer,
        'feature': fields.Integer,
        'file': fields.Integer,
        'activity': fields.Integer,
        'type': fields.Integer,
        'administrative_unit': fields.Integer,
        'artifact': fields.Integer,
        'source_translation': fields.Integer,
        'place': fields.Integer,
        'stratigraphic_unit': fields.Integer,
        'edition': fields.Integer,
        'group': fields.Integer,
        'source': fields.Integer}


def type_tree_template() -> dict[str, Any]:
    return {'typeTree': fields.Raw}


def type_overview_template() -> dict[str, Any]:
    children = {
        'id': fields.Integer,
        'url': fields.String,
        'label': fields.String,
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
        'label': fields.String,
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
        'icon': fields.String,
        'en': fields.String}


def content_template() -> dict[str, Type[String]]:
    return {
        'intro': fields.String,
        'contact': fields.String,
        'legalNotice': fields.String,
        'siteName': fields.String,
        'imageSizes': fields.Raw}
