from typing import List, Optional

from flask import g, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.util.display import button, uc_first
from openatlas.util.table import Table
from openatlas.util.util import is_authorized

# Needed for translations of tab titles
_('member of')
_('texts')
_('invalid dates')
_('invalid link dates')
_('invalid involvement dates')
_('unlinked')
_('missing files')
_('orphaned files')
_('circular dependencies')

# Needed for translations of content items
_('intro_for_frontend')
_('legal_notice_for_frontend')
_('contact_for_frontend')


def tab_header(id_: str, table: Optional[Table] = None, active: Optional[bool] = False) -> str:
    label = uc_first(_(id_.replace('_', ' ').replace('-', ' ')))
    label += ' <span class="tab-counter">{counter}</span>'.format(
        counter=format_number(len(table.rows))) if table and len(table.rows) else ''
    return '''
        <li class="nav-item">
            <a 
                class="nav-link {active}" 
                data-toggle="tab" 
                role="tab" 
                aria-selected="{selected}" 
                href="#tab-{id}">{label}
            </a>
        </li>'''.format(active=' active' if active else '',
                        selected='true' if active else 'false',
                        label=label,
                        id=id_.replace('_', '-').replace(' ', '-'))


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
                                      url_for('insert', class_=code, origin_id=id_)))
        elif name == 'entities':
            buttons = [button(_('move entities'), url_for('node_move_entities', id_=id_))]
        elif name == 'event':
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
                    buttons = [button('link',
                                      url_for('reference_add', id_=id_, class_name='event'))]
                for code in class_codes['event']:
                    label = g.classes[code].name
                    buttons.append(button(label, url_for('insert', class_=code, origin_id=id_)))
        elif name == 'feature':
            if current_user.settings['module_sub_units'] and system_type == 'place':
                buttons = [button(_('feature'), url_for('insert', class_='feature', origin_id=id_))]
        elif name == 'find':
            if current_user.settings['module_sub_units'] and system_type == 'stratigraphic unit':
                buttons = [button(_('find'), url_for('insert', class_='find', origin_id=id_))]
        elif name == 'file':
            table.header = Table.HEADERS['file'] + [_('main image')]
            if code in class_codes['reference']:
                table.header = Table.HEADERS['file'] + [_('main image')]
                buttons = [button(_('link'), url_for('reference_add', id_=id_, class_name='file'))]
            else:
                buttons = [button(_('link'), url_for('entity_add_file', id_=id_))]
            buttons.append(button(_('file'), url_for('insert', class_='file', origin_id=id_)))
        elif name == 'human_remains':
            if current_user.settings['module_sub_units'] and system_type == 'stratigraphic unit':
                buttons = [button(_('human remains'), url_for('insert',
                                                              origin_id=id_,
                                                              class_='human_remains'))]
        elif name == 'member':
            buttons = [button(_('link'), url_for('member_insert', origin_id=id_))]
        elif name == 'member_of':
            buttons = [button(_('link'),
                              url_for('member_insert', origin_id=id_, code='membership'))]
        elif name == 'place':
            if system_type == 'file':
                buttons = [button(_('link'), url_for('file_add', id_=id_, class_name='place'))]
            elif code in class_codes['reference']:
                buttons = [button(_('link'), url_for('reference_add', id_=id_, class_name='place'))]
            elif code in class_codes['source']:
                buttons = [button(_('link'), url_for('source_add', id_=id_, class_name='place'))]
            buttons.append(button(_('place'), url_for('insert', class_='place', origin_id=id_)))
        elif name == 'reference':
            buttons = [button(_('link'), url_for('entity_add_reference', id_=id_))]
            for category in ['bibliography', 'edition', 'external reference']:
                buttons.append(button(_(category), url_for('reference_insert',
                                                           category=category,
                                                           origin_id=id_)))
        elif name == 'relation':
            buttons = [button(_('link'), url_for('relation_insert', origin_id=id_))]
            for code in class_codes['actor']:
                label = g.classes[code].name
                buttons.append(button(label, url_for('insert', class_=code, origin_id=id_)))
        elif name == 'source':
            if system_type == 'file':
                buttons = [button(_('link'), url_for('file_add', id_=id_, class_name='source'))]
            elif code in class_codes['reference']:
                buttons = [button(_('link'),
                                  url_for('reference_add', id_=id_, class_name='source'))]
            else:
                buttons = [button(_('link'), url_for('entity_add_source', id_=id_))]
            buttons.append(button(_('source'), url_for('insert', class_='source', origin_id=id_)))
        elif name == 'subs':
            if code in ['E53', 'E55']:
                table.header = [_('name'), _('count'), _('info')]
            else:
                table.header = Table.HEADERS['event']
        elif name == 'stratigraphic_unit':
            if current_user.settings['module_sub_units'] and system_type == 'feature':
                buttons = [button(_('stratigraphic unit'), url_for('insert',
                                                                   class_='stratigraphic_unit',
                                                                   origin_id=id_))]
        elif name == 'text':
            buttons = [button(_('text'), url_for('translation_insert', source_id=id_))]

        self.table = table
        if is_authorized('contributor'):
            self.buttons = buttons
