from typing import Any, Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, URL

import openatlas
from openatlas import app, logger
from openatlas.forms.forms import TableField, build_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.user import User
from openatlas.util.display import (add_edit_link, add_remove_link, get_base_table_data,
                                    get_entity_data, get_profile_image_table_link, link, uc_first)
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import required_group, was_modified


class ReferenceForm(FlaskForm):  # type: ignore
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


class AddReferenceForm(FlaskForm):  # type: ignore
    reference = TableField(_('reference'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


class AddSourceForm(FlaskForm):  # type: ignore
    source = TableField(_('source'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


class AddEventForm(FlaskForm):  # type: ignore
    event = TableField(_('event'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


class AddActorForm(FlaskForm):  # type: ignore
    actor = TableField(_('actor'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


class AddPlaceForm(FlaskForm):  # type: ignore
    place = TableField(_('place'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


class AddFileForm(FlaskForm):  # type: ignore
    file = TableField(_('file'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


@app.route('/reference/add/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_add(id_: int, class_name: str) -> Union[str, Response]:
    reference = Entity.get_by_id(id_, view_name='reference')
    form = getattr(openatlas.views.reference, 'Add' + uc_first(class_name) + 'Form')()
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


@app.route('/reference')
@app.route('/reference/<action>/<int:id_>')
@required_group('readonly')
def reference_index(action: Optional[str] = None, id_: Optional[int] = None) -> str:
    if id_ and action == 'delete':
        Entity.delete_(id_)
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
    table = Table(Table.HEADERS['reference'])
    table.rows = [get_base_table_data(item) for item in Entity.get_by_menu_item('reference')]
    return render_template('reference/index.html', table=table)


@app.route('/reference/insert/<code>', methods=['POST', 'GET'])
@app.route('/reference/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_insert(code: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    form = build_form(ReferenceForm, 'External Reference' if code == 'external_reference' else code)
    if code == 'external_reference':
        form.name.validators = [InputRequired(), URL()]
        form.name.label.text = 'URL'
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        return redirect(save(form, code=code, origin=origin))
    return render_template('reference/insert.html', form=form, code=code, origin=origin)


@app.route('/reference/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_update(id_: int) -> Union[str, Response]:
    reference = Entity.get_by_id(id_, nodes=True, view_name='reference')
    form = build_form(ReferenceForm, reference.system_type.title(), reference, request)
    if reference.system_type == 'external reference':
        form.name.validators = [InputRequired(), URL()]
        form.name.label.text = 'URL'
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


def reference_view(reference: Entity) -> str:
    tabs = {name: Tab(name, origin=reference) for name in [
        'info', 'source', 'event', 'actor', 'place', 'feature', 'stratigraphic_unit', 'find',
        'human_remains', 'file']}
    for link_ in reference.get_links('P67', True):
        domain = link_.domain
        data = get_base_table_data(domain)
        data = add_remove_link(data, domain.name, link_, reference, 'file')
        tabs['file'].table.rows.append(data)
    profile_image_id = reference.get_profile_image_id()
    for link_ in reference.get_links(['P67', 'P128']):
        range_ = link_.range
        data = get_base_table_data(range_)
        data.append(link_.description)
        if range_.view_name == 'file':  # pragma: no cover
            ext = data[3].replace('.', '')
            data.append(get_profile_image_table_link(range_, reference, ext, profile_image_id))
        data = add_edit_link(data, url_for('reference_link_update',
                                           link_id=link_.id,
                                           origin_id=reference.id))
        data = add_remove_link(data, range_.name, link_, reference, range_.table_name)
        tabs[range_.table_name].table.rows.append(data)
    reference.note = User.get_note(reference)
    return render_template('reference/view.html',
                           reference=reference,
                           tabs=tabs,
                           info=get_entity_data(reference),
                           profile_image_id=profile_image_id)


def save(form: Any,
         reference: Optional[Entity] = None,
         code: Optional[str] = None,
         origin: Optional[Entity] = None) -> str:
    g.cursor.execute('BEGIN')
    log_action = 'update'

    try:
        if not code and not reference:
            abort(400)  # pragma: no cover, either reference or code has to be provided
        elif not reference:
            log_action = 'insert'
            system_type = code.replace('_', ' ')  # type: ignore
            reference = Entity.insert('E31', form.name.data, system_type)
        reference.update(form)
        url = url_for('entity_view', id_=reference.id)
        if origin:
            link_id = reference.link('P67', origin)[0]
            url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
        if form.continue_.data == 'yes' and code:
            url = url_for('reference_insert', code=code)
        g.cursor.execute('COMMIT')
        logger.log_user(reference.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('reference_index')
    return url
