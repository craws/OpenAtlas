from typing import List, Optional

from flask import g, url_for
from openatlas import app
from openatlas.models.entity import Entity
from openatlas.util.table import Table
from openatlas.util.util import button, is_authorized, uc_first
from flask_babel import lazy_gettext as _

# Needed for translations
_('member of')
_('texts')


class Tab:
    origin: Optional[Entity]
    buttons: Optional[List[str]]
    table: Table

    def __init__(self, name: str, origin: Optional[Entity] = None) -> None:
        self.name = name
        self.title = uc_first(_(name.replace('_', ' ')))
        self.origin = origin
        id_ = origin.id if origin else None
        system_type = origin.system_type if origin else None
        code = origin.class_.code if origin else None
        class_codes = app.config['CLASS_CODES']
        buttons: List[str] = []
        table = Table(Table.HEADERS[name]) if name in Table.HEADERS else Table()
        if name == 'reference' or (code in class_codes['reference'] and system_type != 'file'):
            table.header = table.header + ['page']

        if name == 'actor':
            table.defs = [{'className': 'dt-body-right', 'targets': [2, 3]}]
            if code in ['E18', 'E22', 'E20']:
                table.header = ['actor', _('property'), 'class', 'first', 'last', 'description']
                table.defs = [{'className': 'dt-body-right', 'targets': [3, 4]}]
            if system_type == 'file':
                buttons = [button('link', url_for('file_add', id_=id_, class_name='actor'))]
            elif code in class_codes['reference']:
                buttons = [button(_('link'), url_for('reference_add', id_=id_, class_name='actor'))]
            elif code in class_codes['source']:
                buttons = [button('link', url_for('source_add', id_=id_, class_name='actor'))]
            elif code in class_codes['event']:
                table.header = ['actor', 'class', 'involvement', 'first', 'last', 'description']
                table.defs = [{'className': 'dt-body-right', 'targets': [3, 4]}]
                buttons = [button(_('link'), url_for('involvement_insert', origin_id=id_))]
            for code in class_codes['actor']:
                buttons.append(button(g.classes[code].name,
                                      url_for('actor_insert', code=code, origin_id=id_)))
        elif name == 'entities':
            buttons = [button(_('move entities'), url_for('node_move_entities', id_=id_))]
        elif name == 'event':
            table.defs = [{'className': 'dt-body-right', 'targets': [3, 4]}]
            if code in class_codes['actor']:
                table.header = ['event', 'class', 'involvement', 'first', 'last', 'description']
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
                elif code in class_codes['reference']:
                    buttons = [button('link', url_for('reference_add', id_=id_, class_name='event'))]
                for code in class_codes['event']:
                    label = g.classes[code].name
                    buttons.append(button(label, url_for('event_insert', code=code, origin_id=id_)))
        elif name == 'feature':
            if system_type == 'place':
                buttons = [button(_('feature'), url_for('place_insert', origin_id=id_))]
        elif name == 'find':
            if system_type == 'stratigraphic unit':
                buttons = [button(_('find'), url_for('place_insert', origin_id=id_))]
        elif name == 'file':
            table.header = Table.HEADERS['file'] + [_('main image')]
            if code in class_codes['reference']:
                table.header = Table.HEADERS['file'] + [_('main image')]
                buttons = [button(_('link'), url_for('reference_add', id_=id_, class_name='file'))]
            else:
                buttons = [button(_('link'), url_for('entity_add_file', id_=id_))]
            buttons.append(button(_('file'), url_for('file_insert', origin_id=id_)))
        elif name == 'human_remains':
            if system_type == 'stratigraphic unit':
                buttons = [button(_('human remains'), url_for('place_insert',
                                                              origin_id=id_,
                                                              system_type='human_remains'))]
        elif name == 'member':
            table.defs = [{'className': 'dt-body-right', 'targets': [2, 3]}]
            buttons = [button(_('link'), url_for('member_insert', origin_id=id_))]
        elif name == 'member_of':
            table.defs = [{'className': 'dt-body-right', 'targets': [2, 3]}]
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
            table.defs = [{'className': 'dt-body-right', 'targets': [2, 3]}]
            buttons = [button(_('link'), url_for('relation_insert', origin_id=id_))]
            for code in class_codes['actor']:
                label = g.classes[code].name
                buttons.append(button(label, url_for('actor_insert', code=code, origin_id=id_)))
        elif name == 'source':
            if system_type == 'file':
                buttons = [button(_('link'), url_for('file_add', id_=id_, class_name='source'))]
            elif code in class_codes['reference']:
                buttons = [button(_('link'),
                                  url_for('reference_add', id_=id_, class_name='source'))]
            else:
                buttons = [button(_('link'), url_for('entity_add_source', id_=id_))]
            buttons.append(button(_('source'), url_for('source_insert', origin_id=id_)))
        elif name == 'subs':
            if code == 'E55':
                table.header = [_('name'), _('count'), _('info')]
            else:
                table.header = Table.HEADERS['event']
        elif name == 'stratigraphic_unit':
            if system_type == 'feature':
                buttons = [button(_('stratigraphic unit'), url_for('place_insert', origin_id=id_))]
        elif name == 'text':
            buttons = [button(_('text'), url_for('translation_insert', source_id=id_))]

        self.table = table
        if is_authorized('contributor'):
            self.buttons = buttons
