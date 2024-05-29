from flask import g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.image_processing import check_processed_image
from openatlas.display.table import Table
from openatlas.display.util import (
    button, check_iiif_file_exist, get_base_table_data, get_file_path, link,
    required_group)
from openatlas.display.util2 import (
    format_date, is_authorized, manual, show_table_icons, uc_first)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis


@app.route('/index/<view>')
@required_group('readonly')
def index(view: str) -> str | Response:
    buttons = [manual(f'entity/{view}')]
    for name in g.view_class_mapping[view] if view != 'place' else ['place']:
        if is_authorized(g.classes[name].write_access):
            buttons.append(
                button(
                    g.classes[name].label,
                    url_for('insert', class_=name),
                    tooltip_text=g.classes[name].get_tooltip()))
    crumbs = [_(view).replace('_', ' ')]
    if view == 'file':
        crumbs = [[_('file'), url_for('file_index')], _('files')]
    return render_template(
        'entity/index.html',
        class_=view,
        table=get_table(view),
        buttons=buttons,
        gis_data=Gis.get_all() if view == 'place' else None,
        title=_(view.replace('_', ' ')),
        crumbs=crumbs)


def get_table(view: str) -> Table:
    table = Table(g.table_headers[view])
    if view == 'file':
        stats = {'public': 0, 'without_license': 0, 'without_creator': 0}
        table.order = [[0, 'desc']]
        table.header = ['date'] + table.header
        if show_table_icons():
            table.header.insert(1, _('icon'))
        for entity in Entity.get_by_class('file', types=True):
            if entity.public:
                stats['public'] += 1
                if not entity.standard_type:
                    stats['without_license'] += 1
                elif not entity.creator:
                    stats['without_creator'] += 1
            data = [
                format_date(entity.created),
                link(entity),
                link(entity.standard_type),
                _('yes') if entity.public else None,
                entity.creator,
                entity.license_holder,
                entity.get_file_size(),
                entity.get_file_ext(),
                entity.description]
            if show_table_icons():
                data.insert(1, file_preview(entity.id))
            table.rows.append(data)
        table.additional_information = (
            uc_first(_('files')) + ': ' +
            f"{format_number(stats['public'])} " + _('public') +
            f", {format_number(stats['without_license'])} " +
            _('public without license') +
            f", {format_number(stats['without_creator'])} " +
            _('public with license but without creator'))

    elif view == 'reference_system':
        for system in g.reference_systems.values():
            table.rows.append([
                link(system),
                system.count or '',
                link(system.website_url, system.website_url, external=True),
                link(system.resolver_url, system.resolver_url, external=True),
                system.placeholder,
                link(g.types[system.precision_default_id])
                if system.precision_default_id else '',
                system.description])
    else:
        classes = 'place' if view == 'place' else g.view_class_mapping[view]
        entities = Entity.get_by_class(classes, types=True, aliases=True)
        table.rows = [get_base_table_data(entity) for entity in entities]
    return table


def file_preview(entity_id: int) -> str:
    size = app.config['IMAGE_SIZE']['table']
    param = "loading='lazy' alt='image' max-width='100px' max-height='100px'"
    if g.settings['iiif'] and check_iiif_file_exist(entity_id):
        ext = '.tiff' if g.settings['iiif_conversion'] \
            else g.files[entity_id].suffix
        url =\
            f"{g.settings['iiif_url']}{entity_id}{ext}" \
            f"/full/!100,100/0/default.jpg"
        return f"<img src='{url}' {param}>"
    if icon_path := get_file_path(
            entity_id,
            app.config['IMAGE_SIZE']['table']):
        url = url_for('display_file', filename=icon_path.name, size=size)
        return f"<img src='{url}' {param}>"
    if g.settings['image_processing']:
        path = get_file_path(entity_id)
        if path and check_processed_image(path.name):
            if icon := get_file_path(
                    entity_id,
                    app.config['IMAGE_SIZE']['table']):
                url = url_for('display_file', filename=icon.name, size=size)
                return f"<img src='{url}' {param}>"
    return ''
