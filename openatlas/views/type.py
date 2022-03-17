from typing import Any, Union

from flask import abort, flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.forms.form import build_move_form
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.util.table import Table
from openatlas.util.util import link, required_group, sanitize


def walk_tree(types: list[int]) -> list[dict[str, Any]]:
    items = []
    for id_ in types:
        item = g.types[id_]
        count_subs = f' ({format_number(item.count_subs)})' \
            if item.count_subs else ''
        items.append({
            'id': item.id,
            'href': url_for('view', id_=item.id),
            'a_attr': {'href': url_for('view', id_=item.id)},
            'text':
                item.name.replace("'", "&apos;") +
                f' {format_number(item.count)}{count_subs}',
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
        if type_.category not in types:
            continue # pragma: no cover, remove after anthropology features
        types[type_.category][type_] = render_template(
            'forms/tree_select_item.html',
            name=sanitize(type_.name),
            data=walk_tree(Type.get_types(type_.name)))
    return render_template(
        'type/index.html',
        types=types,
        title=_('types'),
        crumbs=[_('types')])


@app.route('/type/delete/<int:id_>', methods=['POST', 'GET'])
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


@app.route('/type/move/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def type_move_entities(id_: int) -> Union[str, Response]:
    type_ = g.types[id_]
    root = g.types[type_.root[0]]
    if root.category == 'value':
        abort(403)  # pragma: no cover
    form = build_move_form(type_)
    if form.validate_on_submit():
        Transaction.begin()
        Type.move_entities(
            type_,
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
        crumbs=[
            [_('types'), url_for('type_index')],
            root,
            type_,
            _('move entities')])


@app.route('/type/untyped/<int:id_>')
@required_group('editor')
def show_untyped_entities(id_: int) -> str:
    hierarchy = g.types[id_]
    table = Table(['name', 'class', 'first', 'last', 'description'])
    for entity in Type.get_untyped(hierarchy.id):
        table.rows.append([
            link(entity),
            entity.class_.label,
            entity.first,
            entity.last,
            entity.description])
    return render_template(
        'table.html',
        entity=hierarchy,
        table=table,
        crumbs=[
            [_('types'),
             url_for('type_index')],
            link(hierarchy),
            _('untyped entities')])
