# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict
from flask import render_template, flash, url_for, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app, NodeMapper
from openatlas.util.util import required_group, sanitize, uc_first, link, truncate_string


class NodeForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    name_inverse = StringField(uc_first(_('inverse')))
    description = TextAreaField(uc_first(_('description')))
    save = SubmitField(_('insert'))


@app.route('/node')
@required_group('readonly')
def node_index():
    nodes = {'system': OrderedDict(), 'custom': OrderedDict()}
    for id_, node in openatlas.nodes.items():
        if not node.root:
            type_ = 'system' if node.system else 'custom'
            nodes[type_][node] = tree_select(node.name)
    return render_template('node/index.html', nodes=nodes)


@app.route('/node/insert/<int:root_id>', methods=['POST'])
@required_group('editor')
def node_insert(root_id):
    root = openatlas.nodes[root_id]
    form = NodeForm()
    if not root.directional:
        del form.name_inverse
    if 'name_search' not in request.form and form.validate_on_submit():
        name = form.name.data
        if hasattr(form, 'name_inverse') in form:
            name += ' (' + form.name_inverse.data + ')'
        openatlas.get_cursor().execute('BEGIN')
        node = NodeMapper.insert('E55', name, None, form.description.data)
        openatlas.get_cursor().execute('COMMIT')
        flash(_('entity created'), 'info')
        return redirect(url_for('node_view', node_id=node.id))
    if 'name_search' in request.form:
        form.name.data = request.form['name_search']
    return render_template('node/insert.html', form=form, root=root)


@app.route('/node/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_update(id_):
    node = openatlas.nodes[id_]
    openatlas.get_cursor().execute('BEGIN')
    openatlas.get_cursor().execute('COMMIT')
    return render_template('node/update.html', node=node)


@app.route('/node/view/<int:id_>')
@required_group('readonly')
def node_view(id_):
    node = openatlas.nodes[id_]
    super_ = openatlas.nodes[node.root[0]] if node.root else None
    tables = {'entities': {
        'name': 'entities',
        'header': [_('name'), _('class'), _('info')],
        'data': []}}
    for entity in node.get_linked_entities('P2', True):
        tables['entities']['data'].append([
            link(entity),
            openatlas.classes[entity.class_.id].name,
            truncate_string(entity.description)])
    tables['subs'] = {
        'name': 'subs',
        'header': [_('name'), _('count'), _('info')],
        'data': []}
    for sub_id in node.subs:
        sub = openatlas.nodes[sub_id]
        tables['subs']['data'].append([
            link(sub),
            sub.count,
            truncate_string(sub.description)])
    return render_template('node/view.html', node=node, super_=super_, tables=tables)


@app.route('/node/delete/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def node_delete(id_):
    node = openatlas.nodes[id_]
    openatlas.get_cursor().execute('BEGIN')
    openatlas.get_cursor().execute('COMMIT')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('node_index'))


def walk_tree(param):
    items = param if isinstance(param, list) else [param]
    text = ''
    for id_ in items:
        item = openatlas.nodes[id_]
        count_subs = " (" + str(item.count_subs) + ")" if item.count_subs else ''
        text += "{href: '/node/view/" + str(item.id) + "',"
        text += "text: '" + item.name + " " + str(item.count) + count_subs
        text += "', 'id':'" + str(item.id) + "'"
        if item.subs:
            text += ",'children' : ["
            for sub in item.subs:
                text += walk_tree(sub)
            text += "]"
        text += "},"
    return text


def tree_select(name):
    tree = "'core':{'data':[" + walk_tree(NodeMapper.get_nodes(name)) + "]}"
    name = sanitize(name)
    html = '<div id="' + name + '-tree"></div>'
    html += '<script>'
    html += '    $(document).ready(function () {'
    html += '        $("#' + name + '-tree").jstree({'
    html += '            "search": {"case_insensitive": true, "show_only_matches": true},'
    html += '            "plugins" : ["core", "html_data", "search"],' + tree + '});'
    html += '        $("#' + name + '-tree-search").keyup(function() {'
    html += '            $("#' + name + '-tree").jstree("search", $(this).val());'
    html += '        });'
    html += '        $("#' + name + '-tree").on("select_node.jstree", '
    html += '           function (e, data) { document.location.href = data.node.original.href; })'
    html += '    });'
    html += '</script>'
    return html
