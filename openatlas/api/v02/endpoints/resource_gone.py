from typing import Tuple, Type

from flask_restful import Resource

from openatlas.api.v02.resources.error import ResourceGoneError


class ResourceGone(Resource):  # type: ignore
    @staticmethod
    def get(*args: str, **kwargs: str) -> Tuple[Type[ResourceGoneError], int]:
        raise ResourceGoneError
