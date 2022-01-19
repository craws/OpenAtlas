from typing import Any

from flask_restful import fields


class TypeTreeTemplate:

    @staticmethod
    def type_tree_template() -> dict[str, Any]:
        return {'typeTree': fields.Raw}
