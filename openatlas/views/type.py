from typing import Any

from flask import abort, flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import BooleanField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    get_chart_data, get_entities_linked_to_type_recursive, link,
    required_group)
from openatlas.display.util2 import manual, sanitize
from openatlas.forms.field import SubmitField
from openatlas.forms.form import get_move_form
from openatlas.models.entity import Entity, Link


def walk_tree(types: list[int]) -> list[dict[str, Any]]:
    items = []
    for id_ in types:
        item = g.types[id_]
        count_subs = f' ({format_number(item.count_subs)})' \
            if item.count_subs else ''
        name = item.name.replace("'", "&apos;")
        if item.selectable:
            text = f'{name} {format_number(item.count)}{count_subs}'
        else:
            text = f'<span class="text-muted">{name}{count_subs}</span>'
        items.append({
            'id': item.id,
            'href': url_for('view', id_=item.id),
            'a_attr': {'href': url_for('view', id_=item.id)},
            'text': text,
            'children': walk_tree(item.subs)})
    return items


@app.route('/type')
@required_group('readonly')
def type_index() -> str:
    types: dict[str, dict[Entity, str]] = {
        'standard': {},
        'custom': {},
        'place': {},
        'value': {},
        'system': {}}
    for type_ in [type_ for type_ in g.types.values() if not type_.root]:
        if type_.category in types:
            type_.chart_data = get_chart_data(type_)
            types[type_.category][type_] = render_template(
                'forms/tree_select_item.html',
                name=sanitize(type_.name, 'ascii'),
                data=walk_tree(type_.subs))
            for link_ in type_.get_links('P67', inverse=True):
                if link_.domain.class_.view == 'reference_system':
                    type_.reference_systems.append(link_)
    return render_template(
        'type/index.html',
        buttons=[manual('entity/type')],
        types=types,
        title=_('type'),
        crumbs=[_('type')])


@app.route('/type/delete/<int:id_>')
@required_group('editor')
def type_delete(id_: int) -> Response:
    type_ = g.types[id_]
    if type_.category == 'system' or type_.subs or type_.count:
        abort(403)
    root = g.types[type_.root[0]] if type_.root else None  # Before deleting
    type_.delete()
    flash(_('entity deleted'), 'info')
    return redirect(
        url_for('view', id_=root.id) if root else url_for('type_index'))


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
        flash(_('types deleted'), 'info')
        g.logger.log_user(id_, 'Recursive type delete')
        return redirect(
            url_for('view', id_=root.id) if root else url_for('type_index'))
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
            tabs['entities'].table.header = [_('domain'), _('range')]
            tabs['entities'].table.rows.append([
                link(Entity.get_by_id(row['domain_id'])),
                link(Entity.get_by_id(row['range_id']))])
    else:
        for item in get_entities_linked_to_type_recursive(type_.id, []):
            data = [link(item), item.class_.label, item.description]
            tabs['entities'].table.rows.append(data)
    crumbs = [[_('type'), url_for('type_index')]]
    if root:
        crumbs += [g.types[type_id] for type_id in type_.root]
    crumbs += [type_, _('delete')]
    return render_template('tabs.html', tabs=tabs, crumbs=crumbs)


@app.route('/type/move/<int:id_>', methods=['GET', 'POST'])
@required_group('editor')
def type_move_entities(id_: int) -> str | Response:
    type_ = g.types[id_]
    root = g.types[type_.root[0]]
    if root.category in ['system', 'value']:
        abort(403)
    form = get_move_form(type_)
    if form.validate_on_submit():
        Transaction.begin()
        type_.move_entities(
            getattr(form, str(root.id)).data,
            form.checkbox_values.data)
        Transaction.commit()
        flash(_('Entities were updated'), 'success')
        return redirect(
            f"{url_for('type_index')}"
            f"#menu-tab-{type_.category}_collapse-{root.id}")
    getattr(form, str(root.id)).data = type_.id
    return render_template(
        'type/move.html',
        table=Table(
            header=['#', _('selection')],
            rows=[[item, item.label.text] for item in form.selection]),
        root=root,
        form=form,
        entity=type_,
        crumbs=[link(type_, index=True), root, type_, _('move entities')])


@app.route('/type/untyped/<int:id_>')
@required_group('editor')
def show_untyped_entities(id_: int) -> str:
    type_ = g.types[id_]
    table = Table(['name', 'class', 'first', 'last', 'description'])
    for entity in type_.get_untyped():
        table.rows.append([
            link(entity),
            entity.class_.label,
            entity.first,
            entity.last,
            entity.description])
    return render_template(
        'content.html',
        content=table.display(),
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
    linked_entities = set()
    multiple_linked_entities = []
    for entity in get_entities_linked_to_type_recursive(id_, []):
        if entity.id in linked_entities:
            multiple_linked_entities.append(entity)
        linked_entities.add(entity.id)
    table = Table(['name', 'class', 'first', 'last', 'description'])
    for entity in multiple_linked_entities:
        table.rows.append([
            link(entity),
            entity.class_.label,
            entity.first,
            entity.last,
            entity.description])
    type_ = g.types[id_]
    return render_template(
        'content.html',
        content=table.display(),
        entity=g.types[id_],
        crumbs=[link(type_, index=True), link(type_), _('untyped entities')])
