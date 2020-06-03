from typing import Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import TableMultiField, build_form, build_table_form
from openatlas.models.entity import Entity
from openatlas.models.user import User
from openatlas.util.table import Table
from openatlas.util.util import (button, display_remove_link, get_base_table_data, get_entity_data,
                                 get_profile_image_table_link, is_authorized, link, required_group,
                                 uc_first, was_modified)


class SourceForm(FlaskForm):  # type: ignore
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    information_carrier = TableMultiField()
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/source')
@app.route('/source/<action>/<int:id_>')
@required_group('readonly')
def source_index(action: Optional[str] = None, id_: Optional[int] = None) -> str:
    if id_ and action == 'delete':
        Entity.delete_(id_)
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
    table = Table(Table.HEADERS['source'])
    for source in Entity.get_by_menu_item('source'):
        data = get_base_table_data(source)
        table.rows.append(data)
    return render_template('source/index.html', table=table)


@app.route('/source/insert/<int:origin_id>', methods=['POST', 'GET'])
@app.route('/source/insert', methods=['POST', 'GET'])
@required_group('contributor')
def source_insert(origin_id: Optional[int] = None) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id) if origin_id else None
    form = build_form(SourceForm, 'Source')
    if origin:
        del form.insert_and_continue
    if form.validate_on_submit():
        return redirect(save(form, origin=origin))
    if origin and origin.class_.code == 'E84':
        form.information_carrier.data = [origin_id]
    return render_template('source/insert.html', form=form, origin=origin)


@app.route('/source/add/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('contributor')
def source_add(id_: int, class_name: str) -> Union[str, Response]:
    source = Entity.get_by_id(id_, view_name='source')
    if request.method == 'POST':
        if request.form['checkbox_values']:
            source.link_string('P67', request.form['checkbox_values'])
        return redirect(url_for('entity_view', id_=source.id) + '#tab-' + class_name)
    form = build_table_form(class_name, source.get_linked_entities('P67'))
    return render_template('source/add.html', source=source, class_name=class_name, form=form)


@app.route('/source/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def source_update(id_: int) -> Union[str, Response]:
    source = Entity.get_by_id(id_, nodes=True, view_name='source')
    form = build_form(SourceForm, 'Source', source, request)
    if form.validate_on_submit():
        if was_modified(form, source):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(source.id)['modifier'])
            return render_template('source/update.html',
                                   form=form,
                                   source=source,
                                   modifier=modifier)
        save(form, source)
        return redirect(url_for('entity_view', id_=id_))
    form.information_carrier.data = [entity.id for entity in
                                     source.get_linked_entities('P128', inverse=True)]
    return render_template('source/update.html', form=form, source=source)


def save(form: FlaskForm, source: Optional[Entity] = None, origin: Optional[Entity] = None) -> str:
    g.cursor.execute('BEGIN')
    log_action = 'update'
    try:
        if not source:
            source = Entity.insert('E33', form.name.data, 'source content')
            log_action = 'insert'
        source.update(form)

        # Information carrier
        source.delete_links(['P128'], inverse=True)
        if form.information_carrier.data:
            source.link_string('P128', form.information_carrier.data, inverse=True)

        url = url_for('entity_view', id_=source.id)
        if origin:
            url = url_for('entity_view', id_=origin.id) + '#tab-source'
            if origin.view_name == 'reference':
                link_id = origin.link('P67', source)[0]
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


def source_view(source: Entity) -> str:
    source.note = User.get_note(source)
    tabs = {
        'info': {'header': _('info')},
        'event': {'header': _('event')},
        'actor': {'header': _('actor')},
        'place': {
            'header': _('place'),
            'buttons': [button(_('add'), url_for('source_add', id_=source.id, class_name='place')),
                        button( _('place'), url_for('place_insert', origin_id=source.id))]},
        'feature': {'header': _('feature')},
        'stratigraphic_unit': {'header': 'stratigraphic unit'},
        'find': {'header': _('find')},
        'human_remains': {'header': _('human remains')},
        'reference': {
            'header': _('reference'),
            'table': Table(Table.HEADERS['reference'] + ['page']),
            'buttons': [button(_('add'), url_for('entity_add_reference', id_=source.id)),
                        button(_('bibliography'), url_for('reference_insert',
                                                          code='bibliography',
                                                          origin_id=source.id)),
                        button(_('edition'), url_for('reference_insert',
                                                     code='edition',
                                                     origin_id=source.id)),
                        button(_('external reference'), url_for('reference_insert',
                                                                code='external_reference',
                                                                origin_id=source.id))]},
        'text': {
            'header': _('texts'),
            'table': Table(['text', 'type', 'content']),
            'buttons': [button(_('text'), url_for('translation_insert', source_id=source.id))]},
        'file': {
            'header': _('files'),
            'table': Table(Table.HEADERS['file'] + [_('main image')]),
            'buttons': [button(_('add'), url_for('entity_add_file', id_=source.id)),
                        button(_('file'), url_for('file_insert', origin_id=source.id))]}}
    for name in ['event', 'actor']:
        tabs[name]['buttons'] = [
            button(_('add'), url_for('source_add', id_=source.id, class_name=name))]
        for code in app.config['CLASS_CODES'][name]:
            tabs[name]['buttons'].append(button(
                g.classes[code].name, url_for(name + '_insert', code=code, origin_id=source.id)))
    for text in source.get_linked_entities('P73', nodes=True):
        tabs['text']['table'].rows.append([link(text),
                                           next(iter(text.nodes)).name if text.nodes else '',
                                           text.description])
    for name in ['actor', 'event', 'place', 'feature', 'stratigraphic_unit', 'find',
                 'human_remains']:
        tabs[name]['table'] = Table(Table.HEADERS[name])
    tabs['actor']['table'].defs = [{'className': 'dt-body-right', 'targets': [2, 3]}]
    tabs['event']['table'].defs = [{'className': 'dt-body-right', 'targets': [3, 4]}]
    tabs['place']['table'].defs = [{'className': 'dt-body-right', 'targets': [2, 3]}]
    for link_ in source.get_links('P67'):
        range_ = link_.range
        data = get_base_table_data(range_)
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=source.id)
            data.append(display_remove_link(url + '#tab-' + range_.table_name, range_.name))
        tabs[range_.table_name]['table'].rows.append(data)
    profile_image_id = source.get_profile_image_id()
    for link_ in source.get_links('P67', True):
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
        tabs[domain.view_name]['table'].rows.append(data)
    return render_template('source/view.html',
                           source=source,
                           tabs=tabs,
                           info=get_entity_data(source),
                           profile_image_id=profile_image_id)
