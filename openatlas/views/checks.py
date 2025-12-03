from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from werkzeug import Response
from werkzeug.utils import redirect

from openatlas import app
from openatlas.api.resources.util import filter_by_type
from openatlas.display.image_processing import delete_orphaned_resized_images
from openatlas.display.tab import Tab
from openatlas.display.table import Table, entity_table
from openatlas.display.util import (
    button, check_iiif_activation, get_file_path, link, required_group)
from openatlas.display.util2 import convert_size, is_authorized, manual
from openatlas.forms.display import display_form
from openatlas.forms.setting import SimilarForm
from openatlas.models import checks
from openatlas.models.annotation import AnnotationImage, AnnotationText
from openatlas.models.dates import format_date
from openatlas.models.entity import Entity
from openatlas.models.export import find_duplicates


@app.route('/check_links')
@required_group('contributor')
def check_links() -> str:
    tabs = {
        'cidoc': Tab(
            'cidoc',
            _('invalid CIDOC links'),
            table=entity_table(
                checks.invalid_cidoc_links(),
                columns=['name', 'property', 'range'])),
        'duplicates': Tab(
            'duplicates',
            _('link duplicates'),
            table=Table([
                'domain', 'range', 'property_code', 'description', 'type',
                'begin_from', 'begin_to', 'begin_comment',
                'end_from', 'end_to', 'end_comment', 'count'])),
        'type': Tab(
            'type',
            _('invalid multiple types'),
            table=Table(['entity', 'class', 'base type', 'types'])),
        'circular': Tab(
            'circular',
            _('circular dependencies'),
            table=entity_table(
                checks.entities_linked_to_itself(),
                columns=['name']))}
    for row in checks.single_type_duplicates():
        remove_links = []
        for type_ in row['offending_types']:
            url = url_for(
                'delete_single_type_duplicate',
                entity_id=row['entity'].id,
                type_id=type_.id)
            remove_links.append(f"{link(_('remove'), url)} {type_.name}")
        tabs['type'].table.rows.append([
            link(row['entity']),
            row['entity'].class_.label,
            link(g.types[row['type'].id]),
            '<br><br>'.join(remove_links)])
    for row in checks.link_duplicates():
        tabs['duplicates'].table.rows.append([
            link(Entity.get_by_id(row['domain_id'])),
            link(Entity.get_by_id(row['range_id'])),
            link(g.properties[row['property_code']]),
            row['description'],
            link(g.types[row['type_id']]) if row['type_id'] else '',
            format_date(row['begin_from']),
            format_date(row['begin_to']),
            row['begin_comment'],
            format_date(row['end_from']),
            format_date(row['end_to']),
            row['end_comment'],
            row['count']])
    for name, tab in tabs.items():
        if not tab.table.rows:
            tab.content = _('Congratulations, everything looks fine!')
        tab.buttons = [manual('admin/data_integrity_checks')]
        if name == 'duplicates' and tab.table.rows:
            tab.buttons.append(
                button(
                    _('delete link duplicates'),
                    url_for('delete_link_duplicates')))
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('check links')])


@app.route('/delete_single_type_duplicate/<int:entity_id>/<int:type_id>')
@required_group('contributor')
def delete_single_type_duplicate(entity_id: int, type_id: int) -> Response:
    g.types[type_id].remove_entity_links(entity_id)
    flash(_('link removed'))
    return redirect(url_for('check_links') + '#tab-type')


@app.route('/delete_link_duplicates')
@required_group('contributor')
def delete_link_duplicates() -> Response:
    count = checks.delete_link_duplicates()
    g.logger.log('info', 'admin', f"Deleted duplicate links: {count}")
    flash(f"{_('deleted links')}: {count}")
    return redirect(url_for('check_links') + '#tab-duplicates')


@app.route('/check_similar', methods=['GET', 'POST'])
@required_group('contributor')
def check_similar() -> str:
    form = SimilarForm()
    form.classes.choices = [
        (c.name, c.label) for c in g.classes.values() if c.group]
    table = Table()
    if form.validate_on_submit():
        table = Table(['name', _('count')])
        for item in checks.similar_named(
                form.classes.data,
                form.ratio.data).values():
            similar = [link(entity) for entity in item['entities']]
            table.rows.append([
                f"{link(item['entity'])}<br>{'<br>'.join(similar)}",
                len(item['entities']) + 1])
    content = display_form(form, manual_page='admin/data_integrity_checks')
    content += ('<p class="uc-first">' + _('no entries') + '</p>') \
        if table and not table.rows else ''
    return render_template(
        'tabs.html',
        tabs={'similar': Tab('similar', content=content, table=table)},
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('check similar names')])


@app.route('/check/dates')
@required_group('contributor')
def check_dates() -> str:
    tabs = {
        'dates': Tab(
            'invalid_dates',
            _('invalid dates'),
            table=entity_table(checks.invalid_dates())),
        'link_dates': Tab(
            'invalid_link_dates',
            _('invalid link dates'),
            table=Table(['link', 'domain', 'range'])),
        'involvement_dates': Tab(
            'invalid_involvement_dates',
            _('invalid involvement dates'),
            table=entity_table(
                checks.invalid_involvement_dates(),
                columns=['name', 'range', 'type_link', 'description'])),
        'preceding_dates': Tab(
            'invalid_preceding_dates',
            _('invalid preceding dates'),
            table=entity_table(
                checks.invalid_preceding_dates(),
                columns=['preceding', 'succeeding'])),
        'sub_dates': Tab(
            'invalid_sub_dates',
            _('invalid sub dates'),
            table=entity_table(
                checks.invalid_sub_dates(),
                columns=['super', 'sub']))}
    for link_ in checks.get_invalid_link_dates():
        url = ''
        domain = link_.domain.class_.name
        for name, relation in g.classes[domain].relations.items():
            if relation.property == link_.property.code \
                    and link_.range.class_.name in relation.classes:
                url = url_for(
                    'link_update',
                    id_=link_.id,
                    origin_id=link_.domain.id,
                    name=name)
                break
        tabs['link_dates'].table.rows.append([
            link(link_.property.name, url),
            link(link_.domain),
            link(link_.range)])
    for tab in tabs.values():
        tab.buttons = [manual('admin/data_integrity_checks')]
        if not tab.table.rows:
            tab.content = _('Congratulations, everything looks fine!')
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('check dates')])


@app.route('/orphans')
@required_group('contributor')
def orphans() -> str:
    columns = [
        'name',
        'class',
        'type',
        'created',
        'updated',
        'description']
    tabs = {
        'orphans': Tab(
            'orphans',
            _('orphans'),
            table=entity_table(
                checks.orphans(),
                columns=['name', 'class', 'type', 'description'])),
        'types': Tab(
            'type',
            table=Table(
                ['name', 'root'],
                [[link(type_), link(g.types[type_.root[0]])]
                 for type_ in checks.type_orphans()])),
        'missing_files': Tab(
            'missing_files',
            _('missing files'),
            table=Table(columns)),
        'orphaned_files': Tab(
            'orphaned_files',
            _('orphaned files'),
            table=Table(['name', 'size', 'date', 'ext'])),
        'orphaned_iiif_files': Tab(
            'orphaned_iiif_files',
            _('orphaned iiif files'),
            table=Table(['name', 'size', 'date', 'ext'])),
        'orphaned_image_annotations': Tab(
            'orphaned_image_annotations',
            _('orphaned image annotations'),
            table=Table(
                ['image', 'entity', 'annotation', 'creation'],
                get_orphaned_image_annotations())),
        'orphaned_text_annotations': Tab(
            'orphaned_text_annotations',
            _('orphaned text annotations'),
            table=Table(
                ['image', 'entity', 'annotation', 'creation'],
                get_orphaned_text_annotations())),
        'orphaned_subunits': Tab(
            'orphaned_subunits',
            _('orphaned subunits'),
            table=Table(
                ['id', 'name', 'class', 'created', 'modified', 'description'],
                [[
                    e.id,
                    e.name,
                    e.class_.label,
                    format_date(e.created),
                    format_date(e.modified),
                    e.description] for e in checks.orphaned_subunits()]))}
    for tab in tabs.values():
        tab.buttons = [manual('admin/data_integrity_checks')]
    entity_file_ids = []
    for entity in Entity.get_by_class('file', types=True):
        entity_file_ids.append(entity.id)
        if not get_file_path(entity):
            tabs['missing_files'].table.rows.append([
                link(entity),
                link(entity.class_),
                link(entity.standard_type),
                entity.class_.label,
                format_date(entity.created),
                format_date(entity.modified),
                entity.description])

    tabs['orphaned_files'].table.rows = \
        get_files_without_entity(entity_file_ids)

    if check_iiif_activation():
        tabs['orphaned_iiif_files'].table.rows = \
            get_iiif_files_without_entity(entity_file_ids)

    for tab in tabs.values():
        if not tab.table.rows:
            tab.content = _('Congratulations, everything looks fine!')

    if tabs['orphaned_files'].table.rows and is_authorized('admin'):
        text = _('delete all files without corresponding entities?')
        tabs['orphaned_files'].buttons.append(
            button(
                _('delete all files'),
                url_for('admin_file_delete', filename='all'),
                onclick=f"return confirm('{text}')"))
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('orphans')])


@app.route('/check_files')
@app.route('/check_files/<arche>')
@required_group('contributor')
def check_files(arche: Optional[str] = None) -> str:
    entities: list[Entity] = Entity.get_by_class('file', types=True)
    result: dict[str, list[Entity]] = {
        'missing_files': [],
        'not_public': [],
        'no_creator': [],
        'no_license_holder': [],
        'no_license': []}
    for entity in entities:
        if not get_file_path(entity):
            result['missing_files'].append(entity)
        if not entity.public:
            result['not_public'].append(entity)
        if not entity.creator:
            result['no_creator'].append(entity)
        if not entity.license_holder:
            result['no_license_holder'].append(entity)
        if not entity.standard_type:
            result['no_license'].append(entity)
    tabs = {
        'no_creator': Tab(
            'no_creator',
            _('no creator'),
            table=entity_table(result['no_creator'])),
        'no_license_holder': Tab(
            'no_license_holder',
            _('no license holder'),
            table=entity_table(result['no_license_holder'])),
        'not_public': Tab(
            'not_public',
            _('not public'),
            table=entity_table(result['not_public'])),
        'no_license': Tab(
            'no_license',
            _('no license'),
            table=entity_table(result['no_license'])),
        'missing_files': Tab(
            'missing_files',
            _('missing files'),
            table=entity_table(result['missing_files'])),
        'duplicates': Tab(
            'duplicates',
            _('duplicated files'),
            table=Table(['domain', 'range']))}
    for tab in tabs.values():
        tab.buttons = [manual('admin/data_integrity_checks')]
    if arche:
        type_ids = app.config['ARCHE_METADATA'].get('typeIds')
        if type_ids:
            entities = filter_by_type(entities, type_ids)
    duplicates = find_duplicates({e.id for e in entities})
    duplicate_ids = set().union(*duplicates)
    mapping = {e.id: e for e in Entity.get_by_ids(list(duplicate_ids))}
    for values in duplicates:
        if entity1 := mapping.get(values[0]):
            if entity2 := mapping.get(values[1]):
                tabs['duplicates'].table.rows.append([
                    link(entity1),
                    link(entity2)])
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            [_('export') + ' ARCHE', f"{url_for('export_arche')}"]
            if arche else None,
            _('check files')])


@app.route('/admin/delete_orphaned_resized_images')
@required_group('admin')
def admin_delete_orphaned_resized_images() -> Response:
    delete_orphaned_resized_images()
    flash(_('resized orphaned images were deleted'))
    return redirect(url_for('admin_index') + '#tab-data')


def get_files_without_entity(entity_file_ids: list[int]) -> list[Any]:
    rows = []
    for file in app.config['UPLOAD_PATH'].iterdir():
        if file.name != '.gitignore' \
                and os.path.isfile(file) \
                and file.stem.isdigit() \
                and int(file.stem) not in entity_file_ids:
            confirm = _('Delete %(name)s?', name=file.name.replace("'", ''))
            rows.append([
                file.stem,
                convert_size(file.stat().st_size),
                format_date(datetime.fromtimestamp(file.stat().st_ctime)),
                file.suffix,
                link(_('download'), url_for('download', filename=file.name)),
                link(
                    _('delete'),
                    url_for('admin_file_delete', filename=file.name),
                    js=f"return confirm('{confirm}')")
                if is_authorized('editor') else ''])
    return rows


def get_iiif_files_without_entity(entity_file_ids: list[int]) -> list[Any]:
    rows = []
    for file in Path(g.settings['iiif_path']).iterdir():
        confirm = _('Delete %(name)s?', name=file.name.replace("'", ''))
        if file.name != '.gitignore' \
                and os.path.isfile(file) \
                and file.stem.isdigit() \
                and int(file.stem) not in entity_file_ids:
            rows.append([
                file.stem,
                convert_size(file.stat().st_size),
                format_date(datetime.fromtimestamp(file.stat().st_ctime)),
                file.suffix,
                link(
                    _('delete'),
                    url_for('admin_file_iiif_delete', filename=file.name),
                    js=f"return confirm('{confirm}')")
                if is_authorized('editor') else ''])
    return rows


def get_orphaned_image_annotations() -> list[Any]:
    rows = []
    for annotation in AnnotationImage.get_orphaned_annotations():
        file = Entity.get_by_id(annotation.image_id)
        entity = Entity.get_by_id(annotation.entity_id)
        rows.append([
            link(file),
            link(entity),
            annotation.text,
            annotation.created,
            link(
                _('relink entity'),
                url_for(
                    'admin_annotation_image_relink',
                    origin_id=file.id,
                    entity_id=entity.id),
                js=f"return confirm('{_('relink entity')}?')"),
            link(
                _('remove entity'),
                url_for(
                    'admin_annotation_image_remove_entity',
                    annotation_id=annotation.id,
                    entity_id=entity.id),
                js=f"return confirm('{_('remove entity')}?')"),
            link(
                _('delete annotation'),
                url_for('admin_annotation_image_delete', id_=annotation.id),
                js=f"return confirm('{_('delete annotation')}?')")])
    return rows


def get_orphaned_text_annotations() -> list[Any]:
    rows = []
    for annotation in AnnotationText.get_orphaned_annotations():
        source = Entity.get_by_id(annotation.source_id)
        entity = Entity.get_by_id(annotation.entity_id)
        rows.append([
            link(source),
            link(entity),
            annotation.text,
            annotation.created,
            link(
                _('relink entity'),
                url_for(
                    'admin_annotation_text_relink',
                    origin_id=annotation.source_root or source.id,
                    entity_id=entity.id),
                js=f"return confirm('{_('relink entity')}?')"),
            link(
                _('remove entity'),
                url_for(
                    'admin_annotation_text_remove_entity',
                    annotation_id=annotation.id,
                    entity_id=entity.id),
                js=f"return confirm('{_('remove entity')}?')"),
            link(
                _('delete annotation'),
                url_for('admin_annotation_text_delete', id_=source.id),
                js=f"return confirm('{_('delete annotation')}?')")])
    return rows
