import json
from typing import Union

from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import TextAreaField
from wtforms.fields.simple import HiddenField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    format_date, get_file_path, is_authorized, link, required_group)
from openatlas.forms.field import SubmitField, TableField
from openatlas.models.annotation import Annotation
from openatlas.models.entity import Entity


class AnnotationForm(FlaskForm):
    coordinate = HiddenField(_('coordinates'), validators=[InputRequired()])
    annotation = TextAreaField(_('annotation'))
    annotated_entity = TableField(_('entity'))
    save = SubmitField(_('save'))


class AnnotationUpdateForm(FlaskForm):
    annotation = TextAreaField(_('annotation'))
    annotated_entity = TableField(_('entity'))
    save = SubmitField(_('save'))


@app.route('/annotation_insert/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def annotation_insert(id_: int) -> Union[str, Response]:
    image = Entity.get_by_id(id_, types=True, aliases=True)
    if not get_file_path(image.id):
        return abort(404)
    form = AnnotationForm()
    form.annotated_entity.filter_ids = [image.id]
    if form.validate_on_submit():
        Annotation.insert(
            image_id=id_,
            coordinates=form.coordinate.data,
            entity_id=form.annotated_entity.data,
            annotation=form.annotation.data)
        return redirect(url_for('annotation_insert', id_=image.id))
    table = None
    if annotations := Annotation.get_by_file(image.id):
        rows = []
        for annotation in annotations:
            delete = ''
            if is_authorized('editor') or (
                    is_authorized('contributor')
                    and current_user.id == annotation.user_id):
                delete = link(
                    _('delete'),
                    url_for('annotation_delete', id_=annotation.id))
            rows.append([
                format_date(annotation.created),
                annotation.annotation,
                link(Entity.get_by_id(annotation.entity_id))
                if annotation.entity_id else '',
                link(
                    _('edit'),
                    url_for('annotation_update', id_=annotation.id)),
                delete])
        table = Table(
            ['date', 'annotation', 'entity'],
            rows=rows,
            order=[[0, 'desc']])
    return render_template(
        'tabs.html',
        tabs={
            'annotation': Tab(
                'annotation',
                form=form,
                table=table,
                content=render_template(
                    'annotate.html',
                    entity=image,
                    annotation_list=json.dumps(annotations, default=str)))},
        entity=image,
        crumbs=[
            [_('file'), url_for('index', view='file')],
            image,
            _('annotate')])


@app.route('/annotation_update/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def annotation_update(id_: int) -> str | Response:
    annotation = Annotation.get_by_id(id_)
    form = AnnotationUpdateForm()
    form.annotated_entity.filter_ids = [annotation.image_id]
    if form.validate_on_submit():
        annotation.update(
            entity_id=form.annotated_entity.data or None,
            annotation=form.annotation.data)
        return redirect(url_for('annotation_insert', id_=annotation.image_id))
    form.annotation.data = annotation.annotation
    form.annotated_entity.data = annotation.entity_id
    return render_template(
        'tabs.html',
        tabs={'annotation': Tab('annotation', form=form)},
        crumbs=[
            [_('file'), url_for('index', view='file')],
            Entity.get_by_id(annotation.image_id),
            _('annotate')])


@app.route('/annotation_delete/<int:id_>')
@required_group('contributor')
def annotation_delete(id_: int) -> Response:
    annotation = Annotation.get_by_id(id_)
    if current_user.group == 'contributor' \
            and annotation.user_id != current_user.id:
        abort(403)
    annotation.delete()
    flash(_('annotation deleted'), 'info')
    return redirect(url_for('annotation_insert', id_=annotation.image_id))
