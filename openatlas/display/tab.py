from __future__ import annotations

from typing import Optional, TYPE_CHECKING


from flask_babel import LazyString, lazy_gettext as _
from flask_wtf import FlaskForm

from openatlas.display.table import Table
from openatlas.display.util2 import uc_first

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity


class Tab:

    def __init__(
            self,
            name: str | LazyString,
            label: Optional[str | LazyString] = None,
            content: Optional[str | LazyString] = None,
            table: Optional[Table] = None,
            buttons: Optional[list[str | LazyString]] = None,
            entity: Optional[Entity] = None,
            form: Optional[FlaskForm] = None,
            tooltip: Optional[str | LazyString] = None) -> None:

        self.name = name
        self.label = uc_first(label or _(name.replace('_', ' ')))
        self.content = content
        self.entity = entity
        self.form = form
        self.table = table or Table()
        self.tooltip = uc_first(tooltip)
        self.buttons: list[str | LazyString] = buttons or []
