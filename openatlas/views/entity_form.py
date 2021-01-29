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
from openatlas.util.display import link, uc_first
from openatlas.util.util import required_group, was_modified


@app.route('/insert/<class_>', methods=['POST', 'GET'])
@app.route('/insert/<class_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def insert(class_: str, origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    if class_ in g.classes:
        form = build_form(g.classes[class_].name.lower().replace(' ', '_'),
                          code=class_,
                          origin=origin)
    else:
        form = build_form(class_, origin=origin)
    if form.validate_on_submit():
        return redirect(save(form, class_=class_, origin=origin))
    if hasattr(form, 'alias'):
        form.alias.append_entry('')
    if origin and origin.system_type == 'place':
        form.residence.data = origin_id
    view_name = app.config['CODE_CLASS'][class_] if class_ in g.classes else _(class_)
    crumb = [[_(view_name), url_for('index', class_=view_name)],
             '+ ' + (g.classes[class_].name if class_ in g.classes else uc_first(_(class_)))]
    if origin:
        crumb = [[_(origin.view_name), url_for('index', class_=origin.view_name)],
                 origin, '+ ' + uc_first(_(view_name))]
    return render_template('entity/insert.html',
                           form=form,
                           crumb=crumb,
                           class_=class_,
                           origin=origin,
                           view_name=view_name)


@app.route('/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def update(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_, nodes=True, aliases=True)
    if entity.view_name == 'actor':
        form = build_form(g.classes[entity.class_.code].name.lower().replace(' ', '_'), entity)
    else:
        form = build_form(entity.view_name, entity)
    if form.validate_on_submit():
        if was_modified(form, entity):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(entity.id)['modifier'])
            return render_template('entity/update.html',
                                   form=form,
                                   entity=entity,
                                   modifier=modifier)
        return redirect(save(form, entity))
    populate_form(form, entity)
    return render_template('entity/update.html',
                           form=form,
                           entity=entity,
                           crumb=[[_(entity.view_name), url_for('index', class_=entity.view_name)],
                                  link(entity),
                                  _('edit')])


def populate_form(form: FlaskForm, entity: Entity, ) -> None:
    if entity.view_name == 'actor':
        residence = entity.get_linked_entity('P74')
        form.residence.data = residence.get_linked_entity_safe('P53', True).id if residence else ''
        first = entity.get_linked_entity('OA8')
        form.begins_in.data = first.get_linked_entity_safe('P53', True).id if first else ''
        last = entity.get_linked_entity('OA9')
        form.ends_in.data = last.get_linked_entity_safe('P53', True).id if last else ''
        for alias in entity.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')
    elif entity.view_name == 'source':
        form.information_carrier.data = [item.id for item in
                                         entity.get_linked_entities('P128', inverse=True)]


def save(form: FlaskForm,
         entity: Optional[Entity] = None,
         class_: Optional[str] = '',
         origin: Optional[Entity] = None) -> Union[str, Response]:
    g.cursor.execute('BEGIN')
    action = 'update'
    try:
        if not entity:
            action = 'insert'
            if class_ == 'source':
                entity = Entity.insert('E33', form.name.data, 'source content')
            else:
                entity = Entity.insert(class_, form.name.data)
        entity.update(form)
        update_links(entity, form, action)
        url = get_redirect_url(form, entity, class_, origin)
        logger.log_user(entity.id, action)
        g.cursor.execute('COMMIT')
        flash(_('entity created') if action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        if action == 'update':
            url = url_for('insert', class_=class_, origin_id=origin.id if origin else None)
        else:
            url = url_for(url_for('entity_index', class_=entity.view_name))
    return url


def update_links(entity: Entity, form, action: str) -> None:
    # Todo: it would be better to only save changes and not delete/recreate all links
    if entity.view_name == 'actor':
        if action == 'update':
            entity.delete_links(['P74', 'OA8', 'OA9'])
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
    elif entity.view_name == 'source':
        if action == 'update':
            entity.delete_links(['P128'], inverse=True)
        if form.information_carrier.data:
            entity.link_string('P128', form.information_carrier.data, inverse=True)


def get_redirect_url(form: FlaskForm,
                     entity: Entity,
                     class_: Optional[str] = '',
                     origin: Optional[Entity] = None) -> str:
    url = url_for('entity_view', id_=entity.id)
    if origin:
        url = url_for('entity_view', id_=origin.id) + '#tab-' + entity.view_name
        if origin.view_name == 'reference':
            link_id = origin.link('P67', entity)[0]
            url = url_for('reference_link_update', link_id=link_id, origin_id=origin.id)
        elif origin.view_name in ['source', 'file']:
            origin.link('P67', entity)
        elif entity.view_name == 'source' and origin.class_.code != 'E84':
            entity.link('P67', origin)
        elif origin.view_name == 'event':
            link_id = origin.link('P11', entity)[0]
            url = url_for('involvement_update', id_=link_id, origin_id=origin.id)
        elif origin.view_name == entity.view_name:
            link_id = origin.link('OA7', entity)[0]
            url = url_for('relation_update', id_=link_id, origin_id=origin.id)
    if hasattr(form, 'continue_') and form.continue_.data == 'yes':
        url = url_for('insert', class_=class_, origin_id=origin.id if origin else None)
    return url
