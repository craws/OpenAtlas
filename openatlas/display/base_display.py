from typing import Any, Optional, Union

from flask import render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas.database.gis import Gis
from openatlas.database.link import Link
from openatlas.database.type import Type
from openatlas.database.user import User
from openatlas.display.tab import Tab
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.util import (
    bookmark_toggle, button, display_delete_link, download_button, format_date,
    get_entity_data, is_authorized, link, manual, siblings_pager, uc_first)


class BaseDisplay:

    entity: Union[Entity, Type]
    tabs: dict[str, Tab]
    event_links: Optional[list[Link]] = None  # Needed for actor and info data
    gis_data: list[dict[str, Any]] = None
    structure = None
    overlays = None

    def __init__(self, entity: Union[Entity, Type]) -> None:
        self.entity = entity
        self.add_tabs()
        self.add_info_content()  # Call later because of profile image
        self.entity.image_id = entity.get_profile_image_id()

    def add_tabs(self) -> None:
        self.tabs = {'info': Tab('info')}

    def add_info_content(self):
        self.entity.info_data = get_entity_data(
            self.entity,
            event_links=self.event_links)
        #if not self.gis_data:
        #    self.gis_data = Gis.get_all(self.entity.linked_places) \
        #        if self.entity.linked_places else None

        problematic_type_id = self.entity.check_too_many_single_type_links()
        buttons = [manual(f'entity/{self.entity.class_.view}')]
        buttons += self.add_buttons(bool(problematic_type_id))
        buttons.append(bookmark_toggle(self.entity.id))
        #if self.entity.class_.view == 'file':
        #    if self.entity.image_id:
        #        buttons.append(download_button(self.entity))
        #    else:
        #        buttons.append(
        #            '<span class="error">' + uc_first(_("missing file")) +
        #            '</span>')
        # buttons.append(siblings_pager(self.entity, self.structure))
        self.tabs['info'].content = render_template(
            'entity/view.html',
            buttons=buttons,
            entity=self.entity,
            gis_data=self.gis_data,
            overlays=self.overlays,
            title=self.entity.name,
            problematic_type_id=problematic_type_id)

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

    def add_buttons(self, type_problem: bool = False) -> list[str]:
        if not is_authorized(self.entity.class_.write_access):
            return []  # pragma: no cover
        buttons = []
        if isinstance(self.entity, Type):
            if self.entity.root and self.entity.category != 'system':
                buttons.append(
                    button(_('edit'), url_for('update', id_=self.entity.id)))
                buttons.append(display_delete_link(self.entity))
        elif isinstance(self.entity, ReferenceSystem):
            buttons.append(button(_('edit'), url_for('update', id_=self.entity.id)))
            if not self.entity.classes and not self.entity.system:
                buttons.append(display_delete_link(self.entity))
        elif self.entity.class_.name == 'source_translation':
            buttons.append(button(_('edit'), url_for('update', id_=self.entity.id)))
            buttons.append(display_delete_link(self.entity))
        else:
            if not type_problem:
                buttons.append(
                    button(_('edit'), url_for('update', id_=self.entity.id)))
            if self.entity.class_.view != 'place' \
                    or not self.entity.get_linked_entities('P46'):
                buttons.append(display_delete_link(self.entity))
        if self.entity.class_.name == 'stratigraphic_unit':
            buttons.append(
                button(
                    _('tools'),
                    url_for('anthropology_index', id_=self.entity.id)))
        return buttons
