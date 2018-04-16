# Created by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

from flask import abort, flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from openatlas import app, logger
from openatlas.forms.forms import build_node_form
from openatlas.models.entity import EntityMapper
from openatlas.models.node import NodeMapper
from openatlas.util.util import link, required_group, sanitize, truncate_string


class NodeForm(Form):
    name = StringField(_('name'), [DataRequired()])
    name_inverse = StringField(_('inverse'))
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))


@app.route('/types')
@required_group('readonly')
def node_index():
    nodes = {'system': OrderedDict(), 'custom': OrderedDict(), 'places': OrderedDict()}
    for id_, node in g.nodes.items():
        if not node.root:
            type_ = 'system' if node.system else 'custom'
            type_ = 'places' if node.class_.code == 'E53' else type_
            nodes[type_][node] = tree_select(node.name)
    return render_template('types/index.html', nodes=nodes)


@app.route('/types/insert/<int:root_id>', methods=['POST'])
@required_group('editor')
def node_insert(root_id):
    root = g.nodes[root_id]
    form = build_node_form(NodeForm, root)
    # Check if form is valid and if it wasn't a submit of the search form
    if 'name_search' not in request.form and form.validate_on_submit():
        name = form.name.data
        if hasattr(form, 'name_inverse') in form:
            name += ' (' + form.name_inverse.data + ')'
        node = save(form, root=root)
        if node:
            flash(_('entity created'), 'info')
            return redirect(url_for('node_view', id_=node.id))
    if 'name_search' in request.form:
        form.name.data = request.form['name_search']
    return render_template('types/insert.html', form=form, root=root)


@app.route('/types/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_update(id_):
    node = g.nodes[id_]
    if node.system:
        abort(403)
    form = build_node_form(NodeForm, node, request)
    root = g.nodes[node.root[-1]] if node.root else None
    if form.validate_on_submit():
        if save(form, node):
            flash(_('info update'), 'info')
            return redirect(url_for('node_view', id_=id_))
        return render_template('types/update.html', node=node, root=root, form=form)
    getattr(form, str(root.id)).label.text = 'super'
    return render_template('types/update.html', node=node, root=root, form=form)


@app.route('/types/view/<int:id_>')
@required_group('readonly')
def node_view(id_):
    from openatlas.models.linkProperty import LinkPropertyMapper
    node = g.nodes[id_]
    root = g.nodes[node.root[-1]] if node.root else None
    super_ = g.nodes[node.root[0]] if node.root else None
    tables = {'entities': {
        'id': 'entities', 'header': [_('name'), _('class'), _('info')], 'data': []}}
    for entity in node.get_linked_entities(['P2', 'P89'], True):
        # If it is a place location get the corresponding object
        entity = entity if node.class_.code == 'E55' else entity.get_linked_entity('P53', True)
        if entity:  # If not entity it is a place node, so do not add
            tables['entities']['data'].append([
                link(entity),
                g.classes[entity.class_.code].name,
                truncate_string(entity.description)])
    tables['link_entities'] = {
        'id': 'link_entities', 'header': [_('domain'), _('range')], 'data': []}
    for row in LinkPropertyMapper.get_entities_by_node(node):
        tables['link_entities']['data'].append([
            link(EntityMapper.get_by_id(row.domain_id)),
            link(EntityMapper.get_by_id(row.range_id))])
    tables['subs'] = {'id': 'subs', 'header': [_('name'), _('count'), _('info')], 'data': []}
    for sub_id in node.subs:
        sub = g.nodes[sub_id]
        tables['subs']['data'].append([link(sub), sub.count, truncate_string(sub.description)])
    return render_template('types/view.html', node=node, super_=super_, tables=tables, root=root)


@app.route('/types/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_delete(id_):
    node = g.nodes[id_]
    if node.system or node.subs or node.count:
        abort(403)
    g.cursor.execute('BEGIN')
    try:
        EntityMapper.delete(node.id)
        g.cursor.execute('COMMIT')
        flash(_('entity deleted'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    root = g.nodes[node.root[-1]] if node.root else None
    if root:
        return redirect(url_for('node_view', id_=root.id))
    return redirect(url_for('node_index'))


def walk_tree(param):
    text = ''
    for id_ in param if isinstance(param, list) else [param]:
        item = g.nodes[id_]
        count_subs = " (" + str(item.count_subs) + ")" if item.count_subs else ''
        text += "{href: '" + url_for('node_view', id_=item.id) + "',"
        text += "text: '" + item.name.replace("'", "&apos;") + " " + str(item.count) + count_subs
        text += "', 'id':'" + str(item.id) + "'"
        if item.subs:
            text += ",'children' : ["
            for sub in item.subs:
                text += walk_tree(sub)
            text += "]"
        text += "},"
    return text


def tree_select(name):
    html = """
        <div id="{name}-tree"></div>
        <script>
            $(document).ready(function () {{
                $("#{name}-tree").jstree({{
                    "search": {{ "case_insensitive": true, "show_only_matches": true }},
                    "plugins" : ["core", "html_data", "search"],
                    "core":{{ "data":[{tree}] }}
                }});
                $("#{name}-tree-search").keyup(function() {{
                    $("#{name}-tree").jstree("search", $(this).val());
                }});
                $("#{name}-tree").on("select_node.jstree", function (e, data) {{
                    document.location.href = data.node.original.href;
                }});
            }});
        </script>""".format(name=sanitize(name), tree=walk_tree(NodeMapper.get_nodes(name)))
    return html


def save(form, node=None, root=None):
    g.cursor.execute('BEGIN')
    try:
        if not node:
            node = NodeMapper.insert(root.class_.code, form.name.data)
            super_ = 'new'
        else:
            root = g.nodes[node.root[-1]] if node.root else None
            super_ = g.nodes[node.root[0]] if node.root else None
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
        node.description = form.description.data
        node.update()
        # update super if changed and node is not a root node
        if super_ and (super_ == 'new' or super_.id != new_super.id):
            property_code = 'P127' if node.class_.code == 'E55' else 'P89'
            node.delete_links(property_code)
            node.link(property_code, new_super.id)
        g.cursor.execute('COMMIT')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        return
    return node
