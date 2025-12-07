from flask import abort, flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import BooleanField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table, entity_table
from openatlas.display.util import (
    get_entities_linked_to_type_recursive, link, required_group)
from openatlas.display.util2 import uc_first
from openatlas.forms.field import SubmitField
from openatlas.forms.form import move_form
from openatlas.models.entity import Entity, Link


@app.route('/type/delete_recursive/<int:id_>', methods=['GET', 'POST'])
@required_group('editor')
def type_delete_recursive(id_: int) -> str | Response:
    class DeleteRecursiveTypesForm(FlaskForm):
        confirm_delete = BooleanField(
            _("I'm sure to delete this type, it's subs and links"),
            default=False,
            validators=[InputRequired()])
        save = SubmitField(_('delete types and remove all links'))

    type_ = g.types[id_]
    root = g.types[type_.root[0]] if type_.root else None
    root_name = root.name if root else type_.name
    if type_.category == 'system' or \
            type_.category in ('standard', 'place') and not root:
        abort(403)
    form = DeleteRecursiveTypesForm()
    if form.validate_on_submit() and form.confirm_delete.data:
        for sub_id in type_.get_sub_ids_recursive():
            g.types[sub_id].delete()
        type_.delete()
        flash(_('types deleted'))
        g.logger.log_user(id_, 'Recursive type delete')
        return redirect(
            url_for('view', id_=root.id) if root
            else url_for('index', group='type'))
    tabs = {
        'info': Tab(
            'info',
            content=_(
                'Warning: this type has subs and/or links to entities '
                '(see tabs). Please check if you want to delete these subs '
                'and links too.'),
            form=form),
        'subs': Tab('subs', entity=type_),
        'entities': Tab('entities', entity=type_)}
    for sub_id in type_.get_sub_ids_recursive():
        sub = g.types[sub_id]
        tabs['subs'].table.rows.append([link(sub), sub.count, sub.description])
    if root_name in app.config['PROPERTY_TYPES']:
        for row in Link.get_links_by_type_recursive(type_, []):
            tabs['entities'].table.columns = [_('domain'), _('range')]
            tabs['entities'].table.rows.append([
                link(Entity.get_by_id(row['domain_id'])),
                link(Entity.get_by_id(row['range_id']))])
    else:
        for item in get_entities_linked_to_type_recursive(type_.id, []):
            data = [link(item), item.class_.label, item.description]
            tabs['entities'].table.rows.append(data)
    crumbs = [[_('type'), url_for('index', group='type')]]
    if root:
        crumbs += [g.types[type_id] for type_id in type_.root]
    crumbs += [type_, _('delete')]
    return render_template('tabs.html', tabs=tabs, crumbs=crumbs)


@app.route('/type/change/<int:id_>', methods=['GET', 'POST'])
@required_group('editor')
def change_type(id_: int) -> str | Response:
    type_ = g.types[id_]
    root = g.types[type_.root[0]]
    if root.category in ['system', 'value']:
        abort(403)
    form = move_form(type_)
    type_field = getattr(form, str(root.id))
    if form.validate_on_submit():
        type_.change_type(type_field.data, form.checkbox_values.data)
        flash(_('Entities were updated'), 'success')
        return redirect(
            f"{url_for('index', group='type')}"
            f"#menu-tab-{type_.category}_collapse-{root.id}")
    return render_template(
        'type/move.html',
        table=Table(
            ['#', _('selection')],
            rows=[[item, item.label.text] for item in form.selection]),
        root=root,
        form=form,
        entity=type_,
        crumbs=[link(type_, index=True), root, type_, _('move entities')])


@app.route('/type/untyped/<int:id_>')
@required_group('editor')
def show_untyped_entities(id_: int) -> str:
    type_ = g.types[id_]
    table = entity_table(
        type_.get_untyped(),
        columns=['name', 'class', 'begin', 'end', 'description'])
    tabs = {
        'untyped': Tab(
            'untyped',
            _('untyped entities'),
            table=table,
            content=_('no entries') if not table.rows else '')}
    return render_template(
        'tabs.html',
        tabs=tabs,
        entity=type_,
        crumbs=[link(type_, index=True), link(type_), _('untyped entities')])


@app.route('/type/set-selectable/<int:id_>')
@required_group('editor')
def type_set_selectable(id_: int) -> Response:
    g.types[id_].set_selectable()
    return redirect(url_for('view', id_=id_))


@app.route('/type/unset-selectable/<int:id_>')
@required_group('editor')
def type_unset_selectable(id_: int) -> Response:
    g.types[id_].unset_selectable()
    return redirect(url_for('view', id_=id_))


@app.route('/type/multiple_linked/<int:id_>')
@required_group('editor')
def show_multiple_linked_entities(id_: int) -> str:
    type_ = g.types[id_]
    linked_entity_ids = set()
    already_tracked_ids = set()
    multiple_linked_entities = []
    for entity in get_entities_linked_to_type_recursive(id_, []):
        if entity.id in linked_entity_ids \
                and entity.id not in already_tracked_ids:
            multiple_linked_entities.append(entity)
            already_tracked_ids.add(entity.id)
        linked_entity_ids.add(entity.id)
    table = entity_table(
        multiple_linked_entities,
        columns=['name', 'class', 'begin', 'end', 'description'])
    tabs = {
        'untyped': Tab(
            'multiple_linked',
            _('multiple linked entities'),
            table=table,
            content=uc_first(_('no entries')) if not table.rows else '')}
    return render_template(
        'tabs.html',
        tabs=tabs,
        entity=type_,
        crumbs=[
            link(type_, index=True),
            link(type_),
            _('multiple linked entities')])
