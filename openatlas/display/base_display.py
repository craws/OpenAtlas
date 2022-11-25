from typing import Union

from flask import url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas.database.type import Type
from openatlas.database.user import User
from openatlas.display.tab import Tab
from openatlas.models.entity import Entity
from openatlas.util.util import format_date, link, uc_first


class BaseDisplay:

    entity: Union[Entity, Type]
    tabs: dict[str, Tab]

    def __init__(self, entity: Union[Entity, Type]) -> None:
        self.entity = entity
        self.add_tabs()
        # self.add_info_content()  # Call later because of profile image
        self.add_tabs_buttons()
        self.entity.image_id = entity.get_profile_image_id()

    def add_tabs(self) -> None:
        self.tabs = {'info': Tab('info')}

    def add_tabs_buttons(self) -> None:
        for tab in self.tabs.values():
            pass
            # tab.add_buttons(self.entity)

    def add_note_tab(self) -> None:
        self.tabs['note'] = Tab('note', entity=self.entity)
        for note in current_user.get_notes_by_entity_id(self.entity.id):
            data = [
                format_date(note['created']),
                uc_first(_('public'))
                if note['public'] else uc_first(_('private')),
                link(User.get_by_id(note['user_id'])),
                note['text'],
                f'<a href="{url_for("note_view", id_=note["id"])}">' +
                uc_first(_("view")) + '</a>']
            self.tabs['note'].table.rows.append(data)
