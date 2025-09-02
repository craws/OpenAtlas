import ast

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.util import link, required_group
from openatlas.display.util2 import uc_first
from openatlas.forms.display import display_form
from openatlas.forms.form import (
    get_manager, link_form, link_update_form, table_form)
from openatlas.forms.process import process_dates
from openatlas.models.entity import Entity, Link
from openatlas.models.search import get_subunits_without_super

_('page')  # This translation is needed for reference table views


@app.route('/link/delete/<int:id_>/<int:origin_id>', methods=['GET', 'POST'])
@required_group('contributor')
def link_delete(id_: int, origin_id: int) -> Response:
    Link.delete_(id_)
    flash(_('link removed'), 'info')
    return redirect(url_for('view', id_=origin_id))


@app.route(
    '/link/insert/<int:origin_id>/<relation_name>',
    methods=['GET', 'POST'])
@required_group('contributor')
def link_insert(origin_id: int, relation_name: str) -> str | Response:
    origin = Entity.get_by_id(origin_id)
    relation = origin.class_.relations[relation_name]
    if request.method == 'POST':
        if request.form['checkbox_values']:
            # Todo: properties can be multiple?
            origin.link_string(
                relation['properties'][0],
                request.form['checkbox_values'],
                inverse=relation['inverse'])
        return redirect(
            f"{url_for('view', id_=origin.id)}#tab-" +
            relation_name.replace('_', '-'))
    # Todo: properties can be multiple?
    content = table_form(
        relation['classes'],
        [e.id for e in origin.get_linked_entities(
            relation['properties'][0],
            inverse=relation['inverse'])])
    return render_template(
        'content.html',
        content=content,
        title=_(origin.class_.group['name']),
        crumbs=[link(origin, index=True), origin, _('link')])


@app.route(
    '/link/insert_detail/<int:origin_id>/<relation_name>',
    methods=['GET', 'POST'])
@required_group('contributor')
def link_insert_detail(origin_id: int, relation_name: str) -> str | Response:
    origin = Entity.get_by_id(origin_id)
    relation = origin.class_.relations[relation_name]
    form = link_form(origin, relation)
    if form.validate_on_submit():
        ids = ast.literal_eval(getattr(form, relation_name).data)
        ids = ids if isinstance(ids, list) else [int(ids)]
        type_id = None
        if 'type' in relation:
            hierarchy = Entity.get_hierarchy(relation['type'])
            type_id = getattr(form, str(hierarchy.id)).data or None
        origin.link(
            relation['properties'][0],
            Entity.get_by_ids(ids),
            form.description.data if 'description' in form else None,
            relation['inverse'],
            type_id,
            dates=process_dates(form))
        return redirect(
            f"{url_for('view', id_=origin.id)}#tab-" +
            relation_name.replace('_', '-'))
    return render_template(
        'content.html',
        content=display_form(form),
        title=_(origin.class_.group['name']),
        crumbs=[
            link(origin, index=True),
            origin,
            '+ ' + uc_first(relation['label'])])


@app.route(
    '/link/update/<int:id_>/<int:origin_id>/<relation>',
    methods=['GET', 'POST'])
@required_group('contributor')
def link_update(id_: int, origin_id: int, relation: str) -> str | Response:
    link_ = Link.get_by_id(id_)
    domain = Entity.get_by_id(link_.domain.id)
    range_ = Entity.get_by_id(link_.range.id)
    origin = domain if origin_id == domain.id else range_
    target = range_ if origin_id == domain.id else domain
    relation = origin.class_.relations[relation]
    form = link_update_form(link_, relation)
    origin_url = url_for('view', id_=origin.id) + \
        f"#tab-{relation['name'].replace('_', '-')}"
    if form.validate_on_submit():
        data = {
            'description': form.description.data
            if hasattr(form, 'description') else None}
        if 'type' in relation:
            hierarchy = Entity.get_hierarchy(relation['type'])
            data['type_id'] = getattr(form, str(hierarchy.id)).data or None
        data.update(process_dates(form))
        try:
            link_.update(data)
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(origin_url)
    return render_template(
        'content.html',
        content=display_form(form),
        crumbs=[
            link(origin, index=True),
            link(origin.name, origin_url),
            target,
            _('edit')])


@app.route('/insert/relation/<type_>/<int:origin_id>', methods=['GET', 'POST'])
@required_group('contributor')
def insert_relation(type_: str, origin_id: int) -> str | Response:
    origin = Entity.get_by_id(origin_id)
    manager = get_manager(
        'actor_function' if type_.startswith('member') else type_,
        origin=origin)
    if manager.form.validate_on_submit():
        Transaction.begin()
        try:
            manager.process_form()
            # manager.update_link()
            Transaction.commit()
        except Exception as e:  # pragma: no cover
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
                'actor' if origin.class_.group['name'] == 'event' else 'event',
            'member': 'member',
            'membership': 'member-of'}
        return redirect(f"{url_for('view', id_=origin.id)}#tab-{tabs[type_]}")
    return render_template(
        'content.html',
        content=display_form(manager.form),
        origin=origin,
        crumbs=[link(origin, index=True), origin, _(type_)])


@app.route('/add/subunit/<int:super_id>', methods=['GET', 'POST'])
@required_group('contributor')
def add_subunit(super_id: int) -> str | Response:
    super_ = Entity.get_by_id(super_id)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            super_.link_string('P46', request.form['checkbox_values'])
        return redirect(f"{url_for('view', id_=super_.id)}#tab-artifact")
    classes = []
    if super_.class_.name != 'human_remains':
        classes.append('artifact')
    if super_.class_.name != 'artifact':
        classes.append('human_remains')
    return render_template(
        'content.html',
        content=table_form(
            classes,
            [super_.id] + get_subunits_without_super(classes)),
        entity=super_,
        title=super_.name,
        crumbs=[link(super_, index=True), super_, _('add subunit')])


@app.route('/entity/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def entity_add_file(id_: int) -> str | Response:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                'P67',
                request.form['checkbox_values'], inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-file")
    return render_template(
        'content.html',
        content=table_form(
            ['file'],
            [e.id for e in entity.get_linked_entities('P67', inverse=True)]),
        entity=entity,
        title=entity.name,
        crumbs=[link(entity, index=True), entity, f"{_('link')} {_('file')}"])
