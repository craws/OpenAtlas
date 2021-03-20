from flask_restful import fields


class TypeTreeTemplate:

    @staticmethod
    def type_tree_template():
        types = {'type_tree': fields.Raw}
        return types

