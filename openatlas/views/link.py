from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.forms.field import TableField
from openatlas.forms.form import get_manager, get_table_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.util import display_form, required_group, uc_first


class AddReferenceForm(FlaskForm):
    reference = TableField(_('reference'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


@app.route('/link/delete/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def link_delete(id_: int, origin_id: int) -> Response:
    Link.delete_(id_)
    flash(_('link removed'), 'info')
    return redirect(url_for('view', id_=origin_id))


@app.route('/link/insert/<int:id_>/<view>', methods=['POST', 'GET'])
@required_group('contributor')
def link_insert(id_: int, view: str) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    property_code = 'P67'
    inverse = False
    if entity.class_.view == 'actor' and view == 'artifact':
        property_code = 'P52'
        inverse = True
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                property_code,
                request.form['checkbox_values'],
                inverse=inverse)
        return redirect(f"{url_for('view', id_=entity.id)}#tab-{view}")
    if entity.class_.view == 'actor' and view == 'artifact':
        excluded = \
            Entity.get_by_link_property(property_code, 'artifact') + \
            Entity.get_by_link_property(property_code, 'human_remains')
    else:
        excluded = entity.get_linked_entities(property_code, inverse=inverse)
    return render_template(
        'content.html',
        content=get_table_form(view, excluded),
        title=_(entity.class_.view),
        crumbs=[
            [_(entity.class_.view), url_for('index', view=entity.class_.view)],
            entity,
            _('link')])


@app.route('/link/update/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def link_update(id_: int, origin_id: int) -> Union[str, Response]:
    link_ = Link.get_by_id(id_)
    domain = Entity.get_by_id(link_.domain.id)
    range_ = Entity.get_by_id(link_.range.id)
    origin = Entity.get_by_id(origin_id)
    if 'reference' in [domain.class_.view, range_.class_.view]:
        return reference_link_update(link_, origin)
    manager_name = 'involvement'
    tab = 'actor' if origin.class_.view == 'event' else 'event'
    if link_.property.code == 'OA7':
        manager_name = 'actor_relation'
        tab = 'relation'
    elif link_.property.code == 'P107':
        manager_name = 'actor_function'
        tab = f"member{'-of' if origin.id == range_.id else ''}"
    manager = get_manager(manager_name, origin=origin, link_=link_)
    if manager.form.validate_on_submit():
        Transaction.begin()
        try:
            manager.process_link_form()
            manager.link_.update()
            Transaction.commit()
        except Exception as e:
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(f"{url_for('view', id_=origin.id)}#tab-{tab}")
    if not manager.form.errors:
        manager.populate_update()
    return render_template(
        'content.html',
        content=display_form(manager.form),
        crumbs=[
            [_(origin.class_.view), url_for('index', view=origin.class_.view)],
            origin,
            domain if origin.id != domain.id else range_,
            _('edit')])


@app.route('/insert/relation/<type_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def insert_relation(type_: str, origin_id: int) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id)
    manager = get_manager(
        'actor_function' if type_.startswith('member') else type_,
        origin=origin)
    if manager.form.validate_on_submit():
        Transaction.begin()
        try:
            manager.process_form()
            manager.update_link()
            Transaction.commit()
        except Exception as e:
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        if hasattr(manager.form, 'continue_') \
                and manager.form.continue_.data == 'yes':
            return redirect(
                url_for('insert_relation', type_=type_, origin_id=origin_id))
        tabs = {
            'actor_relation': 'relation',
            'event': 'event',
            'involvement':
                'actor' if origin.class_.view == 'event' else 'event',
            'member': 'member',
            'membership': 'member-of'}
        return redirect(f"{url_for('view', id_=origin.id)}#tab-{tabs[type_]}")
    return render_template(
        'content.html',
        content=display_form(manager.form),
        origin=origin,
        crumbs=[
            [_(origin.class_.view), url_for('index', view=origin.class_.view)],
            origin,
            _(type_)])


def reference_link_update(link_: Link, origin: Entity) -> Union[str, Response]:
    origin = Entity.get_by_id(origin.id)
    form = AddReferenceForm()
    del form.reference
    if form.validate_on_submit():
        link_.description = form.page.data
        link_.update()
        flash(_('info update'), 'info')
        tab = link_.range.class_.view if origin.class_.view == 'reference' \
            else 'reference'
        return redirect(f"{url_for('view', id_=origin.id)}#tab-{tab}")
    form.save.label.text = _('save')
    form.page.data = link_.description
    if link_.domain.class_.name == 'external_reference':
        form.page.label.text = uc_first(_('link text'))
    return render_template(
        'content.html',
        content=display_form(form),
        crumbs=[
            [_(origin.class_.view),
             url_for('index', view=origin.class_.view)],
            origin,
            link_.domain if link_.domain.id != origin.id else
            link_.range,
            _('edit')])
