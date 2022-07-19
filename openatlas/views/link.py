from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms.field import TableField
from openatlas.forms.form import get_entity_form, get_table_form
from openatlas.forms.process import process_form_dates
from openatlas.forms.util import get_link_type
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.util import required_group, uc_first


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
        'form.html',
        form=get_table_form(view, excluded),
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
    if 'event' in [domain.class_.view, range_.class_.view]:
        return involvement_update(link_, origin)
    if domain.class_.view == 'actor' and range_.class_.view == 'actor':
        return relation_update(link_, domain, range_, origin)
    abort(403)  # pragma: no cover


def involvement_update(link_: Link, origin: Entity) -> Union[str, Response]:
    manager = get_entity_form('involvement', origin=origin, link_=link_)
    event = Entity.get_by_id(link_.domain.id)
    actor = Entity.get_by_id(link_.range.id)
    origin = event if origin.id == event.id else actor
    if manager.form.validate_on_submit():
        Transaction.begin()
        try:
            link_.delete()
            link_ = Link.get_by_id(
                event.link(
                    manager.form.activity.data,
                    actor,
                    manager.form.description.data)[0])
            link_.set_dates(process_form_dates(manager.form))
            link_.type = get_link_type(manager.form)
            link_.update()
            Transaction.commit()
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(
            f"{url_for('view', id_=origin.id)}"
            f"#tab-{'actor' if origin.class_.view == 'event' else 'event'}")
    manager.populate_update()
    return render_template(
        'display_form.html',
        origin=origin,
        form=manager.form,
        crumbs=[
            [_(origin.class_.view), url_for('index', view=origin.class_.view)],
            origin,
            event if origin.id != event.id else actor,
            _('edit')])


def relation_update(
        link_: Link,
        domain: Entity,
        range_: Entity,
        origin: Entity) -> Union[str, Response]:
    origin = range_ if origin.id == range_.id else domain
    related = range_ if origin.id == domain.id else domain
    manager = get_entity_form(
        'actor_actor_relation',
        origin=origin,
        link_=link_)
    if manager.form.validate_on_submit():
        Transaction.begin()
        try:
            link_.delete()
            if manager.form.inverse.data:
                link_ = Link.get_by_id(
                    related.link(
                        'OA7',
                        origin,
                        manager.form.description.data)[0])
            else:
                link_ = Link.get_by_id(
                    origin.link(
                        'OA7',
                        related,
                        manager.form.description.data)[0])
            link_.set_dates(process_form_dates(manager.form))
            link_.type = get_link_type(manager.form)
            link_.update()
            Transaction.commit()
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(f"{url_for('view', id_=origin.id)}#tab-relation")
    manager.populate_update()
    return render_template(
        'display_form.html',
        form=manager.form,
        title=_('relation'),
        crumbs=[
            [_('actor'), url_for('index', view='actor')],
            origin,
            related,
            _('edit')])


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
        'display_form.html',
        form=form,
        crumbs=[
            [_(origin.class_.view),
             url_for('index', view=origin.class_.view)],
            origin,
            link_.domain if link_.domain.id != origin.id else
            link_.range,
            _('edit')])
