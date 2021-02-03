import pathlib
import re
from typing import Any, Dict, List, Optional, Union

import flask
import jinja2
from flask import g, request, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from jinja2 import escape
from markupsafe import Markup
from wtforms import Field, IntegerField
from wtforms.validators import Email

from openatlas import app
from openatlas.models.content import Content
from openatlas.models.entity import Entity
from openatlas.models.imports import Project
from openatlas.models.model import CidocClass, CidocProperty
from openatlas.models.node import Node
from openatlas.models.user import User
from openatlas.util import display, tab, util
from openatlas.util.table import Table

blueprint: flask.Blueprint = flask.Blueprint('filters', __name__)
paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@jinja2.contextfilter
@blueprint.app_template_filter()
def link(self: Any, entity: Entity) -> str:
    return display.link(entity)


@jinja2.contextfilter
@blueprint.app_template_filter()
def button(self: Any,
           label: str,
           url: Optional[str] = '#',
           css: Optional[str] = 'primary',
           id_: Optional[str] = None,
           onclick: Optional[str] = '') -> str:
    return display.button(label, url, css, id_, onclick)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_citation_example(self: Any, code: str) -> str:
    example = Content.get_translation('citation_example')
    if not example or code not in ['edition', 'bibliography']:
        return ''
    return Markup('<h1>' + display.uc_first(_('citation_example')) + '</h1>' + example)


@jinja2.contextfilter
@blueprint.app_template_filter()
def siblings_pager(self: Any, entity: Entity, structure: Optional[Dict[str, Any]]) -> str:
    if entity.view_name != 'place' or not structure or len(structure['siblings']) < 2:
        return ''
    structure['siblings'].sort(key=lambda x: x.id)
    prev_id = None
    next_id = None
    position = None
    for counter, sibling in enumerate(structure['siblings']):
        position = counter + 1
        prev_id = sibling.id if sibling.id < entity.id else prev_id
        if sibling.id > entity.id:
            next_id = sibling.id
            position = counter
            break
    return Markup('{previous} {next} {position} {of_label} {count}'.format(
        previous=display.button('<', url_for('entity_view', id_=prev_id)) if prev_id else '',
        next=display.button('>', url_for('entity_view', id_=next_id)) if next_id else '',
        position=position,
        of_label=_('of'),
        count=len(structure['siblings'])))


@jinja2.contextfilter
@blueprint.app_template_filter()
def crumb(self: Any, crumbs: List[Any]) -> str:
    items = []
    for item in crumbs:
        if not item:
            continue  # Item can be None e.g. if a dynamic generated URL has no origin parameter
        elif isinstance(item, Entity) or isinstance(item, Project) or isinstance(item, User):
            items.append(display.link(item))
        elif isinstance(item, list):
            items.append('<a href="{url}">{label}</a>'.format(
                # If there are more than 2 arguments pass them as parameters with **
                url=url_for(item[1]) if len(item) == 2 else url_for(item[1], **item[2]),
                label=display.truncate(display.uc_first(str(item[0])))))
        else:
            items.append(display.uc_first(item))
    return Markup('&nbsp;>&nbsp; '.join(items))


@jinja2.contextfilter
@blueprint.app_template_filter()
def lay_breadcrumbs(self: Any, crumbs: List[Any]) -> str:
    items = []
    for item in crumbs:
        if not item:
            continue  # Item can be None e.g. if a dynamic generated URL has no origin parameter
        elif isinstance(item, Entity) or isinstance(item, Project) or isinstance(item, User):
            items.append(display.link(item))
        elif isinstance(item, list):
            items.append('<a href="{url}">{label}</a>'.format(
                url=item[1],
                label=display.truncate(display.uc_first(str(item[0])))))
        else:
            items.append(display.uc_first(item))
    return Markup('&nbsp;>&nbsp; '.join(items))


@jinja2.contextfilter
@blueprint.app_template_filter()
def note(self: Any, entity: Entity) -> str:
    if not current_user.settings['module_notes'] or not util.is_authorized('contributor'):
        return ''  # pragma no cover
    if not isinstance(entity.note, str):
        html = '<div class="toolbar">{insert}</div>'.format(
            insert=display.button(_('add note'), url_for('note_insert', entity_id=entity.id)))
    else:
        html = '''
            <h2>{label}</h2>
            <div class="note">{note}</div>
            <div class="toolbar">{edit} {delete}</div>'''.format(
            label=display.uc_first(_('note')),
            note=entity.note.replace('\r\n', '<br>'),
            edit=display.button(_('edit note'), url_for('note_update', entity_id=entity.id)),
            delete=display.button(_('delete'),
                                  url_for('note_delete', entity_id=entity.id),
                                  onclick="return confirm('" + _('Delete note?') + "');"))
    return Markup(html)


@jinja2.contextfilter
@blueprint.app_template_filter()
def is_authorized(self: Any, group: str) -> bool:
    return util.is_authorized(group)


@jinja2.contextfilter
@blueprint.app_template_filter()
def tab_header(self: Any,
               item: str,
               table: Optional[Table] = None,
               active: Optional[bool] = False) -> str:
    return Markup(tab.tab_header(item, table, active))


@jinja2.contextfilter
@blueprint.app_template_filter()
def uc_first(self: Any, string: str) -> str:
    return display.uc_first(string)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_info(self: Any, data: Dict[str, Union[str, List[str]]]) -> str:
    html = '<div class="data-table">'
    for label, value in data.items():
        if value or value == 0:
            if isinstance(value, list):
                value = '<br>'.join(value)
            html += '''
                <div class="table-row">
                    <div>{label}</div>
                    <div class="table-cell">{value}</div>
                </div>'''.format(label=display.uc_first(label), value=value)
    return Markup(html + '</div>')


@jinja2.contextfilter
@blueprint.app_template_filter()
def bookmark_toggle(self: Any, entity_id: int) -> str:
    return Markup(display.bookmark_toggle(entity_id))


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_move_form(self: Any, form: Any, root_name: str) -> str:
    from openatlas.forms.field import TreeField
    html = ''
    for field in form:
        if type(field) is TreeField:
            html += '<p>' + root_name + ' ' + str(field) + '</p>'
    table = Table(header=['#', display.uc_first(_('selection'))],
                  rows=[[item, item.label.text] for item in form.selection])
    return html + """
        <div class="toolbar">
            {select_all}
            {deselect_all}
        </div>
        {table}""".format(select_all=display.button(_('select all'), id_="select-all"),
                          deselect_all=display.button(_('deselect all'), id_="select-none"),
                          table=table.display('move'))


@jinja2.contextfilter
@blueprint.app_template_filter()
def table_select_model(self: Any,
                       name: str,
                       selected: Union[CidocClass, CidocProperty, None] = None) -> str:
    if name in ['domain', 'range']:
        entities = g.classes
    else:
        entities = g.properties
    table = Table(['code', 'name'], defs=[{'orderDataType': 'cidoc-model', 'targets': [0]},
                                          {'sType': 'numeric', 'targets': [0]}])

    for id_ in entities:
        table.rows.append([
            """<a
                    onclick="selectFromTable(this, '{name}', '{entity_id}', '{value}')"
                    href="#">{label}</a>""".format(
                name=name,
                entity_id=id_,
                value=entities[id_].code + ' ' + entities[id_].name,
                label=entities[id_].code),
            """<a
                    onclick="selectFromTable(this, '{name}', '{entity_id}', '{value}')"
                    href="#">{label}</a>""".format(
                name=name,
                entity_id=id_,
                value=entities[id_].code + ' ' + entities[id_].name,
                label=entities[id_].name)])
    value = selected.code + ' ' + selected.name if selected else ''
    html = """
        <input id="{name}-button" name="{name}-button" class="table-select" type="text"
            onfocus="this.blur()" readonly="readonly" value="{value}"
            onclick="$('#{name}-modal').modal('show')">
            <div id="{name}-modal" class="modal fade" tabindex="-1" role="dialog"
                aria-hidden="true">
                <div class="modal-dialog" role="document" style="max-width: 100%!important;">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{name}</h5>
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">{table}</div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-outline-primary btn-sm"
                                data-dismiss="modal">{close_label}</button>
                        </div>
                    </div>
                </div>
            </div>""".format(name=name,
                             value=value,
                             close_label=display.uc_first(_('close')),
                             table=table.display(name))
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def get_class_name(self: Any, code: str) -> str:
    return g.classes[code].name


@jinja2.contextfilter
@blueprint.app_template_filter()
def description(self: Any, entity: Entity) -> str:
    if not entity.description:
        return ''
    label = display.uc_first(_('description'))
    if hasattr(entity, 'system_type') and entity.system_type == 'source content':
        label = display.uc_first(_('content'))
    return Markup("""<h2>{label}</h2><div class="description more">{description}</div>""".format(
        label=label,
        description=entity.description.replace('\r\n', '<br>')))


@jinja2.contextfilter
@blueprint.app_template_filter()
def download_button(self: Any, entity: Entity) -> str:
    if entity.view_name != 'file':
        return ''
    html = '<span class="error">{msg}</span>'.format(msg=display.uc_first(_('missing file')))
    if entity.image_id:
        path = display.get_file_path(entity.image_id)
        html = display.button(_('download'), url_for('download_file', filename=path.name))
    return Markup(html)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_profile_image(self: Any, entity: Entity) -> str:
    if not entity.image_id:
        return ''
    path = display.get_file_path(entity.image_id)
    if not path:
        return ''
    if entity.view_name == 'file':
        if path.suffix.lower() in app.config['DISPLAY_FILE_EXTENSIONS']:
            html = '''
                <a href="{url}" rel="noopener noreferrer" target="_blank">
                    <img style="max-width:{width}px;" alt="image" src="{url}">
                </a>'''.format(url=url_for('display_file', filename=path.name),
                               width=session['settings']['profile_image_width'])
        else:
            html = display.uc_first(_('no preview available'))
    else:
        html = """
            <a href="{url}">
                <img style="max-width:{width}px;" alt="image" src="{src}">
            </a>""".format(url=url_for('entity_view', id_=entity.image_id),
                           src=url_for('display_file', filename=path.name),
                           width=session['settings']['profile_image_width'])
    return Markup('<div id="profile_image_div">{html}</div>'.format(html=html))


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_content_translation(self: Any, text: str) -> str:
    from openatlas.models.content import Content
    return Content.get_translation(text)


@jinja2.contextfilter
@blueprint.app_template_filter()
def manual(self: Any, site: str) -> str:  # Creates a link to a manual page
    return Markup("""
        <a class="manual" href="/static/manual/{site}.html" target="_blank" title="{label}">
            <i class="fas fa-book"></i></a>""".format(site=site, label=display.uc_first('manual')))


def add_row(field: Field,
            label: Optional[str] = None,
            value: Optional[str] = None,
            form_id: Optional[str] = None) -> str:
    field.label.text = display.uc_first(field.label.text)
    if field.flags.required and form_id != 'login-form' and field.label.text:
        field.label.text += ' *'

    # CSS
    css_class = 'required' if field.flags.required else ''
    css_class += ' integer' if type(field) is IntegerField else ''
    for validator in field.validators:
        css_class += ' email' if type(validator) is Email else ''
    errors = ' <span class="error">{errors}</span>'.format(
        errors=' '.join(display.uc_first(error) for error in field.errors)) if field.errors else ''
    return """
        <div class="table-row {css_row}">
            <div>{label} {tooltip}</div>
            <div class="table-cell">{value} {errors}</div>
        </div>""".format(
        label=label if isinstance(label, str) else field.label,
        tooltip=display.tooltip(field.description),
        value=value if value else field(class_=css_class).replace('> ', '>'),
        css_row='external-reference' if field.id.startswith('reference_system_') else '',
        errors=errors)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_form(self: Any,
                 form: Any,
                 form_id: Optional[str] = None,
                 for_persons: bool = False,
                 manual_page: Optional[str] = None) -> str:
    from openatlas.forms.field import ValueFloatField

    def display_value_type_fields(node_: Node, root: Optional[Node] = None) -> str:
        root = root if root else node_
        html_ = ''
        for sub_id in node_.subs:
            sub = g.nodes[sub_id]
            field_ = getattr(form, str(sub_id))
            html_ += """
                <div class="table-row value-type-switch{id}">
                    <div>{label}</div>
                    <div class="table-cell">{field} {unit}</div>
                </div>
                {value_fields}""".format(id=root.id,
                                         label=sub.name,
                                         unit=sub.description,
                                         field=field_(class_='value-type'),
                                         value_fields=display_value_type_fields(sub, root))
        return html_

    html = ''
    for field in form:

        # These fields will be added in combination with other fields
        if type(field) is ValueFloatField or field.id.startswith('insert_'):
            continue
        if field.id.startswith('reference_system_precision'):
            continue

        if field.type in ['CSRFTokenField', 'HiddenField']:
            html += str(field)
            continue
        if field.id.split('_', 1)[0] in ('begin', 'end'):  # If it's a date field use a function
            if field.id == 'begin_year_from':
                html += display.add_dates_to_form(form, for_persons)
            continue

        if field.type in ['TreeField', 'TreeMultiField']:
            hierarchy_id = int(field.id)
            node = g.nodes[hierarchy_id]
            label = node.name
            if node.name in app.config['BASE_TYPES']:
                label = display.uc_first(_('type'))
            if field.label.text == 'super':
                label = display.uc_first(_('super'))
            if node.value_type and 'is_node_form' not in form:
                field.description = node.description
                onclick = 'switch_value_type({id})'.format(id=node.id)
                html += add_row(field, label, display.button(_('show'),
                                                             onclick=onclick,
                                                             css='secondary'))
                html += display_value_type_fields(node)
                continue
            tooltip = '' if 'is_node_form' in form else ' ' + display.tooltip(node.description)
            html += add_row(field, label + tooltip)
            continue

        if field.id == 'save':
            field.label.text = display.uc_first(field.label.text)
            class_ = app.config['CSS']['button']['primary']
            buttons = []
            if manual_page:
                buttons.append(escape(manual(None, manual_page)))
            buttons.append(field(class_=class_))
            if 'insert_and_continue' in form:
                buttons.append(form.insert_and_continue(class_=class_))
            if 'insert_continue_sub' in form:
                buttons.append(form.insert_continue_sub(class_=class_))
            if 'insert_continue_human_remains' in form:
                buttons.append(form.insert_continue_human_remains(class_=class_))
            text = '<div class ="toolbar">{buttons}</div>'.format(buttons=' '.join(buttons))
            html += add_row(field, '', text)
            continue

        # External reference system
        if field.id.startswith('reference_system_id_'):
            precision_field = getattr(form, field.id.replace('id_', 'precision_'))
            html += add_row(field, field.label, ' '.join([str(field(class_=field.label.text)),
                                                          str(precision_field.label),
                                                          str(precision_field)]))
            continue
        html += add_row(field, form_id=form_id)

    return Markup("""
        <form method="post" {id} {multi}>
            <div class="data-table">{html}</div>
        </form>""".format(id=('id="' + form_id + '" ') if form_id else '',
                          html=html,
                          multi='enctype="multipart/form-data"' if hasattr(form, 'file') else ''))


@jinja2.contextfilter
@blueprint.app_template_filter()
def test_file(self: Any, file_name: str) -> Optional[str]:
    return file_name if (pathlib.Path(app.root_path) / file_name).is_file() else None


@jinja2.contextfilter
@blueprint.app_template_filter()
def sanitize(self: Any, string: str) -> str:
    return display.sanitize(string)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_delete_link(self: Any, entity: Entity) -> str:
    """ Build a link to delete an entity with a JavaScript confirmation dialog."""
    name = entity.name.replace('\'', '')
    url = url_for('index', class_=entity.view_name, delete_id=entity.id)
    if entity.system_type == 'source translation':
        url = url_for('translation_delete', id_=entity.id)
    return display.button(_('delete'),
                          url,
                          onclick="return confirm('" + _('Delete %(name)s?', name=name) + "')")


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_menu(self: Any, entity: Optional[Entity], origin: Optional[Entity]) -> str:
    """ Returns HTML with the menu and mark appropriate item as selected."""
    html = ''
    if current_user.is_authenticated:
        view_name = ''
        if entity:
            view_name = entity.view_name
        if origin:
            view_name = origin.view_name
        for item in ['source', 'event', 'actor', 'place', 'reference', 'object']:
            if view_name:
                css = 'active' if view_name.replace('node', 'types') == item else ''
            else:
                css = 'active' if request.path.startswith('/' + item) else ''
            html += '<a href="/index/{item}" class="nav-item nav-link {css}">{label}</a>'.format(
                css=css, item=item, label=display.uc_first(_(item)))
        html += '<a href="/types" class="nav-item nav-link">{label}</a>'.format(
                label=display.uc_first(_('types')))
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_debug_info(self: Any, debug_model: Dict[str, Any], form: Any) -> str:
    """ Returns HTML with debug information about database queries and form errors."""
    html = ''
    for name, value in debug_model.items():
        if name in ['current']:
            continue  # Don't display current time counter
        if name not in ['sql']:
            value = '{:10.2f}'.format(value)
        html += """
            <div>
                <div>{name}</div>
                <div class="table-cell" style="text-align:right;">
                    {value}
                </div>
            </div>""".format(name=name, value=value)
    if form and hasattr(form, 'errors'):
        for fieldName, errorMessages in form.errors.items():
            html += fieldName + ' - ' + errorMessages[0] + '<br>'
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_external_references(self: Any, entity: Entity) -> str:
    system_links = []
    for link_ in entity.reference_systems:
        system = g.reference_systems[link_.domain.id]
        name = link_.description
        if system.resolver_url:
            name = '<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>'.format(
                url=system.resolver_url + name,
                name=name)
        system_links.append('''{name} ({match} {at} {system_name})'''.format(
            name=name,
            match= g.nodes[link_.type.id].name,
            at=_('at'),
            system_name= display.link(link_.domain)))
    html = '<br>'.join(system_links)
    if not html:
        return ''
    return Markup('<h2>' + display.uc_first(_('external reference systems')) + '</h2>' + html)
