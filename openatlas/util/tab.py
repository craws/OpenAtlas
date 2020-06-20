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
        system_type = self.origin.system_type
        code = self.origin.class_.code
        class_codes = app.config['CLASS_CODES']
        buttons = []
        if name == 'actor':
            if system_type == 'file':
                buttons = [button('link', url_for('file_add', id_=id_, class_name='actor'))]
            elif code in class_codes['reference']:
                buttons = [button(_('link'), url_for('reference_add', id_=id_, class_name='actor'))]
            elif code in class_codes['source']:
                buttons = [button('link', url_for('source_add', id_=id_, class_name='actor'))]
            elif code in class_codes['event']:
                buttons = [button(_('link'), url_for('involvement_insert', origin_id=id_))]
            for code in class_codes['actor']:
                buttons.append(button(g.classes[code].name,
                                      url_for('actor_insert', code=code, origin_id=id_)))
        elif name == 'entities':
            buttons = [button(_('move entities'), url_for('node_move_entities', id_=id_))]
        elif name == 'event':
            if code == 'E84':
                buttons = [button(g.classes['E9'].name,
                                  url_for('event_insert', code='E9', origin_id=id_))]
            else:
                if system_type == 'file':
                    buttons = [button('link', url_for('file_add', id_=id_, class_name='event'))]
                elif code in class_codes['actor']:
                    buttons = [button(_('link'), url_for('involvement_insert', origin_id=id_))]
                elif code in class_codes['source']:
                    buttons = [button('link', url_for('source_add', id_=id_, class_name='event'))]
                for code in class_codes['event']:
                    label = g.classes[code].name
                    buttons.append(button(label, url_for('event_insert', code=code, origin_id=id_)))
        elif name == 'feature' and system_type == 'place':
            buttons = [button(_('feature'), url_for('place_insert', origin_id=id_))]
        elif name == 'find' and system_type == 'stratigraphic unit':
            buttons = [button(_('find'), url_for('place_insert', origin_id=id_))]
        elif name == 'file':
            if code in class_codes['reference']:
                buttons = [button(_('link'), url_for('reference_add', id_=id_, class_name='file'))]
            else:
                buttons = [button(_('link'), url_for('entity_add_file', id_=id_))]
            buttons.append(button(_('file'), url_for('file_insert', origin_id=id_)))
        elif name == 'human_remains' and system_type == 'stratigraphic unit':
            buttons = [button(_('human remains'), url_for('place_insert',
                                                          origin_id=id_,
                                                          system_type='human_remains'))]
        elif name == 'member':
            buttons = [button(_('link'), url_for('member_insert', origin_id=id_))]
        elif name == 'member_of':
            buttons = [button(_('link'), url_for('membership_insert', origin_id=id_))]
        elif name == 'place':
            if system_type == 'file':
                buttons = [button(_('link'), url_for('file_add', id_=id_, class_name='place'))]
            elif code in class_codes['reference']:
                buttons = [button(_('link'), url_for('reference_add', id_=id_, class_name='place'))]
            elif code in class_codes['source']:
                buttons = [button(_('link'), url_for('source_add', id_=id_, class_name='place'))]
            buttons.append(button(_('place'), url_for('place_insert', origin_id=id_)))
        elif name == 'reference':
            buttons = [button(_('link'), url_for('entity_add_reference', id_=id_)),
                       button(_('bibliography'), url_for('reference_insert',
                                                         code='bibliography',
                                                         origin_id=id_)),
                       button(_('edition'), url_for('reference_insert',
                                                    code='edition',
                                                    origin_id=id_)),
                       button(_('external reference'), url_for('reference_insert',
                                                               code='external_reference',
                                                               origin_id=id_))]
        elif name == 'relation':
            buttons = [button(_('link'), url_for('relation_insert', origin_id=id_))]
            for code in class_codes['actor']:
                label = g.classes[code].name
                buttons.append(button(label, url_for('actor_insert', code=code, origin_id=id_)))
        elif name == 'source':
            if system_type == 'file':
                buttons = [button(_('link'), url_for('file_add', id_=id_, class_name='source'))]
            elif code in class_codes['reference']:
                buttons = [button(_('link'), url_for('reference_add', id_=id_, class_name='source'))]
            else:
                buttons = [button(_('link'), url_for('entity_add_source', id_=id_))]
            buttons.append(button(_('source'), url_for('source_insert', origin_id=id_)))
        elif name == 'stratigraphic_unit' and system_type == 'feature':
            buttons = [button(_('stratigraphic unit'), url_for('place_insert', origin_id=id_))]
        elif name == 'texts':
            buttons = [button(_('text'), url_for('translation_insert', source_id=id_))]
        return buttons
