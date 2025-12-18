from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm

from openatlas.display.table import Table
from openatlas.display.util2 import uc_first

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity


@dataclass
class Tab:
    name: str
    label: Optional[str] = None
    content: Optional[str] = None
    table: Table = field(
        default_factory=lambda: Table())  # pylint: disable=unnecessary-lambda
    buttons: list[str] = field(default_factory=list)
    entity: Optional[Entity] = None
    form: Optional[FlaskForm] = None
    tooltip: Optional[str] = None

    def __post_init__(self) -> None:
        self.label = uc_first(self.label or _(self.name.replace('_', ' ')))
        self.tooltip = uc_first(self.tooltip)
