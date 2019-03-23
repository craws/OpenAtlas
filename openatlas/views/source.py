# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import build_form
from openatlas.models.entity import EntityMapper
from openatlas.util.util import (build_table_form, display_remove_link, get_base_table_data,
                                 get_entity_data, is_authorized, link, required_group,
                                 truncate_string, uc_first, was_modified,
                                 get_profile_image_table_link)


class SourceForm(Form):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
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


@app.route('/source/view/<int:id_>')
@required_group('readonly')
def source_view(id_):
    source = EntityMapper.get_by_id(id_)
    tables = {
        'info': get_entity_data(source),
        'text': {'id': 'translation', 'data': [], 'header': ['text', 'type', 'content']},
        'file': {'id': 'files', 'data': [],
                 'header': app.config['TABLE_HEADERS']['file'] + [_('main image')]},
        'reference': {'id': 'source', 'data': [],
                      'header': app.config['TABLE_HEADERS']['reference'] + ['page']}}
    for text in source.get_linked_entities('P73'):
        tables['text']['data'].append([
            link(text),
            next(iter(text.nodes)).name if text.nodes else '',
            truncate_string(text.description)])
    for name in ['actor', 'event', 'place', 'feature', 'stratigraphic-unit', 'find']:
        tables[name] = {'id': name, 'header': app.config['TABLE_HEADERS'][name], 'data': []}
    for link_ in source.get_links('P67'):
        range_ = link_.range
        data = get_base_table_data(range_)
        if is_authorized('editor'):
            url = url_for('link_delete', id_=link_.id, origin_id=source.id)
            data.append(display_remove_link(url + '#tab-' + range_.table_name, range_.name))
        tables[range_.table_name]['data'].append(data)
    profile_image_id = source.get_profile_image_id()
    for link_ in source.get_links(['P67', 'P128'], True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':  # pragma: no cover
            extension = data[3].replace('.', '')
            data.append(get_profile_image_table_link(domain, source, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if domain.view_name not in ['file']:
            data.append(link_.description)
            if domain.system_type == 'external reference':
                source.external_references.append(domain.name)
            if is_authorized('editor'):
                update_url = url_for('reference_link_update', link_id=link_.id, origin_id=source.id)
                data.append('<a href="' + update_url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('editor'):
            url = url_for('link_delete', id_=link_.id, origin_id=source.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name]['data'].append(data)
    return render_template('source/view.html', source=source, tables=tables,
                           profile_image_id=profile_image_id)


@app.route('/source/add/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def source_add(origin_id):
    """ Link an entity to source coming from the entity."""
    origin = EntityMapper.get_by_id(origin_id)
    if request.method == 'POST':
        g.cursor.execute('BEGIN')
        try:
            for entity in EntityMapper.get_by_ids(request.form.getlist('values')):
                entity.link('P67', origin)
            g.cursor.execute('COMMIT')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for(origin.view_name + '_view', id_=origin.id) + '#tab-source')
    form = build_table_form('source', origin.get_linked_entities('P67', True))
    return render_template('source/add.html', origin=origin, form=form)


@app.route('/source/add2/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('editor')
def source_add2(id_, class_name):
    """ Link an entity to source coming from the source"""
    source = EntityMapper.get_by_id(id_)
    if request.method == 'POST':
        for entity in EntityMapper.get_by_ids(request.form.getlist('values')):
            source.link('P67', entity)
        return redirect(url_for('source_view', id_=source.id) + '#tab-' + class_name)
    form = build_table_form(class_name, source.get_linked_entities('P67'))
    return render_template('source/add2.html', source=source, class_name=class_name, form=form)


@app.route('/source/delete/<int:id_>')
@required_group('editor')
def source_delete(id_):
    EntityMapper.delete(id_)
    logger.log_user(id_, 'delete')
    flash(_('entity deleted'), 'info')
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
            return render_template('source/update.html', form=form, source=source,
                                   modifier=modifier)
        save(form, source)
        return redirect(url_for('source_view', id_=id_))
    return render_template('source/update.html', form=form, source=source)


def save(form, source=None, origin=None):
    g.cursor.execute('BEGIN')
    log_action = 'update'
    try:
        if not source:
            source = EntityMapper.insert('E33', form.name.data, 'source content')
            log_action = 'insert'
        source.name = form.name.data
        source.description = form.description.data
        source.update()
        source.save_nodes(form)
        url = url_for('source_view', id_=source.id)
        if origin:
            url = url_for(origin.view_name + '_view', id_=origin.id) + '#tab-source'
            if origin.view_name == 'reference':
                link_id = origin.link('P67', source)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin)
            elif origin.view_name == 'file':
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
