from typing import Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.display import (link)
from openatlas.util.util import required_group, was_modified


@app.route('/insert/<code>', methods=['POST', 'GET'])
@app.route('/insert/<code>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def insert(code: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    form = build_form(g.classes[code].name.lower().replace(' ', '_'), code=code, origin=origin)
    if form.validate_on_submit():
        return redirect(save(form, code=code, origin=origin))
    form.alias.append_entry('')
    if origin and origin.system_type == 'place':
        form.residence.data = origin_id
    view_name = 'actor'
    crumb = [[_(view_name), url_for('index', class_=view_name)], '+ ' + g.classes[code].name]
    if origin:
        crumb = [[_(origin.view_name), url_for('index', class_=origin.view_name)],
                 origin, '+ ' + g.classes[code].name]
    return render_template('entity/insert.html',
                           form=form,
                           crumb=crumb,
                           code=code,
                           origin=origin,
                           view_name=view_name)


@app.route('/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def update(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_, nodes=True, aliases=True)
    form = build_form(g.classes[entity.class_.code].name.lower().replace(' ', '_'), entity)
    if form.validate_on_submit():
        if was_modified(form, entity):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(entity.id)['modifier'])
            return render_template('entity/update.html', form=form, entity=entity, modifier=modifier)
        save(form, entity)
        return redirect(url_for('entity_view', id_=id_))
    residence = entity.get_linked_entity('P74')
    form.residence.data = residence.get_linked_entity_safe('P53', True).id if residence else ''
    first = entity.get_linked_entity('OA8')
    form.begins_in.data = first.get_linked_entity_safe('P53', True).id if first else ''
    last = entity.get_linked_entity('OA9')
    form.ends_in.data = last.get_linked_entity_safe('P53', True).id if last else ''
    for alias in entity.aliases.values():
        form.alias.append_entry(alias)
    form.alias.append_entry('')
    return render_template('entity/update.html', form=form, entity=entity)


def save(form: FlaskForm,
         entity: Optional[Entity] = None,
         code: str = '',
         origin: Optional[Entity] = None) -> Union[str, Response]:
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if entity:
            entity.delete_links(['P74', 'OA8', 'OA9'])
        else:
            entity = Entity.insert(code, form.name.data)
            log_action = 'insert'
        entity.update(form)
        ReferenceSystem.update_links(form, entity)
        if form.residence.data:
            object_ = Entity.get_by_id(form.residence.data, view_name='place')
            entity.link('P74', object_.get_linked_entity_safe('P53'))
        if form.begins_in.data:
            object_ = Entity.get_by_id(form.begins_in.data, view_name='place')
            entity.link('OA8', object_.get_linked_entity_safe('P53'))
        if form.ends_in.data:
            object_ = Entity.get_by_id(form.ends_in.data, view_name='place')
            entity.link('OA9', object_.get_linked_entity_safe('P53'))

        url = url_for('entity_view', id_=entity.id)
        if origin:
            if origin.view_name == 'reference':
                link_id = origin.link('P67', entity)[0]
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
            elif origin.view_name in ['source', 'file']:
                origin.link('P67', entity)
                url = url_for('entity_view', id_=origin.id) + '#tab-' + entity.view_name
            elif origin.view_name == 'event':
                link_id = origin.link('P11', entity)[0]
                url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
            elif origin.view_name == entity.view_name:
                link_id = origin.link('OA7', entity)[0]
                url = url_for('relation_update', id_=link_id, origin_id=origin.id)
            elif origin.view_name == 'place':
                url = url_for('entity_view', id_=origin.id) + '#tab-' + entity.view_name
        if hasattr(form, 'continue_') and form.continue_.data == 'yes':
            url = url_for('entity_insert', code=code)
        logger.log_user(entity.id, log_action)
        g.cursor.execute('COMMIT')
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        return redirect(url_for('entity_index', class_=entity.view_name))
    return url
