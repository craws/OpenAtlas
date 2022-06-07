import ast
from typing import Any, Optional, Union

from flask_wtf import FlaskForm
from wtforms import HiddenField

from openatlas.models.entity import Entity


class BaseForm:
    name: str = ''
    fields: list[str] = []
    form: FlaskForm = None
    entity: Optional[Entity] = None
    origin: Optional[Entity] = None

    def __init__(
            self,
            name: str,
            entity: Union[Entity, None],
            origin: Union[Entity, None]):

        self.name = name
        self.entity = entity
        self.origin = origin

    class Form(FlaskForm):
        origin_id = HiddenField()

    def additional_fields(self) -> dict[str, Any]:
        pass

    def populate_insert(self) -> None:
        pass

    def populate_update(self) -> None:
        pass

    def process_form_data(self, entity: Optional[Entity] = None) -> None:
        pass


def convert(value: str) -> list[int]:
    if not value:
        return []
    ids = ast.literal_eval(value)
    return ids if isinstance(ids, list) else [int(ids)]
