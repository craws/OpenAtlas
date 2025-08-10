import ast

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.util import link, required_group
from openatlas.forms.display import display_form
from openatlas.forms.form import (
    get_add_reference_form, get_manager, get_table_form)
from openatlas.models.entity import Entity, Link
from openatlas.models.search import get_subunits_without_super


@app.route('/link/delete/<int:id_>/<int:origin_id>', methods=['GET', 'POST'])
@required_group('contributor')
def link_delete(id_: int, origin_id: int) -> Response:
    Link.delete_(id_)
    flash(_('link removed'), 'info')
    return redirect(url_for('view', id_=origin_id))


@app.route('/link/insert/<int:id_>/<view>', methods=['GET', 'POST'])
@required_group('contributor')
def link_insert(id_: int, view: str) -> str | Response:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string('P67', request.form['checkbox_values'])
        return redirect(f"{url_for('view', id_=entity.id)}#tab-{view}")
    return render_template(
        'content.html',
        content=get_table_form(
            g.class_groups[view]['classes'],
            [e.id for e in entity.get_linked_entities('P67')]),
        title=_(entity.class_.group['name']),
        crumbs=[link(entity, index=True), entity, _('link')])

@app.route('/link/insert2/<int:id_>/<relation_name>', methods=['GET', 'POST'])
@required_group('contributor')
def link_insert2(id_: int, relation_name: str) -> str | Response:
    entity = Entity.get_by_id(id_)
    relation = entity.class_.relations[relation_name]
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                relation['property'],
                request.form['checkbox_values'],
                inverse=relation['inverse'])
        return redirect(f"{url_for('view', id_=entity.id)}#tab-{relation_name}")
    return render_template(
        'content.html',
        content=get_table_form(
            relation['class'],
            [e.id for e in entity.get_linked_entities(
                relation['property'],
                inverse=relation['inverse'])]),
        title=_(entity.class_.group['name']),
        crumbs=[link(entity, index=True), entity, _('link')])


@app.route('/link/update/<int:id_>/<int:origin_id>', methods=['GET', 'POST'])
@required_group('contributor')
def link_update(id_: int, origin_id: int) -> str | Response:
    link_ = Link.get_by_id(id_)
    domain = Entity.get_by_id(link_.domain.id)
    range_ = Entity.get_by_id(link_.range.id)
    origin = Entity.get_by_id(origin_id)
    if 'reference' in [domain.class_.group['name'], range_.class_.group['name']]:
        return reference_link_update(link_, origin)
    manager_name = 'involvement'
    tab = 'actor' if origin.class_.group['name'] == 'event' else 'event'
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
        except Exception as e:  # pragma: no cover
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
            link(origin, index=True),
            origin,
            domain if origin.id != domain.id else range_,
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
            manager.update_link()
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


def reference_link_update(link_: Link, origin: Entity) -> str | Response:
    origin = Entity.get_by_id(origin.id)
    form = get_add_reference_form('reference')
    del form.reference
    if form.validate_on_submit():
        link_.description = form.page.data
        link_.update()
        flash(_('info update'), 'info')
        tab = link_.range.class_.group['name'] if origin.class_.group['name'] == 'reference' \
            else 'reference'
        return redirect(f"{url_for('view', id_=origin.id)}#tab-{tab}")
    form.save.label.text = _('save')
    form.page.data = link_.description
    if link_.domain.class_.name == 'external_reference':
        form.page.label.text = _('link text')
    return render_template(
        'content.html',
        content=display_form(form),
        crumbs=[
            link(origin, index=True),
            origin,
            link_.domain if link_.domain.id != origin.id else link_.range,
            _('edit')])


@app.route('/reference/add/<int:id_>/<view>', methods=['GET', 'POST'])
@required_group('contributor')
def reference_add(id_: int, view: str) -> str | Response:
    reference = Entity.get_by_id(id_)
    form = get_add_reference_form(view)
    if form.validate_on_submit():
        ids = ast.literal_eval(getattr(form, view).data)
        ids = ids if isinstance(ids, list) else [int(ids)]
        reference.link('P67', Entity.get_by_ids(ids), form.page.data)
        return redirect(f"{url_for('view', id_=reference.id)}#tab-{view}")
    if reference.class_.name == 'external_reference':
        form.page.label.text = _('link text')
    return render_template(
        'content.html',
        content=display_form(form),
        title=_('reference'),
        crumbs=[link(reference, index=True), reference, _('link')])


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
        content=get_table_form(
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
        content=get_table_form(
            ['file'],
            [e.id for e in entity.get_linked_entities('P67', inverse=True)]),
        entity=entity,
        title=entity.name,
        crumbs=[link(entity, index=True), entity, f"{_('link')} {_('file')}"])


@app.route('/entity/add/source/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def entity_add_source(id_: int) -> str | Response:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                'P67',
                request.form['checkbox_values'],
                inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-source")
    return render_template(
        'content.html',
        content=get_table_form(
            ['source'],
            [e.id for e in entity.get_linked_entities('P67', inverse=True)]),
        title=entity.name,
        crumbs=[
            link(entity, index=True),
            entity,
            _('link') + ' ' + _('source')])


@app.route('/entity/add/reference/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def entity_add_reference(id_: int) -> str | Response:
    entity = Entity.get_by_id(id_)
    form = get_add_reference_form('reference')
    if form.validate_on_submit():
        entity.link_string(
            'P67',
            form.reference.data,
            description=form.page.data,
            inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-reference")
    form.page.label.text = _('page / link text')
    return render_template(
        'content.html',
        content=display_form(form),
        entity=entity,
        crumbs=[
            link(entity, index=True),
            entity,
            _('link') + ' ' + _('reference')])
