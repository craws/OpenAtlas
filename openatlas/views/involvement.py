# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import flash, render_template, url_for, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app, PropertyMapper
from openatlas.forms import DateForm, build_form, TableMultiField, TreeField
from openatlas.models.date import DateMapper
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.link import LinkMapper
from openatlas.models.linkProperty import LinkPropertyMapper
from openatlas.util.util import (required_group, truncate_string, append_node_data,
                                 build_delete_link, build_remove_link, get_base_table_data,
                                 uc_first, link)

# Todo: insert and continue


class ActorForm(DateForm):
    actor = TableMultiField(_('actor'), validators=[InputRequired()])
    involvement = TreeField()
    activity = SelectField(_('activity'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/involvement/insert/<int:origin_id>/<int:actor_id>', methods=['POST', 'GET'])
@app.route('/involvement/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def involvement_insert(origin_id, actor_id=None):
    origin = EntityMapper.get_by_id(origin_id)
    form = ActorForm()
    if origin.class_.code in ['E6', 'E7', 'E8', 'E12']:
        form.activity.choices = [('P11', openatlas.properties['P11'].name)]
        if origin.class_.code in ['E7', 'E8', 'E12']:
            form.activity.choices.append(('P14', openatlas.properties['P14'].name))
        if origin.class_.code == 'E8':
            form.activity.choices.append(('P22', openatlas.properties['P22'].name))
            form.activity.choices.append(('P23', openatlas.properties['P23'].name))
    if form.validate_on_submit():
        if origin.class_.code in ['E6', 'E7', 'E8', 'E12']:
            openatlas.get_cursor().execute('BEGIN')
            for actor_id in ast.literal_eval(form.actor.data):
                link_id = origin.link(form.activity.data, actor_id, form.description.data)
                DateMapper.save_link_dates(link_id, form)
                LinkPropertyMapper.insert(link_id, 'P2', form.involvement.data)
            openatlas.get_cursor().execute('COMMIT')
            flash(_('entity created'), 'info')
            return redirect(url_for('event_view', id_=origin.id) + '#tab-actor')
    if actor_id:
        form.actor.data = [actor_id]
        del form.insert_and_continue
    return render_template('involvement/insert.html', origin=origin, form=form)


@app.route('/involvement/update/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def involvement_update(id_, origin_id):
    origin = EntityMapper.get_by_id(origin_id)
    link_ = LinkMapper.get_by_id(id_)
    linked_object_id = link_.domain.id if link_.domain.id != origin.id else link_.range.id
    form = ActorForm()
    form.save.label.text = _('save')
    del form.actor, form.insert_and_continue
    if origin.class_.code in ['E6', 'E7', 'E8', 'E12']:
        form.activity.choices = [('P11', openatlas.properties['P11'].name)]
        if origin.class_.code in ['E7', 'E8', 'E12']:
            form.activity.choices.append(('P14', openatlas.properties['P14'].name))
        if origin.class_.code == 'E8':
            form.activity.choices.append(('P22', openatlas.properties['P22'].name))
            form.activity.choices.append(('P23', openatlas.properties['P23'].name))
    if form.validate_on_submit():
        openatlas.get_cursor().execute('BEGIN')
        domain = link_.domain
        range_ = link_.range
        link_.delete()
        link_id = domain.link(form.activity.data, range_, form.description.data)
        DateMapper.save_link_dates(link_id, form)
        LinkPropertyMapper.insert(link_id, 'P2', form.involvement.data)
        openatlas.get_cursor().execute('COMMIT')
        return redirect(url_for('event_view', id_=origin.id) + '#tab-actor')
    form.activity.data = link_.property.code
    form.description.data = link_.description
    if link_.type_id:
        form.involvement.data = openatlas.nodes[link_.type_id].id
    link_.set_dates()
    form.populate_dates(link_)
    return render_template(
        'involvement/update.html',
        origin=origin,
        form=form,
        linked_object=EntityMapper.get_by_id(linked_object_id))
