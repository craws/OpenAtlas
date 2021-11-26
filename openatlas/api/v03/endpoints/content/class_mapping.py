from typing import Tuple, Union

from flask import Response, g
from flask_restful import Resource, marshal

from openatlas.api.v03.templates.class_mapping import ClassMappingTemplate


class ClassMapping(Resource):
    # todo: add swagger
    def get(self) -> Union[Tuple[Resource, int], Response]:
        return marshal(
            ClassMapping.get_mapping(),
            ClassMappingTemplate.class_template()), 200

    @staticmethod
    def get_mapping():
        return [{
            "systemClass": class_.name,
            "crmClass": class_.cidoc_class.code,
            "view": class_.view,
            "icon": class_.icon,
            "en": class_.label}
            for class_ in g.classes.values() if class_.cidoc_class]
