from typing import Union

from flask_restful import fields
from flask_restful.fields import List


class SubunitTemplate:

    @staticmethod
    def subunit_template(id_: Union[int, str]) -> dict[str, List]:
        standard_type = {
            'name': fields.String,
            'id': fields.Integer,
            'rootId': fields.Integer,
            'path': fields.String}
        timespan = {
            'earliestBegin': fields.String,
            'latestBegin': fields.String,
            'earliestEnd': fields.String,
            'latestEnd': fields.String}
        external_references = {
            'type': fields.String,
            'identifier': fields.String,
            'referenceSystem': fields.String}
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
            'unit': fields.String}
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
        return {str(id_): fields.List(fields.Nested(json))}
