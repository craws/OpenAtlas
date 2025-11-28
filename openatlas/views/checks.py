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
from openatlas.display.table import Table
from openatlas.display.util import (
    button, check_iiif_activation, get_file_path, link, required_group)
from openatlas.display.util2 import convert_size, is_authorized, manual
from openatlas.forms.display import display_form
from openatlas.forms.setting import SimilarForm
from openatlas.models.annotation import AnnotationImage, AnnotationText
from openatlas.models.checks import (
    entities_linked_to_itself, invalid_cidoc_links, invalid_dates,
    orphaned_subunits, orphans as get_orphans, similar_named,
    single_type_duplicates)
from openatlas.models.dates import format_date
from openatlas.models.entity import Entity, Link
from openatlas.models.export import find_duplicates


@app.route('/check_links')
@required_group('contributor')
def check_links() -> str:
    table = Table(['domain', 'property', 'range'])
    for row in invalid_cidoc_links():
        table.rows.append([
            f"{link(row['domain'])} ({row['domain'].cidoc_class.code})",
            link(row['property']),
            f"{link(row['range'])} ({row['range'].cidoc_class.code})"])
    return render_template(
        'tabs.html',
        tabs={
            'links': Tab(
                'links',
                content='' if table.rows
                else _('Congratulations, everything looks fine!'),
                table=table,
                buttons=[manual('admin/data_integrity_checks')])},
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('check links')])


@app.route('/check_link_duplicates')
@app.route('/check_link_duplicates/<delete>')
@required_group('contributor')
def check_link_duplicates(delete: Optional[str] = None) -> str | Response:
    if delete:
        count = Link.delete_link_duplicates()
        g.logger.log('info', 'admin', f"Deleted duplicate links: {count}")
        flash(f"{_('deleted links')}: {count}")
        return redirect(url_for('check_link_duplicates'))
    tab = Tab(
        'check_link_duplicates',
        buttons=[manual('admin/data_integrity_checks')])
    tab.table = Table([
        'domain', 'range', 'property_code', 'description', 'type_id',
        'begin_from', 'begin_to', 'begin_comment', 'end_from', 'end_to',
        'end_comment', 'count'])
    for row in Link.check_link_duplicates():
        tab.table.rows.append([
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
    if tab.table.rows:
        tab.buttons.append(
            button(
                _('delete link duplicates'),
                url_for('check_link_duplicates', delete='delete')))
    else:  # Check single types for multiple use
        tab.table = Table(
            ['entity', 'class', 'base type', 'incorrect multiple types'])
        for row in single_type_duplicates():
            remove_links = []
            for type_ in row['offending_types']:
                url = url_for(
                    'delete_single_type_duplicate',
                    entity_id=row['entity'].id,
                    type_id=type_.id)
                remove_links.append(f"{link(_('remove'), url)} {type_.name}")
            tab.table.rows.append([
                link(row['entity']),
                row['entity'].class_.label,
                link(g.types[row['type'].id]),
                '<br><br>'.join(remove_links)])
    if not tab.table.rows:
        tab.content = _('Congratulations, everything looks fine!')
    return render_template(
        'tabs.html',
        tabs={'tab': tab},
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            _('check link duplicates')])


@app.route('/delete_single_type_duplicate/<int:entity_id>/<int:type_id>')
@required_group('contributor')
def delete_single_type_duplicate(entity_id: int, type_id: int) -> Response:
    g.types[type_id].remove_entity_links(entity_id)
    flash(_('link removed'))
    return redirect(url_for('check_link_duplicates'))


@app.route('/check_similar', methods=['GET', 'POST'])
@required_group('contributor')
def check_similar() -> str:
    form = SimilarForm()
    form.classes.choices = [
        (class_.name, class_.label)
        for name, class_ in g.classes.items() if class_.group]
    table = None
    if form.validate_on_submit():
        table = Table(['name', _('count')])
        for item in similar_named(form.classes.data, form.ratio.data).values():
            similar = [link(entity) for entity in item['entities']]
            table.rows.append([
                f"{link(item['entity'])}<br><br>{'<br><br>'.join(similar)}",
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
            table=Table([
                'name',
                'class',
                'type',
                'created',
                'updated',
                'description'])),
        'link_dates': Tab(
            'invalid_link_dates',
            _('invalid link dates'),
            table=Table(['link', 'domain', 'range'])),
        'involvement_dates': Tab(
            'invalid_involvement_dates',
            _('invalid involvement dates'),
            table=Table(
                ['actor', 'event', 'class', 'involvement', 'description'])),
        'preceding_dates': Tab(
            'invalid_preceding_dates',
            _('invalid preceding dates'),
            table=Table(['preceding', 'succeeding'])),
        'sub_dates': Tab(
            'invalid_sub_dates',
            _('invalid sub dates'),
            table=Table(['super', 'sub']))}
    for entity in invalid_dates():
        tabs['dates'].table.rows.append([
            link(entity),
            entity.class_.label,
            link(entity.standard_type),
            format_date(entity.created),
            format_date(entity.modified),
            entity.description])
    for link_ in Link.get_invalid_link_dates():
        update_link_ = ''
        domain = link_.domain.class_.name
        for name, relation in g.classes[domain].relations.items():
            if relation.property == link_.property.code \
                    and link_.range.class_.name in relation.classes:
                update_link_ = url_for(
                    'link_update',
                    id_=link_.id,
                    origin_id=link_.domain.id,
                    name=name)
                break
        tabs['link_dates'].table.rows.append([
            link(link_.property.name, update_link_),
            link(link_.domain),
            link(link_.range)])
    for link_ in Link.invalid_involvement_dates():
        event = link_.domain
        actor = link_.range
        data = [
            link(actor),
            link(event),
            event.class_.label,
            link_.type.name if link_.type else '',
            link_.description]
        tabs['involvement_dates'].table.rows.append(data)
    for link_ in Link.invalid_preceding_dates():
        tabs['preceding_dates'].table.rows.append([
            link(link_.range),
            link(link_.domain)])
    for link_ in Link.invalid_sub_dates():
        tabs['sub_dates'].table.rows.append([
            link(link_.range),
            link(link_.domain)])
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
        'orphans': Tab('orphans', _('orphans'), table=Table(columns)),
        'unlinked': Tab('unlinked', _('unlinked'), table=Table(columns)),
        'types': Tab(
            'type',
            table=Table(
                ['name', 'root'],
                [[link(type_), link(g.types[type_.root[0]])]
                 for type_ in Entity.get_type_orphans()])),
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
                    e.description] for e in orphaned_subunits()])),
        'circular': Tab(
            'circular_dependencies',
            _('circular dependencies'),
            table=Table(
                ['entity'],
                [[link(e)] for e in entities_linked_to_itself()]))}
    for tab in tabs.values():
        tab.buttons = [manual('admin/data_integrity_checks')]
    for entity in get_orphans():
        tabs[
            'unlinked'
            if entity.class_.group['name'] else 'orphans'].table.rows.append([
                link(entity),
                link(entity.class_),
                link(entity.standard_type),
                entity.class_.label,
                format_date(entity.created),
                format_date(entity.modified),
                entity.description])

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
    columns = ['name', 'type', 'created', 'updated', 'description']
    tabs = {
        'no_creator': Tab('no_creator', _('no creator'), table=Table(columns)),
        'no_license_holder': Tab(
            'no_license_holder',
            _('no license holder'),
            table=Table(columns)),
        'not_public': Tab('not_public', _('not public'), table=Table(columns)),
        'no_license': Tab('no_license', _('no license'), table=Table(columns)),
        'missing_files': Tab(
            'missing_files',
            _('missing files'),
            table=Table(columns)),
        'duplicated_files': Tab(
            'duplicated_files',
            _('duplicated files'),
            table=Table(['domain', 'range']))}

    for tab in tabs.values():
        tab.buttons = [manual('admin/data_integrity_checks')]

    entities: list[Entity] = Entity.get_by_class('file', types=True)
    if arche:
        type_ids = app.config['ARCHE_METADATA'].get('typeIds')
        if type_ids:
            entities = filter_by_type(entities, type_ids)
    for entity in entities:
        entity_for_table = [
            link(entity),
            link(entity.standard_type),
            format_date(entity.created),
            format_date(entity.modified),
            entity.description]
        if not get_file_path(entity):
            tabs['missing_files'].table.rows.append(entity_for_table)
        if not entity.public:
            tabs['not_public'].table.rows.append(entity_for_table)
        if not entity.creator:
            tabs['no_creator'].table.rows.append(entity_for_table)
        if not entity.license_holder:
            tabs['no_license_holder'].table.rows.append(entity_for_table)
        if not entity.standard_type:
            tabs['no_license'].table.rows.append(entity_for_table)

    duplicated_files = find_duplicates({e.id for e in entities})
    all_duplicate_ids = set().union(*duplicated_files)
    duplicate_entities = Entity.get_by_ids(list(all_duplicate_ids))
    duplicate_entity_map = {e.id: e for e in duplicate_entities}
    for duplicate_group in duplicated_files:
        entity1 = duplicate_entity_map.get(duplicate_group[0])
        entity2 = duplicate_entity_map.get(duplicate_group[1])
        if entity1 and entity2:
            tabs['duplicated_files'].table.rows.append([
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
