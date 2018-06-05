# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from openatlas import app, logger
from openatlas.forms.forms import build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import (build_table_form, display_remove_link, get_base_table_data,
                                 get_entity_data, get_view_name, is_authorized, link,
                                 required_group, truncate_string, uc_first, was_modified)


class SourceForm(Form):
    name = StringField(_('name'), [DataRequired()])
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/source')
@required_group('readonly')
def source_index():
    table = {'id': 'source', 'header': app.config['TABLE_HEADERS']['source'], 'data': []}
    for source in EntityMapper.get_by_codes('source'):
        data = get_base_table_data(source)
        table['data'].append(data)
    return render_template('source/index.html', table=table)


@app.route('/source/insert/<int:origin_id>', methods=['POST', 'GET'])
@app.route('/source/insert', methods=['POST', 'GET'])
@required_group('editor')
def source_insert(origin_id=None):
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(SourceForm, 'Source')
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        return redirect(save(form, origin=origin))
    return render_template('source/insert.html', form=form, origin=origin)


@app.route('/source/view/<int:id_>/<int:unlink_id>')
@app.route('/source/view/<int:id_>')
@required_group('readonly')
def source_view(id_, unlink_id=None):
    source = EntityMapper.get_by_id(id_)
    if unlink_id:
        LinkMapper.delete_by_id(unlink_id)
        flash(_('link removed'), 'info')
    tables = {
        'info': get_entity_data(source),
        'text': {'id': 'translation', 'data': [], 'header': ['text', 'type', 'content']},
        'file': {'id': 'files', 'data': [], 'header': app.config['TABLE_HEADERS']['file']},
        'reference': {
            'id': 'source', 'data': [],
            'header': app.config['TABLE_HEADERS']['reference'] + ['page']}}
    for text in source.get_linked_entities('P73'):
        tables['text']['data'].append([
            link(text),
            next(iter(text.nodes)).name if text.nodes else '',
            truncate_string(text.description)])
    for name in ['actor', 'event', 'place', 'feature', 'stratigraphic-unit', 'find']:
        tables[name] = {'id': name, 'header': app.config['TABLE_HEADERS'][name], 'data': []}
    for link_ in source.get_links('P67'):
        data = get_base_table_data(link_.range)
        view_name = get_view_name(link_.range)
        table_name = view_name
        if view_name == 'place':
            table_name = link_.range.system_type.replace(' ', '-')
        if is_authorized('editor'):
            unlink = url_for('source_view', id_=source.id, unlink_id=link_.id) + '#tab-' + \
                     table_name
            data.append(display_remove_link(unlink, link_.range.name))
        tables[table_name]['data'].append(data)
    for link_ in source.get_links(['P67', 'P128'], True):
        data = get_base_table_data(link_.domain)
        view_name = get_view_name(link_.domain)
        if view_name not in ['file']:
            data.append(link_.description)
            if is_authorized('editor'):
                update_url = url_for('reference_link_update', link_id=link_.id, origin_id=source.id)
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('editor'):
            unlink = url_for('source_view', id_=source.id, unlink_id=link_.id) + '#tab-' + view_name
            data.append(display_remove_link(unlink, link_.domain.name))
        tables[view_name]['data'].append(data)
    return render_template('source/view.html', source=source, tables=tables)


@app.route('/source/add/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def source_add(origin_id):
    """ Link an entity to source coming from the entity."""
    origin = EntityMapper.get_by_id(origin_id)
    if request.method == 'POST':
        g.cursor.execute('BEGIN')
        try:
            for value in request.form.getlist('values'):
                LinkMapper.insert(int(value), 'P67', origin.id)
            g.cursor.execute('COMMIT')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for(get_view_name(origin) + '_view', id_=origin.id) + '#tab-source')
    form = build_table_form('source', origin.get_linked_entities('P67', True))
    return render_template('source/add.html', origin=origin, form=form)


@app.route('/source/add2/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('editor')
def source_add2(id_, class_name):
    """ Link an entity to source coming from the source"""
    source = EntityMapper.get_by_id(id_)
    if request.method == 'POST':
        for value in request.form.getlist('values'):
            source.link('P67', int(value))
        return redirect(url_for('source_view', id_=source.id) + '#tab-' + class_name)
    form = build_table_form(class_name, source.get_linked_entities('P67'))
    return render_template('source/add2.html', source=source, class_name=class_name, form=form)


@app.route('/source/delete/<int:id_>')
@required_group('editor')
def source_delete(id_):
    g.cursor.execute('BEGIN')
    try:
        EntityMapper.delete(id_)
        logger.log_user(id_, 'delete')
        g.cursor.execute('COMMIT')
        flash(_('entity deleted'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    return redirect(url_for('source_index'))


@app.route('/source/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def source_update(id_):
    source = EntityMapper.get_by_id(id_)
    form = build_form(SourceForm, 'Source', source, request)
    if form.validate_on_submit():
        if was_modified(form, source):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(source.id)['modifier'])
            return render_template(
                'source/update.html', form=form, source=source, modifier=modifier)
        save(form, source)
        return redirect(url_for('source_view', id_=id_))
    return render_template('source/update.html', form=form, source=source)


def save(form, source=None, origin=None):
    g.cursor.execute('BEGIN')
    try:
        log_action = 'update'
        if not source:
            source = EntityMapper.insert('E33', form.name.data, 'source content')
            log_action = 'insert'
        source.name = form.name.data
        source.description = form.description.data
        source.update()
        source.save_nodes(form)
        url = url_for('source_view', id_=source.id)
        if origin:
            url = url_for(get_view_name(origin) + '_view', id_=origin.id) + '#tab-source'
            if get_view_name(origin) == 'reference':
                link_ = origin.link('P67', source)
                url = url_for('reference_link_update', link_id=link_, origin_id=origin)
            elif get_view_name(origin) == 'file':
                origin.link('P67', source)
            else:
                source.link('P67', origin)
        g.cursor.execute('COMMIT')
        if form.continue_.data == 'yes':
            url = url_for('source_insert', origin_id=origin.id if origin else None)
        logger.log_user(source.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('source_insert', origin_id=origin.id if origin else None)
    return url
