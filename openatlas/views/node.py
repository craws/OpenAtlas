# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict
from flask import render_template, flash, url_for, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app, NodeMapper
from openatlas.util.util import required_group, sanitize, uc_first


class NodeForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    inverse_test = StringField(uc_first(_('inverse')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('description')))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/node')
@required_group('readonly')
def node_index():
    nodes = {'system': OrderedDict(), 'custom': OrderedDict()}
    for id_, node in openatlas.nodes.items():
        if hasattr(node, 'extendable') and node.extendable and not node.root:
            type_ = 'system' if node.system else 'custom'
            nodes[type_][node] = tree_select(node.name)
    return render_template('node/index.html', nodes=nodes)


@app.route('/node/insert/<int:root_id>', methods=['POST'])
@required_group('editor')
def node_insert(root_id):
    root = openatlas.nodes[root_id]
    if not root.extendable:
        flash(_('error forbidden'), 'info')
        return redirect(url_for('node_index'))
    form = NodeForm()
    if not root.directional:
        del form.inverse_test
    if 'name_search' not in request.form and form.validate_on_submit():
        name = form.name.data + (form.inverse_text.data if hasattr(form, 'inverse_test') in form else '')
        openatlas.get_cursor().execute('BEGIN')
        node = NodeMapper.insert('E55', name, form.description.data)
        openatlas.get_cursor().execute('COMMIT')
        flash(_('entity created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('node_insert', node_id=root.id))
        return redirect(url_for('node_view', node_id=node.id))
    if 'name_search' in request.form:
        form.name.data = request.form['name_search']
    return render_template('node/insert.html', form=form, root=root)


@app.route('/node/update/<int:node_id>', methods=['POST', 'GET'])
@required_group('editor')
def node_update(node_id):
    openatlas.get_cursor().execute('BEGIN')
    openatlas.get_cursor().execute('COMMIT')
    return render_template('node/update.html')


@app.route('/node/view/<int:node_id>')
@required_group('editor')
def node_view(node_id):
    return render_template('node/view.html')


@app.route('/node/delete/<int:node_id>', methods=['POST', 'GET'])
@required_group('editor')
def node_delete(node_id):
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
        text += "text: '" + item.name + " " + str(item.count) + count_subs + "', 'id':'" + str(item.id) + "'"
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
