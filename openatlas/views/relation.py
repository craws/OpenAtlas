import ast
from typing import Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms.form import get_entity_form
from openatlas.forms.process import process_form_dates
from openatlas.forms.util import get_link_type
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.util import required_group, uc_first


@app.route('/relation/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def relation_insert(origin_id: int) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id)
    manager = get_entity_form('actor_actor_relation', origin=origin)
    manager.form.relation_origin_id.data = origin.id
    if manager.form.validate_on_submit():
        Transaction.begin()
        try:
            for actor in Entity.get_by_ids(
                    ast.literal_eval(manager.form.actor.data)):
                if manager.form.inverse.data:
                    link_ = Link.get_by_id(
                        actor.link(
                            'OA7',
                            origin,
                            manager.form.description.data)[0])
                else:
                    link_ = Link.get_by_id(
                        origin.link(
                            'OA7',
                            actor,
                            manager.form.description.data)[0])
                link_.set_dates(process_form_dates(manager.form))
                link_.type = get_link_type(manager.form)
                link_.update()
            Transaction.commit()
            flash(_('entity created'), 'info')
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        if hasattr(manager.form, 'continue_') \
                and manager.form.continue_.data == 'yes':
            return redirect(url_for('relation_insert', origin_id=origin_id))
        return redirect(f"{url_for('view', id_=origin.id)}#tab-relation")
    return render_template(
        'display_form.html',
        form=manager.form,
        title=_('relation'),
        crumbs=[
            [_('actor'), url_for('index', view='actor')],
            origin,
            f"+ {uc_first(_('relation'))}"])


@app.route('/involvement/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def involvement_insert(origin_id: int) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id)
    manager = get_entity_form('involvement', origin=origin)
    manager.form.activity.choices = [('P11', g.properties['P11'].name_inverse)]
    if origin.class_.name in ['acquisition', 'activity', 'production']:
        manager.form.activity.choices.append(
            ('P14', g.properties['P14'].name_inverse))
        if origin.class_.name == 'acquisition':
            manager.form.activity.choices.append((
                'P22',
                g.properties['P22'].name_inverse))
            manager.form.activity.choices.append((
                'P23',
                g.properties['P23'].name_inverse))
    if manager.form.validate_on_submit():
        Transaction.begin()
        try:
            if origin.class_.view == 'event':
                for actor in Entity.get_by_ids(
                        ast.literal_eval(manager.form.actor.data)):
                    link_ = Link.get_by_id(
                        origin.link(
                            manager.form.activity.data,
                            actor,
                            manager.form.description.data)[0])
                    link_.set_dates(process_form_dates(manager.form))
                    link_.type = get_link_type(manager.form)
                    link_.update()
            else:
                for event in Entity.get_by_ids(
                        ast.literal_eval(manager.form.event.data)):
                    link_ = Link.get_by_id(
                        event.link(
                            manager.form.activity.data,
                            origin,
                            manager.form.description.data)[0])
                    link_.set_dates(process_form_dates(manager.form))
                    link_.type = get_link_type(manager.form)
                    link_.update()
            Transaction.commit()
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        if hasattr(manager.form, 'continue_') \
                and manager.form.continue_.data == 'yes':
            return redirect(url_for('involvement_insert', origin_id=origin_id))
        return redirect(
            f"{url_for('view', id_=origin.id)}"
            f"#tab-{'actor' if origin.class_.view == 'event' else 'event'}")
    return render_template(
        'display_form.html',
        form=manager.form,
        crumbs=[
            [_(origin.class_.view), url_for('index', view=origin.class_.view)],
            origin,
            _('involvement')])
