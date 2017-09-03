# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template
from flask_login import current_user
from flask_babel import lazy_gettext as _

import openatlas
from openatlas import app
from openatlas.util.util import required_group, uc_first


@app.route('/hierarchy')
@required_group('readonly')
def hierarchy_index():
    tabs = {'system ul': '', 'system div': '', 'custom ul': '', 'custom div': ''}
    for root, hierarchy in openatlas.nodes:
        for item in openatlas.nodes[root]:
            node = item['node']
            tabs[hierarchy + ' ul'] += '<li><a href="#tab' + str(node.id) + '">' + node.name + '</a></li>'
            tabs[hierarchy + ' div'] += ''
            tabs[hierarchy + ' div'] += '''
                <div id="tab{node_id}"><p><strong>{node_name}</strong></p>
                    <div style="float:left;margin-right:3em;">
                    <div class="button-bar" style="margin-bottom:0.5em;">
                        <form method="post" action="/admin/hierarchy/insert/id/{node_id}" style="margin-bottom:1em;">
                            <input class="tree-filter" id="{node_id}-tree-search" placeholder="Filter" style="width:8em;" name="name" />
                            <input type="hidden" name="mode" value="insert" />
                            <button value="insert" name="add-hierarchy-submit" type="submit">+</button>
                '''.format(node_id=str(node.id), node_name=node.name)
            if not node.system and current_user.group in ['admin', 'manager']:
                tabs[hierarchy + ' div'] += ' <a href="/admin/hierarchy/update-hierarchy/id/' + node.id + '">'
                # tabs[hierarchy + ' div'] += uc_first(_('edit')) + '</a>' + link(node, 'delete')
            tabs[hierarchy + ' div'] += '</form></div>' + item['tree'] + '</div>'
            tabs[hierarchy + ' div'] += '<div style="float:left;">'
            if node.forms:
                tabs[hierarchy + ' div'] += '<p style="margin-top:0">' + uc_first(_('forms')) + ':</strong> '
                tabs[hierarchy + ' div'] += ' ,'.join(node.forms) + '</p>'
            if node.description:
                tabs[hierarchy + ' div'] += '<p style="width:500px;">' + node.description + '</p>'
            tabs[hierarchy + ' div'] += '</div></div>'
    return render_template('hierarchy/index.html', tabs=tabs)
