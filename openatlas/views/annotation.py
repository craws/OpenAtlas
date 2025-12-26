from flask import flash, render_template, url_for
from flask_babel import gettext as _
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import get_file_path, link, required_group
from openatlas.display.util2 import is_authorized, manual
from openatlas.forms.form import annotate_image_form
from openatlas.models.annotation import AnnotationImage
from openatlas.models.dates import format_date
from openatlas.models.entity import Entity


@app.route('/annotation_image_insert/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def annotation_image_insert(id_: int) -> str | Response:
    image = Entity.get_by_id(id_, types=True, aliases=True)
    if not get_file_path(image.id):
        return abort(404)  # pragma: no cover
    form = annotate_image_form(image.id)
    if form.validate_on_submit():
        AnnotationImage.insert(
            image_id=id_,
            coordinates=form.coordinate.data,
            entity_id=form.entity.data,
            text=form.text.data)
        return redirect(url_for('annotation_image_insert', id_=image.id))
    table = Table()
    if annotations := AnnotationImage.get_by_file_id(image.id):
        rows = []
        for annotation in annotations:
            delete = ''
            if is_authorized('contributor'):
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
                content=render_template('annotate_image.html', entity=image),
                table=table,
                buttons=[manual('tools/image_annotation')],
                form=form)},
        entity=image,
        crumbs=[link(image, index=True), image, _('annotate')])


@app.route('/annotation_image_update/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def annotation_image_update(id_: int) -> str | Response:
    annotation = AnnotationImage.get_by_id(id_)
    form = annotate_image_form(
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
            [_('file'), url_for('index', group='file')],
            Entity.get_by_id(annotation.image_id),
            _('annotate')])


@app.route('/annotation_image_delete/<int:id_>')
@required_group('contributor')
def annotation_image_delete(id_: int) -> Response:
    annotation = AnnotationImage.get_by_id(id_)
    annotation.delete()
    flash(_('annotation deleted'))
    return redirect(
        url_for('annotation_image_insert', id_=annotation.image_id))
