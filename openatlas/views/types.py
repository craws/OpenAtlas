# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import List, Union

from flask import abort, flash, g, render_template, request, session, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import (HiddenField, SelectMultipleField, StringField, SubmitField, TextAreaField,
                     widgets)
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import build_move_form, build_node_form
from openatlas.models.entity import Entity, EntityMapper
from openatlas.models.node import NodeMapper
from openatlas.util.table import Table
from openatlas.util.util import (get_entity_data, link, required_group, sanitize, truncate_string,
                                 uc_first)


class NodeForm(FlaskForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    name_inverse = StringField(_('inverse'))
    is_node_form = HiddenField()
    unit = StringField(_('unit'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/types')
@required_group('readonly')
def node_index() -> str:
    nodes: dict = {'system': {}, 'custom': {}, 'places': {}, 'value': {}}
    for id_, node in g.nodes.items():
        if node.root:
            continue
        type_ = 'custom'
        if node.class_.code == 'E53':
            type_ = 'places'
        elif node.system:
            type_ = 'system'
        elif node.value_type:
            type_ = 'value'
        nodes[type_][node] = tree_select(node.name)
    return render_template('types/index.html', nodes=nodes, placeholder=_('type to search'))


@app.route('/types/insert/<int:root_id>', methods=['GET', 'POST'])
@app.route('/types/insert/<int:root_id>/<int:super_id>', methods=['GET', 'POST'])
@required_group('editor')
def node_insert(root_id: int, super_id: int = None) -> Union[str, Response]:
    root = g.nodes[root_id]
    form = build_node_form(NodeForm, root)
    # Check if form is valid and if it wasn't a submit of the search form
    if 'name_search' not in request.form and form.validate_on_submit():
        return redirect(save(form, root=root))
    getattr(form, str(root.id)).label.text = 'super'
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
    if node.system or (root and root.locked):
        abort(403)
    form = build_node_form(NodeForm, node, request)
    if form.validate_on_submit():
        save(form, node)
        return redirect(url_for('node_view', id_=id_))
    getattr(form, str(root.id)).label.text = 'super'
    return render_template('types/update.html', node=node, root=root, form=form)


@app.route('/types/view/<int:id_>')
@required_group('readonly')
def node_view(id_: int) -> str:
    from openatlas.models.link import LinkMapper
    node = g.nodes[id_]
    root = g.nodes[node.root[-1]] if node.root else None
    super_ = g.nodes[node.root[0]] if node.root else None
    header = [_('name'), _('class'), _('info')]
    if root and root.value_type:  # pragma: no cover
        header = [_('name'), _('value'), _('class'), _('info')]
    tables = {'entities': Table(header)}
    for entity in node.get_linked_entities(['P2', 'P89'], inverse=True, nodes=True):
        # If it is a place location get the corresponding object
        entity = entity if node.class_.code == 'E55' else entity.get_linked_entity('P53', True)
        if entity:  # If not entity it is a place node, so do not add
            data = [link(entity)]
            if root and root.value_type:  # pragma: no cover
                data.append(format_number(entity.nodes[node]))
            data.append(g.classes[entity.class_.code].name)
            data.append(truncate_string(entity.description))
            tables['entities'].rows.append(data)
    tables['link_entities'] = Table([_('domain'), _('range')])
    for row in LinkMapper.get_entities_by_node(node):
        tables['link_entities'].rows.append([link(EntityMapper.get_by_id(row.domain_id)),
                                             link(EntityMapper.get_by_id(row.range_id))])
    tables['subs'] = Table([_('name'), _('count'), _('info')])
    for sub_id in node.subs:
        sub = g.nodes[sub_id]
        tables['subs'].rows.append([link(sub), sub.count, truncate_string(sub.description)])
    return render_template('types/view.html', node=node, super_=super_, tables=tables, root=root,
                           info=get_entity_data(node))


@app.route('/types/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_delete(id_: int) -> Response:
    node = g.nodes[id_]
    root = g.nodes[node.root[-1]] if node.root else None
    if node.system or node.subs or node.count or (root and root.locked):
        abort(403)
    node.delete()
    flash(_('entity deleted'), 'info')
    return redirect(url_for('node_view', id_=root.id) if root else url_for('node_index'))


class MoveForm(FlaskForm):
    is_node_form = HiddenField()
    checkbox_values = HiddenField()
    selection = SelectMultipleField('', [InputRequired()], coerce=int,
                                    option_widget=widgets.CheckboxInput(),
                                    widget=widgets.ListWidget(prefix_label=False))
    save = SubmitField()


@app.route('/types/move/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_move_entities(id_: int) -> Union[str, Response]:
    node = g.nodes[id_]
    root = g.nodes[node.root[-1]]
    if root.value_type:  # pragma: no cover
        abort(403)
    form = build_move_form(MoveForm, node)
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        NodeMapper.move_entities(node, getattr(form, str(root.id)).data, form.checkbox_values.data)
        g.cursor.execute('COMMIT')
        flash('Entities where updated', 'success')
        return redirect(url_for('node_index') + '#tab-' + str(root.id))
    form.save.label.text = uc_first(_('move'))
    getattr(form, str(root.id)).data = node.id
    return render_template('types/move.html', node=node, root=root, form=form)


def walk_tree(nodes: List[Entity]) -> str:
    """ Builds JSON for jsTree"""
    text = ''
    for id_ in nodes:
        item = g.nodes[id_]
        count_subs = ' (' + format_number(item.count_subs) + ')' if item.count_subs else ''
        text += "{href: '" + url_for('node_view', id_=item.id) + "',"
        text += "a_attr: { href: '" + url_for('node_view', id_=item.id) + "'}, "
        text += "text: '" + item.name.replace("'", "&apos;") + " "
        text += '<span style="font-weight:normal">' + format_number(item.count) + count_subs
        text += "', 'id':'" + str(item.id) + "'"
        if item.subs:
            text += ",'children' : ["
            for sub in item.subs:
                text += walk_tree([sub])
            text += "]"
        text += "},"
    return text


def tree_select(name: str) -> str:
    html = """
        <div id="{name}-tree"></div>
        <script>
            $(document).ready(function () {{
                $("#{name}-tree").jstree({{
                    "search": {{ "case_insensitive": true, "show_only_matches": true }},
                    "plugins" : ["core", "html_data", "search"],
                    "core":{{ "data":[{tree}] }}
                }});
                $("#{name}-tree").on("select_node.jstree", function (e, data) {{
                    document.location.href = data.node.original.href;
                }});
                $("#{name}-tree-search").keyup(function() {{
                    if (this.value.length >= {min_chars}) {{
                        $("#{name}-tree").jstree("search", $(this).val());
                    }}
                }});
            }});
        </script>""".format(min_chars=session['settings']['minimum_jstree_search'],
                            name=sanitize(name), tree=walk_tree(NodeMapper.get_nodes(name)))
    return html


def save(form, node=None, root=None):
    g.cursor.execute('BEGIN')
    try:
        if node:
            log_action = 'update'
            root = g.nodes[node.root[-1]] if node.root else None
            super_ = g.nodes[node.root[0]] if node.root else None
        else:
            log_action = 'insert'
            node = NodeMapper.insert(root.class_.code, form.name.data)
            super_ = 'new'
        new_super_id = getattr(form, str(root.id)).data
        new_super = g.nodes[int(new_super_id)] if new_super_id else g.nodes[root.id]
        if new_super.id == node.id:
            flash(_('error node self as super'), 'error')
            return
        if new_super.root and node.id in new_super.root:
            flash(_('error node sub as super'), 'error')
            return
        node.name = form.name.data
        if root.directional and form.name_inverse.data.strip():
            node.name += ' (' + form.name_inverse.data.strip() + ')'
        if not root.directional:
            node.name = node.name.replace('(', '').replace(')', '')
        node.description = form.description.data if form.description else form.unit.data
        node.update()

        # Update super if changed and node is not a root node
        if super_ and (super_ == 'new' or super_.id != new_super_id):
            property_code = 'P127' if node.class_.code == 'E55' else 'P89'
            node.delete_links(property_code)
            node.link(property_code, new_super)
        g.cursor.execute('COMMIT')
        url = url_for('node_view', id_=node.id)
        if form.continue_.data == 'yes':
            url = url_for('node_insert', root_id=root.id,
                          super_id=new_super_id if new_super_id else None)
        logger.log_user(node.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('node_index')
    return url
