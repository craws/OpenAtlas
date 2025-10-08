from flask import g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.image_processing import check_processed_image
from openatlas.display.table import Table, entity_table
from openatlas.display.util import (
    button, check_iiif_file_exist, get_file_path, link, required_group)
from openatlas.display.util2 import is_authorized, manual
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.reference_system import ReferenceSystem


@app.route('/index/<group>')
@required_group('readonly')
def index(group: str) -> str | Response:
    buttons = [manual(f'entity/{group}')]
    for name in g.class_groups[group]['classes'] \
            if group != 'place' else ['place']:
        if is_authorized(g.classes[name].write_access):
            buttons.append(
                button(
                    g.classes[name].label,
                    url_for('insert', class_=name),
                    tooltip_text=g.classes[name].display['tooltip']))
    return render_template(
        'entity/index.html',
        class_=group,
        table=get_table(group),
        buttons=buttons,
        gis_data=Gis.get_all() if group == 'place' else None,
        title=_(group.replace('_', ' ')),
        crumbs=[_(group).replace('_', ' ')])


def get_table(group: str) -> Table:
    if group == 'reference_system':
        table = Table([
             'name', 'count', 'website URL', 'resolver URL', 'example ID',
             'default precision', 'description'])
        counts = ReferenceSystem.get_counts()
        for system in g.reference_systems.values():
            table.rows.append([
                link(system),
                format_number(counts[system.id]) if counts[system.id] else '',
                link(system.website_url, system.website_url, external=True),
                link(system.resolver_url, system.resolver_url, external=True),
                system.placeholder,
                link(g.types[system.precision_default_id])
                if system.precision_default_id else '',
                system.description])
    else:
        table = entity_table(
            Entity.get_by_class(
                'place' if group == 'place'
                else g.class_groups[group]['classes'],
                types=True,
                aliases=True))
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
    if icon := get_file_path(entity_id, app.config['IMAGE_SIZE']['table']):
        url = url_for('display_file', filename=icon.name, size=size)
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
