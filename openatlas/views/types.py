from typing import Dict, Optional, Union

from flask import abort, flash, g, render_template, request, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_move_form, build_node_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.util.display import (add_remove_link, get_base_table_data, get_entity_data,
                                    get_profile_image_table_link, link, tree_select)
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import required_group


@app.route('/types')
@required_group('readonly')
def node_index() -> str:
    nodes: Dict[str, Dict[Entity, str]] = {'standard': {}, 'custom': {}, 'places': {}, 'value': {}}
    for id_, node in g.nodes.items():
        if node.root:
            continue
        type_ = 'custom'
        if node.class_.code == 'E53':
            type_ = 'places'
        elif node.standard:
            type_ = 'standard'
        elif node.value_type:
            type_ = 'value'
        nodes[type_][node] = tree_select(node.name)
    return render_template('types/index.html', nodes=nodes, placeholder=_('type to search'))


@app.route('/types/insert/<int:root_id>', methods=['GET', 'POST'])
@app.route('/types/insert/<int:root_id>/<int:super_id>', methods=['GET', 'POST'])
@required_group('editor')
def node_insert(root_id: int, super_id: Optional[int] = None) -> Union[str, Response]:
    root = g.nodes[root_id]
    form = build_node_form(root=root)
    # Check if form is valid and if it wasn't a submit of the search form
    if 'name_search' not in request.form and form.validate_on_submit():
        return redirect(save(form, root=root))
    if super_id:
        getattr(form, str(root.id)).data = super_id if super_id != root.id else None
    if 'name_search' in request.form:
        form.name.data = request.form['name_search']
    return render_template('types/insert.html', form=form, root=root)


@app.route('/types/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_update(id_: int) -> Union[str, Response]:
    node = g.nodes[id_]
    root = g.nodes[node.root[-1]] if node.root else None
    if node.standard or (root and root.locked):
        abort(403)
    form = build_node_form(node=node)
    if form.validate_on_submit():
        save(form, node)
        return redirect(url_for('entity_view', id_=id_))
    return render_template('types/update.html', node=node, root=root, form=form)


@app.route('/types/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_delete(id_: int) -> Response:
    node = g.nodes[id_]
    root = g.nodes[node.root[-1]] if node.root else None
    if node.standard or node.subs or node.count or (root and root.locked):
        abort(403)
    node.delete()
    flash(_('entity deleted'), 'info')
    return redirect(url_for('entity_view', id_=root.id) if root else url_for('node_index'))


@app.route('/types/move/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_move_entities(id_: int) -> Union[str, Response]:
    node = g.nodes[id_]
    root = g.nodes[node.root[-1]]
    if node.class_.code == 'E53':
        tab_hash = '#menu-tab-places_collapse-'
    elif root.standard:
        tab_hash = '#menu-tab-standard_collapse-'
    elif node.value_type:  # pragma: no cover
        tab_hash = '#menu-tab-value_collapse-'
    else:
        tab_hash = '#menu-tab-custom_collapse-'
    if root.value_type:  # pragma: no cover
        abort(403)
    form = build_move_form(node)
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        Node.move_entities(node, getattr(form, str(root.id)).data, form.checkbox_values.data)
        g.cursor.execute('COMMIT')
        flash(_('Entities were updated'), 'success')
        return redirect(url_for('node_index') + tab_hash + str(root.id))
    getattr(form, str(root.id)).data = node.id
    return render_template('types/move.html', node=node, root=root, form=form)


def node_view(node: Node) -> str:
    root = g.nodes[node.root[-1]] if node.root else None
    super_ = g.nodes[node.root[0]] if node.root else None
    tabs = {name: Tab(name, origin=node) for name in ['info', 'subs', 'entities', 'file']}
    if root and root.value_type:  # pragma: no cover
        tabs['entities'].table.header = [_('name'), _('value'), _('class'), _('info')]
    for entity in node.get_linked_entities(['P2', 'P89'], inverse=True, nodes=True):
        if entity.class_.code == 'E32':  # Don't add reference systems themselves
            continue  # pragma: no cover
        if node.class_.code == 'E53':  # pragma: no cover
            object_ = entity.get_linked_entity('P53', inverse=True)
            if not object_:  # If it's a location show the object, continue otherwise
                continue
            entity = object_
        data = [link(entity)]
        if root and root.value_type:  # pragma: no cover
            data.append(format_number(entity.nodes[node]))
        data.append(g.classes[entity.class_.code].name)
        data.append(entity.description)
        tabs['entities'].table.rows.append(data)
    profile_image_id = node.get_profile_image_id()
    for link_ in node.get_links('P67', inverse=True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':  # pragma: no cover
            extension = data[3]
            data.append(get_profile_image_table_link(domain, node, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        data = add_remove_link(data, domain.name, link_, node, domain.view_name)
        tabs[domain.view_name].table.rows.append(data)
    for sub_id in node.subs:
        sub = g.nodes[sub_id]
        tabs['subs'].table.rows.append([link(sub), sub.count, sub.description])
    if not tabs['entities'].table.rows:  # If no entities available get links with this type_id
        tabs['entities'].table = Table([_('domain'), _('range')])
        for row in Link.get_entities_by_node(node):
            tabs['entities'].table.rows.append([link(Entity.get_by_id(row.domain_id)),
                                                link(Entity.get_by_id(row.range_id))])
    return render_template('types/view.html',
                           entity=node,
                           super_=super_,
                           tabs=tabs,
                           root=root,
                           info=get_entity_data(node),
                           profile_image_id=profile_image_id)


def save(form: FlaskForm, node=None, root: Optional[Node] = None) -> Optional[str]:  # type: ignore
    g.cursor.execute('BEGIN')
    super_ = None
    log_action = 'insert'
    try:
        if node:
            log_action = 'update'
            root = g.nodes[node.root[-1]] if node.root else None
            super_ = g.nodes[node.root[0]] if node.root else None
        elif root:
            node = Entity.insert(root.class_.code, form.name.data)
            super_ = 'new'
        else:
            abort(404)  # pragma: no cover, either node or root has to be provided
        new_super_id = getattr(form, str(root.id)).data  # type: ignore
        new_super = g.nodes[int(new_super_id)] if new_super_id else g.nodes[root.id]  # type: ignore
        if new_super.id == node.id:
            flash(_('error node self as super'), 'error')
            return None
        if new_super.root and node.id in new_super.root:
            flash(_('error node sub as super'), 'error')
            return None
        node.description = form.description.data
        node.name = form.name.data
        if root and root.directional and form.name_inverse.data.strip():
            node.name += ' (' + form.name_inverse.data.strip() + ')'
        if root and not root.directional:
            node.name = node.name.replace('(', '').replace(')', '')
        node.update()

        # Update super if changed and node is not a root node
        if super_ and (super_ == 'new' or super_.id != new_super_id):
            property_code = 'P127' if node.class_.code == 'E55' else 'P89'
            node.delete_links([property_code])
            node.link(property_code, new_super)
        g.cursor.execute('COMMIT')
        url = url_for('entity_view', id_=node.id)
        if hasattr(form, 'continue_') and form.continue_.data == 'yes':
            url = url_for('node_insert', root_id=root.id,  # type: ignore
                          super_id=new_super_id if new_super_id else None)
        logger.log_user(node.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('node_index')
    return url
