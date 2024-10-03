from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    display_annotation_text_links, get_file_path, link, required_group)
from openatlas.display.util2 import format_date, is_authorized, manual
from openatlas.forms.form import (
    get_annotation_image_form, get_annotation_text_form)
from openatlas.models.annotation import AnnotationImage, AnnotationText
from openatlas.models.entity import Entity


@app.route('/annotation_text_insert/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def annotation_text_insert(id_: int) -> str | Response:
    source = Entity.get_by_id(id_, types=True)
    form = get_annotation_text_form(source.id)
    if form.validate_on_submit():
        AnnotationText.insert(
            source_id=id_,
            link_start=int(form.link_start.data),
            link_end=int(form.link_end.data),
            entity_id=int(form.entity.data) if form.entity.data else None,
            text=form.text.data)
        return redirect(url_for('annotation_text_insert', id_=source.id))
    table = None
    if annotations := AnnotationText.get_by_source_id(source.id):
        table = Table(
            ['date', 'text', 'entity', 'start', 'end'],
            [],
            [[0, 'desc']])
        for annotation in annotations:
            delete = ''
            if is_authorized('editor') or (
                    is_authorized('contributor')
                    and current_user.id == annotation.user_id):
                delete = link(
                    _('delete'),
                    url_for('annotation_text_delete', id_=annotation.id),
                    js="return confirm('" + _('delete annotation') + "?')")
            table.rows.append([
                format_date(annotation.created),
                annotation.text,
                link(Entity.get_by_id(annotation.entity_id))
                if annotation.entity_id else '',
                annotation.link_start,
                annotation.link_end,
                link(
                    _('edit'),
                    url_for('annotation_text_update', id_=annotation.id)),
                delete])

    return render_template(
        'tabs.html',
        tabs={
            'annotation': Tab(
                'annotation',
                render_template(
                    'annotate_text.html',
                    entity=source,
                    formatted_text=display_annotation_text_links(source)),
                table,
                [manual('tools/text_annotation')],
                form=form)},
        entity=source,
        crumbs=[
            [_('source'), url_for('index', view='source')],
            source,
            _('annotate')])


@app.route('/annotation_text_update/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def annotation_text_update(id_: int) -> str | Response:
    annotation = AnnotationText.get_by_id(id_)
    source = Entity.get_by_id(annotation.source_id)
    form = get_annotation_text_form(
        annotation.source_id,
        Entity.get_by_id(annotation.entity_id)
        if annotation.entity_id else None,
        insert=False)
    if form.validate_on_submit():
        annotation.update(
            form.link_start.data,
            form.link_end.data,
            int(form.entity.data) if form.entity.data else None,
            form.text.data)
        return redirect(url_for('annotation_text_insert', id_=source.id))
    form.text.data = annotation.text
    form.entity.data = annotation.entity_id
    form.link_start.data = annotation.link_start
    form.link_end.data = annotation.link_end
    return render_template(
        'tabs.html',
        tabs={'annotation': Tab('annotation', form=form)},
        crumbs=[
            [_('source'), url_for('index', view='source')],
            source,
            _('annotate')])


@app.route('/annotation_image_insert/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def annotation_image_insert(id_: int) -> str | Response:
    image = Entity.get_by_id(id_, types=True, aliases=True)
    if not get_file_path(image.id):
        return abort(404)  # pragma: no cover
    form = get_annotation_image_form(image.id)
    if form.validate_on_submit():
        AnnotationImage.insert(
            image_id=id_,
            coordinates=form.coordinate.data,
            entity_id=form.entity.data,
            text=form.text.data)
        return redirect(url_for('annotation_image_insert', id_=image.id))
    table = None
    if annotations := AnnotationImage.get_by_file(image.id):
        rows = []
        for annotation in annotations:
            delete = ''
            if is_authorized('editor') or (
                    is_authorized('contributor')
                    and current_user.id == annotation.user_id):
                delete = link(
                    _('delete'),
                    url_for('annotation_image_delete', id_=annotation.id),
                    js="return confirm('" + _('delete annotation') + "?')")
            rows.append([
                format_date(annotation.created),
                annotation.text,
                link(Entity.get_by_id(annotation.entity_id))
                if annotation.entity_id else '',
                link(
                    _('edit'),
                    url_for('annotation_image_update', id_=annotation.id)),
                delete])
        table = Table(['date', 'text', 'entity'], rows, [[0, 'desc']])
    return render_template(
        'tabs.html',
        tabs={
            'annotation': Tab(
                'annotation',
                render_template('annotate_image.html', entity=image),
                table,
                [manual('tools/image_annotation')],
                form=form)},
        entity=image,
        crumbs=[
            [_('file'), url_for('index', view='file')],
            image,
            _('annotate')])


@app.route('/annotation_image_update/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def annotation_image_update(id_: int) -> str | Response:
    annotation = AnnotationImage.get_by_id(id_)
    form = get_annotation_image_form(
        annotation.image_id,
        Entity.get_by_id(annotation.entity_id)
        if annotation.entity_id else None,
        insert=False)
    if form.validate_on_submit():
        annotation.update(form.entity.data or None, form.text.data)
        return redirect(
            url_for('annotation_image_insert', id_=annotation.image_id))
    form.text.data = annotation.text
    form.entity.data = annotation.entity_id
    return render_template(
        'tabs.html',
        tabs={'annotation': Tab('annotation', form=form)},
        crumbs=[
            [_('file'), url_for('index', view='file')],
            Entity.get_by_id(annotation.image_id),
            _('annotate')])


@app.route('/annotation_image_delete/<int:id_>')
@required_group('contributor')
def annotation_image_delete(id_: int) -> Response:
    annotation = AnnotationImage.get_by_id(id_)
    if current_user.group == 'contributor' \
            and annotation.user_id != current_user.id:
        abort(403)  # pragma: no cover
    annotation.delete()
    flash(_('annotation deleted'), 'info')
    return redirect(
        url_for('annotation_image_insert', id_=annotation.image_id))


@app.route('/annotation_text_delete/<int:id_>')
@required_group('contributor')
def annotation_text_delete(id_: int) -> Response:
    annotation = AnnotationText.get_by_id(id_)
    if current_user.group == 'contributor' \
            and annotation.user_id != current_user.id:
        abort(403)  # pragma: no cover
    annotation.delete()
    flash(_('annotation deleted'), 'info')
    return redirect(
        url_for('annotation_text_insert', id_=annotation.source_id))
