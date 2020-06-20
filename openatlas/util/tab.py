from typing import List, Optional

from flask import url_for

from openatlas.models.entity import Entity
from openatlas.util.table import Table
from openatlas.util.util import button, is_authorized, uc_first
from flask_babel import lazy_gettext as _

# needed for translations
_('member of')


class Tab:
    id: str
    origin: Optional[Entity]

    def __init__(self,
                 id_: str,
                 origin: Optional[Entity] = None,
                 buttons: Optional[List[str]] = None,
                 table: Optional[Table] = None) -> None:
        self.id = id_
        self.title = uc_first(_(id_.replace('_', ' ')))
        self.buttons = buttons if buttons else []
        self.table = table
        self.origin = origin
        if self.origin and is_authorized('contributor'):
            self.buttons = self.add_buttons()

    def add_buttons(self):
        buttons = []
        if self.id == 'source':
            if self.origin.class_.code == 'E31':
                buttons.append(button(_('add'), url_for('reference_add',
                                                        id_=self.origin.id,
                                                        class_name='source')))
            if self.origin.system_type == 'file':
                buttons.append(button(_('add'), url_for('file_add',
                                                        id_=self.origin.id,
                                                        class_name='source')))
            else:
                buttons.append(button(_('add'), url_for('entity_add_source', id_=self.origin.id)))
            buttons.append(button(_('source'), url_for('source_insert', origin_id=self.origin.id)))
        return buttons
