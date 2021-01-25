from typing import Any, Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.field import TableField
from openatlas.forms.form import build_add_reference_form, build_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.display import link, uc_first
from openatlas.util.util import required_group, was_modified


class AddReferenceForm(FlaskForm):  # type: ignore
    reference = TableField(_('reference'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


@app.route('/reference/add/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_add(id_: int, class_name: str) -> Union[str, Response]:
    reference = Entity.get_by_id(id_, view_name='reference')
    form = build_add_reference_form(class_name)
    if form.validate_on_submit():
        property_code = 'P128' if reference.class_.code == 'E84' else 'P67'
        entity = Entity.get_by_id(getattr(form, class_name).data)
        reference.link(property_code, entity, form.page.data)
        return redirect(url_for('entity_view', id_=reference.id) + '#tab-' + class_name)
    if reference.system_type == 'external reference':
        form.page.label.text = uc_first(_('link text'))
    return render_template('reference/add.html',
                           reference=reference,
                           form=form,
                           class_name=class_name)


@app.route('/reference/link-update/<int:link_id>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_link_update(link_id: int, origin_id: int) -> Union[str, Response]:
    link_ = Link.get_by_id(link_id)
    origin = Entity.get_by_id(origin_id)
    form = AddReferenceForm()
    del form.reference
    if form.validate_on_submit():
        link_.description = form.page.data
        link_.update()
        flash(_('info update'), 'info')
        tab = '#tab-' + (link_.range.view_name if origin.view_name == 'reference' else 'reference')
        return redirect(url_for('entity_view', id_=origin.id) + tab)
    form.save.label.text = _('save')
    form.page.data = link_.description
    if link_.domain.system_type == 'external reference':
        form.page.label.text = uc_first(_('link text'))
    linked_object = link_.domain if link_.domain.id != origin.id else link_.range
    return render_template('reference/link-update.html',
                           origin=origin,
                           form=form,
                           linked_object=linked_object)


@app.route('/reference/insert/<category>', methods=['POST', 'GET'])
@app.route('/reference/insert/<category>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_insert(category: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    form = build_form(category.replace(' ', '_'), origin=origin)
    if form.validate_on_submit():
        return redirect(save(form, category=category, origin=origin))
    return render_template('reference/insert.html', form=form, category=category, origin=origin)


@app.route('/reference/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_update(id_: int) -> Union[str, Response]:
    reference = Entity.get_by_id(id_, nodes=True, view_name='reference')
    form_name = reference.system_type.replace(' ', '_')
    if form_name.startswith('external_reference'):
        form_name = 'external_reference'
    form = build_form(form_name, reference)
    if form.validate_on_submit():
        if was_modified(form, reference):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(reference.id)['modifier'])
            return render_template('reference/update.html',
                                   form=form,
                                   reference=reference,
                                   modifier=modifier)
        save(form, reference)
        return redirect(url_for('entity_view', id_=id_))
    return render_template('reference/update.html', form=form, reference=reference)


def save(form: Any,
         reference: Optional[Entity] = None,
         category: Optional[str] = None,
         origin: Optional[Entity] = None) -> str:
    g.cursor.execute('BEGIN')
    log_action = 'update'
    try:
        if not category and not reference:
            abort(400)  # pragma: no cover, either reference or category has to be provided
        elif not reference:
            log_action = 'insert'
            system_type = category.replace('_', ' ')  # type: ignore
            reference = Entity.insert('E31', form.name.data, system_type)
        reference.update(form)
        url = url_for('entity_view', id_=reference.id)
        if origin:
            link_id = reference.link('P67', origin)[0]
            url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
        if hasattr(form, 'continue_') and form.continue_.data == 'yes' and category:
            url = url_for('reference_insert', category=category)
        g.cursor.execute('COMMIT')
        logger.log_user(reference.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('reference_index')
    return url
