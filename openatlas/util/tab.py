from typing import List, Optional

from openatlas.util.table import Table
from openatlas.util.util import uc_first
from flask_babel import lazy_gettext as _


class Tab:

    def __init__(self,
                 id_: str,
                 buttons: Optional[List[str]] = None,
                 table: Optional[Table] = None) -> None:
        self.id = id_
        self.title = uc_first(_(id_.replace('_', ' ')))
        self.buttons = buttons if buttons else []
        self.table = table

        # needed for translations
        _('member of')
