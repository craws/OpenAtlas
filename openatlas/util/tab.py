from typing import List, Optional

from flask import g, url_for
from openatlas import app
from openatlas.models.entity import Entity
from openatlas.util.table import Table
from openatlas.util.util import button, is_authorized, uc_first
from flask_babel import lazy_gettext as _

# needed for translations
_('member of')
_('texts')


class Tab:
    name: str
    origin: Optional[Entity]

    def __init__(self,
                 name: str,
                 origin: Optional[Entity] = None,
                 buttons: Optional[List[str]] = None,
                 table: Optional[Table] = None) -> None:
        self.name = name
        self.title = uc_first(_(name.replace('_', ' ')))
        self.buttons = buttons if buttons else []
        self.table = table
        self.origin = origin
        if self.origin and is_authorized('contributor'):
            self.buttons = self.add_buttons()

    def add_buttons(self) -> List[str]:
        id_ = self.origin.id
        name = self.name
        buttons = []

        if name == 'source':
            if self.origin.system_type == 'file':
                buttons = [button(_('add'), url_for('file_add', id_=id_, class_name='source'))]
            elif self.origin.class_.code in app.config['CLASS_CODES']['reference']:
                buttons = [button(_('add'), url_for('reference_add', id_=id_, class_name='source'))]
            else:
                buttons = [button(_('add'), url_for('entity_add_source', id_=id_))]
            buttons.append(button(_('source'), url_for('source_insert', origin_id=id_)))

        elif name == 'event':
            if self.origin.class_.code == 'E84':
                buttons = [button(g.classes['E9'].name,
                                  url_for('event_insert', code='E9', origin_id=id_))]
            else:
                if self.origin.system_type == 'file':
                    buttons = [button('add', url_for('file_add', id_=id_, class_name='event'))]
                elif self.origin.class_.code in app.config['CLASS_CODES']['actor']:
                    buttons = [button(_('add'), url_for('involvement_insert', origin_id=id_))]
                elif self.origin.class_.code in app.config['CLASS_CODES']['source']:
                    buttons = [button('add', url_for('source_add', id_=id_, class_name='event'))]
                for code in app.config['CLASS_CODES']['event']:
                    label = g.classes[code].name
                    buttons.append(button(label, url_for('event_insert', code=code, origin_id=id_)))

        elif name == 'relation':
            buttons = [button(_('add'), url_for('relation_insert', origin_id=id_))]
            for code in app.config['CLASS_CODES']['actor']:
                label = g.classes[code].name
                buttons.append(button(label, url_for('actor_insert', code=code, origin_id=id_)))

        elif name == 'member_of':
            buttons = [button(_('add'), url_for('membership_insert', origin_id=id_))]

        elif name == 'member':
            buttons = [button(_('add'), url_for('member_insert', origin_id=id_))]

        elif name == 'reference':
            buttons = [button(_('add'), url_for('entity_add_reference', id_=id_)),
                       button(_('bibliography'), url_for('reference_insert',
                                                         code='bibliography',
                                                         origin_id=id_)),
                       button(_('edition'), url_for('reference_insert',
                                                    code='edition',
                                                    origin_id=id_)),
                       button(_('external reference'), url_for('reference_insert',
                                                               code='external_reference',
                                                               origin_id=id_))]

        elif name == 'file':
            if self.origin.class_.code in app.config['CLASS_CODES']['reference']:
                buttons = [button(_('add'), url_for('reference_add', id_=id_, class_name='file'))]
            else:
                buttons = [button(_('add'), url_for('entity_add_file', id_=id_))]
            buttons.append(button(_('file'), url_for('file_insert', origin_id=id_)))

        elif name == 'entities':
            buttons = [button(_('move entities'), url_for('node_move_entities', id_=id_))]

        elif name == 'actor':
            if self.origin.system_type == 'file':
                buttons = [button('add', url_for('file_add', id_=id_, class_name='actor'))]
            elif self.origin.class_.code in app.config['CLASS_CODES']['reference']:
                buttons = [button(_('add'), url_for('reference_add', id_=id_, class_name='actor'))]
            elif self.origin.class_.code in app.config['CLASS_CODES']['source']:
                buttons = [button('add', url_for('source_add', id_=id_, class_name='actor'))]
            elif self.origin.class_.code in app.config['CLASS_CODES']['event']:
                buttons = [button(_('add'), url_for('involvement_insert', origin_id=id_))]
            for code in app.config['CLASS_CODES']['actor']:
                buttons.append(button(g.classes[code].name,
                                      url_for('actor_insert', code=code, origin_id=id_)))

        elif name == 'feature' and self.origin.system_type == 'place':
            buttons = [button(_('feature'), url_for('place_insert', origin_id=id_))]

        elif name == 'stratigraphic_unit' and self.origin.system_type == 'feature':
            buttons = [button(_('stratigraphic unit'), url_for('place_insert', origin_id=id_))]

        elif name == 'find' and self.origin.system_type == 'stratigraphic unit':
            buttons = [button(_('find'), url_for('place_insert', origin_id=id_))]

        elif name == 'human_remains' and self.origin.system_type == 'stratigraphic unit':
            buttons = [button(_('human remains'), url_for('place_insert',
                                                          origin_id=id_,
                                                          system_type='human_remains'))]

        elif name == 'place':
            if self.origin.system_type == 'file':
                buttons = [button(_('add'), url_for('file_add', id_=id_, class_name='place'))]
            elif self.origin.class_.code in app.config['CLASS_CODES']['reference']:
                buttons = [button(_('add'), url_for('reference_add', id_=id_, class_name='place'))]
            elif self.origin.class_.code in app.config['CLASS_CODES']['source']:
                buttons = [button(_('add'), url_for('source_add', id_=id_, class_name='place'))]
            buttons.append(button(_('place'), url_for('place_insert', origin_id=id_)))

        elif name == 'texts':
            buttons = [button(_('text'), url_for('translation_insert', source_id=id_))]
        return buttons
