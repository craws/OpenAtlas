# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

from flask import render_template
from flask_login import current_user
from flask_babel import lazy_gettext as _

import openatlas
from openatlas import app, NodeMapper
from openatlas.util.util import required_group, sanitize, uc_first


@app.route('/hierarchy')
@required_group('readonly')
def hierarchy_index():
    nodes = OrderedDict()
    for id_, node in openatlas.nodes.items():
        if not node.root:
            nodes[node] = tree_select(node.name)
    return render_template('hierarchy/index.html', nodes=nodes)


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
