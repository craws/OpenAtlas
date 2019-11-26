# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import FieldList, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.date import DateForm
from openatlas.forms.forms import TableField, build_form, build_table_form
from openatlas.models.entity import Entity, EntityMapper
from openatlas.util.table import Table
from openatlas.util.util import (get_base_table_data, link, required_group, truncate_string,
                                 uc_first, was_modified)
from openatlas.views.reference import AddReferenceForm


class ActorForm(DateForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    alias = FieldList(StringField(''), description=_('tooltip alias'))
    residence = TableField(_('residence'))
    begins_in = TableField()
    ends_in = TableField()
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/actor')
@required_group('readonly')
def actor_index() -> str:
    table = Table(Table.HEADERS['actor'] + ['description'],
                  defs='[{className: "dt-body-right", targets: [2,3]}]')
    for actor in EntityMapper.get_by_codes('actor'):
        data = get_base_table_data(actor)
        data.append(truncate_string(actor.description))
        table.rows.append(data)
    return render_template('actor/index.html', table=table)


@app.route('/actor/insert/<code>', methods=['POST', 'GET'])
@app.route('/actor/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def actor_insert(code: str, origin_id: int = None) -> Union[str, Response]:
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    code_class = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, code_class[code])
    if form.validate_on_submit():
        return redirect(save(form, code=code, origin=origin))
    form.alias.append_entry('')
    if origin:
        del form.insert_and_continue
    if code == 'E21':
        form.begins_in.label.text = _('born in')
        form.ends_in.label.text = _('died in')
    return render_template('actor/insert.html', form=form, code=code, origin=origin)


@app.route('/actor/delete/<int:id_>')
@required_group('contributor')
def actor_delete(id_: int) -> Response:
    EntityMapper.delete(id_)
    logger.log_user(id_, 'delete')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('actor_index'))


@app.route('/actor/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def actor_update(id_: int) -> Union[str, Response]:
    actor = EntityMapper.get_by_id(id_, nodes=True, aliases=True, view_name='actor')
    code_class = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    form = build_form(ActorForm, code_class[actor.class_.code], actor, request)
    if form.validate_on_submit():
        if was_modified(form, actor):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(actor.id)['modifier'])
            return render_template('actor/update.html', form=form, actor=actor, modifier=modifier)
        save(form, actor)
        return redirect(url_for('entity_view', id_=id_))
    residence = actor.get_linked_entity('P74')
    form.residence.data = residence.get_linked_entity('P53', True).id if residence else ''
    first = actor.get_linked_entity('OA8')
    form.begins_in.data = first.get_linked_entity('P53', True).id if first else ''
    last = actor.get_linked_entity('OA9')
    form.ends_in.data = last.get_linked_entity('P53', True).id if last else ''
    for alias in actor.aliases.values():
        form.alias.append_entry(alias)
    form.alias.append_entry('')
    if actor.class_.code == 'E21':
        form.begins_in.label.text = _('born in')
        form.ends_in.label.text = _('died in')
    return render_template('actor/update.html', form=form, actor=actor)


@app.route('/actor/add/source/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def actor_add_source(id_: int) -> Union[str, Response]:
    actor = EntityMapper.get_by_id(id_, view_name='actor')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            actor.link_string('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-source')
    form = build_table_form('source', actor.get_linked_entities('P67', inverse=True))
    return render_template('add_source.html', entity=actor, form=form)


@app.route('/actor/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def actor_add_reference(id_: int) -> Union[str, Response]:
    actor = EntityMapper.get_by_id(id_, view_name='actor')
    form = AddReferenceForm()
    if form.validate_on_submit():
        actor.link_string('P67', form.reference.data, description=form.page.data, inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-reference')
    form.page.label.text = uc_first(_('page / link text'))
    return render_template('add_reference.html', entity=actor, form=form)


@app.route('/actor/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def actor_add_file(id_: int) -> Union[str, Response]:
    actor = EntityMapper.get_by_id(id_, view_name='actor')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            actor.link_string('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-file')
    form = build_table_form('file', actor.get_linked_entities('P67', inverse=True))
    return render_template('add_file.html', entity=actor, form=form)


def save(form: ActorForm, actor: Entity = None, code: str = '',
         origin: Entity = None) -> Union[str, Response]:
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if actor:
            actor.delete_links(['P74', 'OA8', 'OA9'])
        else:
            actor = EntityMapper.insert(code, form.name.data)
            log_action = 'insert'
        actor.name = form.name.data
        actor.description = form.description.data
        actor.set_dates(form)
        actor.update()
        actor.update_aliases(form)
        actor.save_nodes(form)
        url = url_for('entity_view', id_=actor.id)
        if form.residence.data:
            object_ = EntityMapper.get_by_id(form.residence.data, view_name='place')
            actor.link('P74', object_.get_linked_entity('P53'))
        if form.begins_in.data:
            object_ = EntityMapper.get_by_id(form.begins_in.data, view_name='place')
            actor.link('OA8', object_.get_linked_entity('P53'))
        if form.ends_in.data:
            object_ = EntityMapper.get_by_id(form.ends_in.data, view_name='place')
            actor.link('OA9', object_.get_linked_entity('P53'))

        if origin:
            if origin.view_name == 'reference':
                link_id = origin.link('P67', actor)[0]
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.view_name == 'source':
                origin.link('P67', actor)
                url = url_for('entity_view', id_=origin.id) + '#tab-actor'
            elif origin.view_name == 'event':
                link_id = origin.link('P11', actor)[0]
                url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
            elif origin.view_name == 'actor':
                link_id = origin.link('OA7', actor)[0]
                url = url_for('relation_update', id_=link_id, origin_id=origin.id)
        if form.continue_.data == 'yes' and code:
            url = url_for('actor_insert', code=code)
        logger.log_user(actor.id, log_action)
        g.cursor.execute('COMMIT')
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        return redirect(url_for('actor_index'))
    return url
