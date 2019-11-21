# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import TableMultiField, build_form, build_table_form
from openatlas.models.entity import EntityMapper
from openatlas.models.user import UserMapper
from openatlas.util.table import Table
from openatlas.util.util import (display_remove_link, get_base_table_data,
                                 get_entity_data, get_profile_image_table_link, is_authorized, link,
                                 required_group, truncate_string, uc_first, was_modified)
from openatlas.views.reference import AddReferenceForm


class SourceForm(FlaskForm):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    information_carrier = TableMultiField()
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/source')
@required_group('readonly')
def source_index() -> str:
    table = Table(Table.HEADERS['source'])
    for source in EntityMapper.get_by_codes('source'):
        data = get_base_table_data(source)
        table.rows.append(data)
    return render_template('source/index.html', table=table)


@app.route('/source/insert/<int:origin_id>', methods=['POST', 'GET'])
@app.route('/source/insert', methods=['POST', 'GET'])
@required_group('contributor')
def source_insert(origin_id: int = None) -> Union[str, Response]:
    origin = EntityMapper.get_by_id(origin_id) if origin_id else None
    form = build_form(SourceForm, 'Source')
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        return redirect(save(form, origin=origin))
    if origin and origin.class_.code == 'E84':
        form.information_carrier.data = [origin_id]
    return render_template('source/insert.html', form=form, origin=origin)


@app.route('/source/view/<int:id_>')
@required_group('readonly')
def source_view(id_: int) -> str:
    source = EntityMapper.get_by_id(id_, nodes=True, view_name='source')
    source.note = UserMapper.get_note(source)
    tables = {'text': Table(['text', 'type', 'content']),
              'file': Table(Table.HEADERS['file'] + [_('main image')]),
              'reference': Table(Table.HEADERS['reference'] + ['page'])}
    for text in source.get_linked_entities('P73', nodes=True):
        tables['text'].rows.append([link(text),
                                    next(iter(text.nodes)).name if text.nodes else '',
                                    truncate_string(text.description)])
    for name in ['actor', 'event', 'place', 'feature', 'stratigraphic-unit', 'find']:
        tables[name] = Table(Table.HEADERS[name])
    tables['actor'].defs = '[{className: "dt-body-right", targets: [2,3]}]'
    tables['event'].defs = '[{className: "dt-body-right", targets: [3,4]}]'
    tables['place'].defs = '[{className: "dt-body-right", targets: [2,3]}]'
    for link_ in source.get_links('P67'):
        range_ = link_.range
        data = get_base_table_data(range_)
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=source.id)
            data.append(display_remove_link(url + '#tab-' + range_.table_name, range_.name))
        tables[range_.table_name].rows.append(data)
    profile_image_id = source.get_profile_image_id()
    for link_ in source.get_links(['P67'], True):
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
                source.external_references.append(link_)
            if is_authorized('contributor'):
                url = url_for('reference_link_update', link_id=link_.id, origin_id=source.id)
                data.append('<a href="' + url + '">' + uc_first(_('edit')) + '</a>')
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=source.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name].rows.append(data)
    return render_template('source/view.html', source=source, tables=tables,
                           info=get_entity_data(source), profile_image_id=profile_image_id)


@app.route('/source/add/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('contributor')
def source_add(id_: int, class_name: str) -> Union[str, Response]:
    source = EntityMapper.get_by_id(id_, view_name='source')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            source.link('P67', request.form['checkbox_values'])
        return redirect(url_for('source_view', id_=source.id) + '#tab-' + class_name)
    form = build_table_form(class_name, source.get_linked_entities('P67'))
    return render_template('source/add.html', source=source, class_name=class_name, form=form)


@app.route('/source/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def source_add_reference(id_: int) -> Union[str, Response]:
    source = EntityMapper.get_by_id(id_, view_name='source')
    form = AddReferenceForm()
    if form.validate_on_submit():
        source.link('P67', form.reference.data, description=form.page.data, inverse=True)
        return redirect(url_for('source_view', id_=id_) + '#tab-reference')
    form.page.label.text = uc_first(_('page / link text'))
    return render_template('add_reference.html', entity=source, form=form)


@app.route('/source/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def source_add_file(id_: int) -> Union[str, Response]:
    source = EntityMapper.get_by_id(id_, view_name='source')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            source.link('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('source_view', id_=id_) + '#tab-file')
    form = build_table_form('file', source.get_linked_entities('P67', inverse=True))
    return render_template('add_file.html', entity=source, form=form)


@app.route('/source/delete/<int:id_>')
@required_group('contributor')
def source_delete(id_: int) -> Response:
    EntityMapper.delete(id_)
    logger.log_user(id_, 'delete')
    flash(_('entity deleted'), 'info')
    return redirect(url_for('source_index'))


@app.route('/source/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def source_update(id_: int) -> Union[str, Response]:
    source = EntityMapper.get_by_id(id_, nodes=True, view_name='source')
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
    form.information_carrier.data = [entity.id for entity in
                                     source.get_linked_entities('P128', inverse=True)]
    return render_template('source/update.html', form=form, source=source)


def save(form, source=None, origin=None) -> str:
    g.cursor.execute('BEGIN')
    log_action = 'update'
    try:
        if not source:
            source = EntityMapper.insert('E33', form.name.data, 'source content')
            log_action = 'insert'
        url = url_for('source_view', id_=source.id)
        source.name = form.name.data
        source.description = form.description.data
        source.update()
        source.save_nodes(form)

        # Information carrier
        source.delete_links(['P128'], inverse=True)
        if form.information_carrier.data:
            source.link('P128', form.information_carrier.data, inverse=True)

        if origin:
            url = url_for(origin.view_name + '_view', id_=origin.id) + '#tab-source'
            if origin.view_name == 'reference':
                link_id = origin.link('P67', source)
                url = url_for('reference_link_update', link_id=link_id, origin_id=origin)
            elif origin.view_name == 'file':
                origin.link('P67', source)
            elif origin.class_.code != 'E84':
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
