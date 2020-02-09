import os
import re
from typing import Any, Dict, List, Optional, Union

import flask
import jinja2
from flask import g, request, session, url_for
from flask_babel import format_number as babel_format_number, lazy_gettext as _
from flask_login import current_user
from jinja2 import escape, evalcontextfilter
from wtforms import IntegerField
from wtforms.validators import Email

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.imports import Project
from openatlas.models.model import CidocClass, CidocProperty
from openatlas.util import util
from openatlas.util.table import Table
from openatlas.util.util import get_file_path, print_file_extension

blueprint: flask.Blueprint = flask.Blueprint('filters', __name__)
paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@jinja2.contextfilter
@blueprint.app_template_filter()
def link(self: Any, entity: Entity) -> str:
    return util.link(entity)


@jinja2.contextfilter
@blueprint.app_template_filter()
def crumb(self: Any, crumbs: List[Any]) -> str:
    items = []
    for item in crumbs:
        if not item:
            continue
        elif isinstance(item, list):
            items.append('<a href="{url}">{label}</a>'.format(
                url=url_for(item[1]) if len(item) == 2 else url_for(item[1], **item[2]),
                label=util.truncate(util.uc_first(str(item[0])))))
        elif isinstance(item, Entity) or isinstance(item, Project):
            items.append(util.link(item))
        else:
            items.append(util.truncate(util.uc_first(item)))
    return ' > '.join(items)


@jinja2.contextfilter
@blueprint.app_template_filter()
def note(self: Any, entity: Entity) -> str:
    if not current_user.settings['module_notes'] or not util.is_authorized('contributor'):
        return ''  # pragma no cover
    if not entity.note:
        return '<p><a href="{url}">{label}</a></p>'.format(
            url=url_for('note_insert', entity_id=entity.id),
            label=util.uc_first(_('note')))
    return '<h2>{label}</h2><p>{note}</p><a href="{url}">{edit}</a>'.format(
        label=util.uc_first(_('note')),
        note=entity.note,
        url=url_for('note_update', entity_id=entity.id),
        edit=util.uc_first(_('edit note')))


@jinja2.contextfilter
@blueprint.app_template_filter()
def format_tab_number(self: Any, param: Union[int, Table]) -> str:
    length = len(param.rows) if isinstance(param, Table) else param
    return '<span class="tab-counter">' + babel_format_number(length) + '</span>'


@jinja2.contextfilter
@blueprint.app_template_filter()
def is_authorized(self: Any, group: str) -> bool:
    return util.is_authorized(group)


@jinja2.contextfilter
@blueprint.app_template_filter()
def uc_first(self: Any, string: str) -> str:
    return util.uc_first(string)


@jinja2.contextfilter
@evalcontextfilter
@blueprint.app_template_filter()
def nl2br(self: Any, value: str) -> str:
    result = u'\n\n'.join(
        u'<p>%s</p>' % p.replace('\n', '<br>\n') for p in paragraph_re.split(escape(value)))
    return result


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_info(self: Any, data: Dict[str, str]) -> str:
    html = '<div class="data-table">'
    for key, value in data:
        if value or value == 0:
            value = util.uc_first(_('no')) if value is False else value
            value = util.uc_first(_('yes')) if value is True else value
            html += '''
                <div class="table-row">
                    <div>{key}</div>
                    <div class="table-cell">{value}</div>
                </div>'''.format(key=util.uc_first(key), value=value)
    return html + '</div>'


@jinja2.contextfilter
@blueprint.app_template_filter()
def bookmark_toggle(self: Any, entity_id: int) -> str:
    return util.bookmark_toggle(entity_id)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_move_form(self: Any, form: Any, root_name: str) -> str:
    from openatlas.forms.forms import TreeField
    html = ''
    for field in form:
        if type(field) is TreeField:
            html += '<p>' + root_name + ' ' + str(field) + '</p>'
    table = Table(header=['#', util.uc_first(_('selection'))],
                  rows=[[item, item.label.text] for item in form.selection])
    return html + """
        <p>
            <a class="button" id="select-all">{select_all}</a>
            <a class="button" id="select-none">{deselect_all}</a>
        </p>
        {table}""".format(select_all=util.uc_first(_('select all')),
                          deselect_all=util.uc_first(_('deselect all')),
                          table=table.display('move'))


@jinja2.contextfilter
@blueprint.app_template_filter()
def table_select_model(self: Any, name: str,
                       selected: Union[CidocClass, CidocProperty, None] = None) -> str:
    if name in ['domain', 'range']:
        entities = g.classes
    else:
        entities = g.properties
    table = Table(['code', 'name'], defs=[{'orderDataType': 'cidoc-model', 'targets': [0]},
                                          {'sType': 'numeric', 'targets': [0]}])
    for id_ in entities:
        table.rows.append([
            '<a onclick="selectFromTable(this, \'' + name + '\', \'' + str(id_) + '\')">' +
            entities[id_].code + '</a>',
            '<a onclick="selectFromTable(this, \'' + name + '\', \'' + str(id_) + '\')">' +
            entities[id_].name + '</a>'])
    value = selected.code + ' ' + selected.name if selected else ''
    html = """
        <input id="{name}-button" value="{value}" class="table-select" type="text"
            onfocus="this.blur()" readonly="readonly">
        <div id="{name}-overlay" class="overlay">
            <div id="{name}-dialog" class="overlay-container">
                {table}
            </div>
        </div>
        <script>$(document).ready(function () {{createOverlay("{name}");}});</script>
    """.format(name=name, value=value, table=table.display(name))
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
    text = entity.description.replace('\r\n', '<br>')
    label = util.uc_first(_('description'))
    if hasattr(entity, 'system_type') and entity.system_type == 'source content':
        label = util.uc_first(_('content'))
    html = """<h2>{label}</h2>
        <div class="description more">{description}</div>""".format(label=label, description=text)
    return html


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_profile_image(self: Any, image_id: int) -> str:
    if not image_id:
        return ''
    file_path = get_file_path(image_id)
    if file_path:
        return """
            <div id="profile_image_div">
                <a href="/entity/{id}">
                    <img style="max-width:{width}px;" alt="profile image" src="{src}">
                </a>
            </div>
            """.format(id=image_id,
                       src=url_for('display_file', filename=os.path.basename(file_path)),
                       width=session['settings']['profile_image_width'])
    return ''  # pragma no cover


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_content_translation(self: Any, text: str) -> str:
    from openatlas.models.content import Content
    return Content.get_translation(text)


@jinja2.contextfilter
@blueprint.app_template_filter()
def manual_link(self: Any, wiki_site: str) -> str:
    # Creates a link to a manual page
    return """
        <p class="manual">
            <a class="manual" href="{url}" rel="noopener" target="_blank">
                <img style="height:14px;" src="/static/images/icons/book.png" alt=''> {label}
            </a>
        </p>
        """.format(url='https://redmine.openatlas.eu/projects/uni/wiki/' + wiki_site,
                   label=util.uc_first(_('manual')))


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_logo(self: Any, file_id: str) -> str:
    src = '/static/images/layout/logo.png'
    if file_id:
        extension = print_file_extension(int(file_id))
        if extension != 'N/A':
            src = url_for('display_logo', filename=file_id + extension)
    return '<img src="{src}" alt="Logo">'.format(src=src)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_form(self: Any,
                 form: Any,
                 form_id: Optional[str] = None,
                 for_persons: bool = False) -> str:
    from openatlas.forms.forms import ValueFloatField
    multipart = 'enctype="multipart/form-data"' if hasattr(form, 'file') else ''
    if 'update' in request.path:
        if hasattr(form, 'save') and hasattr(form.save, 'label'):
            form.save.label.text = _('save')
        if hasattr(form, 'insert_and_continue'):
            del form.insert_and_continue
    id_attribute = ' id="' + form_id + '" ' if form_id else ''
    html = {'main': '', 'types': '', 'value_types': '', 'header': '', 'footer': ''}

    def display_value_type_fields(subs: List[int], html_: str = '') -> str:
        for sub_id in subs:
            sub = g.nodes[sub_id]
            field_ = getattr(form, str(sub_id))
            html_ += """
                <div class="table-row value-type-switch">
                    <div><label>{label}</label></div>
                    <div class="table-cell">{field} {unit}</div>
                </div>
                {value_fields}""".format(label=sub.name,
                                         unit=sub.description,
                                         field=field_(class_='value-type'),
                                         value_fields=display_value_type_fields(sub.subs))
        return html_

    for field in form:
        if type(field) is ValueFloatField:
            continue
        class_ = 'required' if field.flags.required else ''
        class_ += ' integer' if type(field) is IntegerField else ''
        for validator in field.validators:
            class_ += ' email' if type(validator) is Email else ''
        errors = ''
        for error in field.errors:
            errors += util.uc_first(error)
        if field.type in ['TreeField', 'TreeMultiField']:
            hierarchy_id = int(field.id)
            node = g.nodes[hierarchy_id]
            label = node.name
            if node.name in app.config['BASE_TYPES']:
                label = util.uc_first(_('type'))
            if field.label.text == 'super':
                label = util.uc_first(_('super'))
            if node.value_type and 'is_node_form' not in form:
                html['value_types'] += """
                    <div class="table-row value-type-switch">
                        <div></div>
                        <div class="table-cell">
                            <label style="font-weight:bold;">{label}</label> {tooltip}
                        </div>
                    </div>
                    {value_fields}""".format(label=label,
                                             tooltip=util.display_tooltip(node.description),
                                             value_fields=display_value_type_fields(node.subs))
                continue
            else:
                info = '' if 'is_node_form' in form else util.display_tooltip(node.description)
                type_field = """
                    <div class="table-row">
                        <div><label>{label}</label> {info}</div>
                        <div class="table-cell">{field}</div>
                    </div>
                """.format(label=label, field=str(field(class_=class_)) + errors, info=info)
                if node.name in app.config['BASE_TYPES']:  # base type should be above other fields
                    html['types'] = type_field + html['types']
                else:
                    html['types'] += type_field
                continue
        if field.type in ['CSRFTokenField', 'HiddenField']:
            html['header'] += str(field)
            continue
        field.label.text = util.uc_first(field.label.text)
        field.label.text += ' *' if field.flags.required and form_id != 'login-form' else ''
        if field.id == 'description':
            html['footer'] += '<br>{label}<br>{text}<br>'.format(label=field.label,
                                                                 text=field(class_=class_))
            continue
        if field.type == 'SubmitField':
            html['footer'] += str(field)
            continue
        if field.id.split('_', 1)[0] in ('begin', 'end'):  # If it's a date field use a function
            if field.id == 'begin_year_from':
                html['footer'] += util.add_dates_to_form(form, for_persons)
            continue
        field.label.text += util.display_tooltip(field.description)
        errors = ' <span class="error">' + errors + ' </span>' if errors else ''
        if field.id in ('file', 'name'):
            html['header'] += '''
                <div class="table-row">
                    <div>{label}</div>
                    <div class="table-cell">{field} {errors}</div>
                </div>'''.format(label=field.label, errors=errors, field=field(class_=class_))
            continue
        if field.id == 'geonames_id':
            precision_field = getattr(form, 'geonames_precision')
            html['main'] += '''
            <div class="table-row">
                <div>{label}</div>
                <div class="table-cell">{field}{precision_field}{precision_label} {errors}</div>
            </div>'''.format(label=field.label,
                             errors=errors,
                             field=field(class_=class_),
                             precision_field=precision_field,
                             precision_label=precision_field.label)
            continue
        if field.id == 'geonames_precision':
            continue  # Is already added with geonames_id field
        html['main'] += '''
            <div class="table-row">
                <div>{label}</div>
                <div class="table-cell">{field} {errors}</div>
            </div>'''.format(label=field.label,
                             errors=errors,
                             field=field(class_=class_).replace('> ', '>'))

    html_all = '<form method="post"' + id_attribute + ' ' + multipart + '>'
    html_all += '<div class="data-table">'
    if html['value_types']:
        values_html = """
            <div class="table-row">
                <div>
                    <label>{values}</label>
                </div>
                <div class="table-cell value-type-switcher">
                    <span id="value-type-switcher" class="button">{show}</span>
                </div>
            </div>
            """.format(values=util.uc_first(_('values')), show=util.uc_first(_('show')))
        html['value_types'] = values_html + html['value_types']
    html_all += html['header'] + html['types'] + html['main'] + html['value_types'] + html['footer']
    html_all += '</div></form>'
    return html_all


@jinja2.contextfilter
@blueprint.app_template_filter()
def test_file(self: Any, file_name: str) -> Optional[str]:
    return file_name if os.path.isfile(app.root_path + '/' + file_name) else None


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_tooltip(self: Any, text: str) -> str:
    return util.display_tooltip(text)


@jinja2.contextfilter
@blueprint.app_template_filter()
def sanitize(self: Any, string: str) -> str:
    return util.sanitize(string)


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_delete_link(self: Any, entity: Entity) -> str:
    """ Build a link to delete an entity with a JavaScript confirmation dialog."""
    name = entity.name.replace('\'', '')
    return '<a {confirm} href="{url}">{label}</a>'.format(
        confirm='onclick="return confirm(\'' + _('Delete %(name)s?', name=name) + '\')"',
        url=url_for(entity.view_name + '_index', action='delete', id_=entity.id),
        label=util.uc_first(_('delete')))


@jinja2.contextfilter
@blueprint.app_template_filter()
def display_menu(self: Any, origin: Entity) -> str:
    """ Returns HTML with the menu and mark appropriate item as selected."""
    html = ''
    if current_user.is_authenticated:
        selected = origin.view_name if origin else ''
        items = ['overview', 'source', 'event', 'actor', 'place', 'reference', 'object', 'types',
                 'admin', 'api']
        for item in items:
            if selected:
                css = 'active' if item == selected else ''
            else:
                css = 'active' if request.path.startswith('/' + item) or \
                                  (item == 'overview' and request.path == '/') else ''
            html += '<div class="{css}"><a href="/{item}">{label}</a></div>'.format(
                css=css, item=item, label=util.uc_first(_(item)))
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
    """ Formats external references for display."""
    html = ''
    for link_ in entity.external_references:
        url = link_.domain.name
        name = util.truncate(url.replace('http://', '').replace('https://', ''), span=False)
        if link_.description:
            name = link_.description
        if link_.domain.system_type == 'external reference geonames':
            name = 'GeoNames (' + link_.domain.name + ')'
            url = app.config['GEONAMES_VIEW_URL'] + link_.domain.name
        html += '<a target="_blank" href="{url}">{name}</a><br>'.format(url=url, name=name)
    return '<h2>' + util.uc_first(_('external references')) + '</h2>' + html if html else ''
