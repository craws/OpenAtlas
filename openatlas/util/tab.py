from typing import List, Optional

from flask import url_for

from openatlas.models.entity import Entity
from openatlas.util.table import Table
from openatlas.util.util import button, uc_first
from flask_babel import lazy_gettext as _

# needed for translations
_('member of')


class Tab:

    def __init__(self,
                 id_: str,
                 origin: Optional[Entity] = None,
                 buttons: Optional[List[str]] = None,
                 table: Optional[Table] = None) -> None:
        self.id = id_
        self.title = uc_first(_(id_.replace('_', ' ')))
        self.buttons = buttons if buttons else []
        self.table = table
        if origin and id_ == 'source':
            if origin.class_.code == 'E31':
                self.buttons = [
                    button(_('add'), url_for('reference_add', id_=origin.id, class_name='source'))]
            if origin.system_type == 'file':
                self.buttons = [
                    button(_('add'), url_for('file_add', id_=origin.id, class_name='source'))]
            else:
                self.buttons = [button(_('add'), url_for('entity_add_source', id_=origin.id))]
            self.buttons.append(button(_('source'), url_for('source_insert', origin_id=origin.id)))

