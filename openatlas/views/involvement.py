import ast
from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, SelectField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.date import DateForm
from openatlas.forms.util import build_form2, get_link_type
from openatlas.forms.field import TableMultiField
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.util import required_group


class ActorForm(DateForm):
    actor = TableMultiField(_('actor'), [InputRequired()])
    event = TableMultiField(_('event'), [InputRequired()])
    activity = SelectField(_('activity'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/involvement/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def involvement_insert(origin_id: int) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id)
    form = build_form2(ActorForm, 'Involvement')
    if origin.view_name == 'event':
        del form.event
    else:
        del form.actor
    form.activity.choices = [('P11', g.properties['P11'].name_inverse)]
    if origin.class_.code in ['E7', 'E8']:
        form.activity.choices.append(('P14', g.properties['P14'].name_inverse))
    if origin.class_.code == 'E8':
        form.activity.choices.append(('P22', g.properties['P22'].name_inverse))
        form.activity.choices.append(('P23', g.properties['P23'].name_inverse))
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            if origin.view_name == 'event':
                for actor in Entity.get_by_ids(ast.literal_eval(form.actor.data)):
                    link_ = Link.get_by_id(origin.link(form.activity.data,
                                                       actor,
                                                       form.description.data)[0])
                    link_.set_dates(form)
                    link_.type = get_link_type(form)
                    link_.update()
            else:
                for event in Entity.get_by_ids(ast.literal_eval(form.event.data)):
                    link_ = Link.get_by_id(event.link(form.activity.data,
                                                      origin,
                                                      form.description.data)[0])
                    link_.set_dates(form)
                    link_.type = get_link_type(form)
                    link_.update()
            g.cursor.execute('COMMIT')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        if form.continue_.data == 'yes':
            return redirect(url_for('involvement_insert', origin_id=origin_id))
        tab = 'actor' if origin.view_name == 'event' else 'event'
        return redirect(url_for('entity_view', id_=origin.id) + '#tab-' + tab)
    return render_template('involvement/insert.html', origin=origin, form=form)


@app.route('/involvement/update/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def involvement_update(id_: int, origin_id: int) -> Union[str, Response]:
    link_ = Link.get_by_id(id_)
    form = build_form2(ActorForm, 'Involvement', link_, request)
    del form.actor, form.event, form.insert_and_continue
    form.activity.choices = [('P11', g.properties['P11'].name)]
    event = Entity.get_by_id(link_.domain.id, view_name='event')
    actor = Entity.get_by_id(link_.range.id, view_name='actor')
    origin = event if origin_id == event.id else actor
    if event.class_.code in ['E7', 'E8']:
        form.activity.choices.append(('P14', g.properties['P14'].name))
    if event.class_.code == 'E8':
        form.activity.choices.append(('P22', g.properties['P22'].name))
        form.activity.choices.append(('P23', g.properties['P23'].name))
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            link_.delete()
            link_ = Link.get_by_id(event.link(form.activity.data, actor, form.description.data)[0])
            link_.set_dates(form)
            link_.type = get_link_type(form)
            link_.update()
            g.cursor.execute('COMMIT')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        tab = 'actor' if origin.view_name == 'event' else 'event'
        return redirect(url_for('entity_view', id_=origin.id) + '#tab-' + tab)
    form.save.label.text = _('save')
    form.activity.data = link_.property.code
    form.description.data = link_.description
    form.populate_dates(link_)
    return render_template('involvement/update.html',
                           origin=origin,
                           form=form,
                           linked_object=event if origin_id != event.id else actor)
