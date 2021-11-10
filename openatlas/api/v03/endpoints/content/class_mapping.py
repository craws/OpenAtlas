from typing import Tuple, Union

from flask import Response, g
from flask_restful import Resource, marshal

from openatlas.api.v03.templates.class_mapping import ClassMappingTemplate


class ClassMapping(Resource):  # type: ignore

    def get(self) -> Union[Tuple[Resource, int], Response]:
        mapping = []
        for class_ in g.classes.values():
            if class_.cidoc_class:
                mapping.append({
                    "systemClass": class_.name,
                    "crmClass": class_.cidoc_class.code,
                    "view": class_.view,
                    "icon": class_.icon,
                    "en": class_.label})

        return marshal(mapping, ClassMappingTemplate.class_template()), 200
