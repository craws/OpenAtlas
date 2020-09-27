from typing import Any, Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import build_form
from openatlas.models.entity import Entity
from openatlas.models.user import User
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import (is_authorized, required_group, was_modified)
from openatlas.util.display import remove_link, get_base_table_data, get_entity_data, link


class InformationCarrierForm(FlaskForm):  # type: ignore
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()
    opened = HiddenField()


@app.route('/object')
@app.route('/object/<action>/<int:id_>')
@required_group('readonly')
def object_index(action: Optional[str] = None, id_: Optional[int] = None) -> str:
    if id_ and action == 'delete':
        Entity.delete_(id_)
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
    table = Table(Table.HEADERS['object'])
    table.rows = [get_base_table_data(item) for item in Entity.get_by_menu_item('object')]
    return render_template('object/index.html', table=table)


@app.route('/object/insert', methods=['POST', 'GET'])
@required_group('contributor')
def object_insert() -> Union[str, Response]:
    form = build_form(InformationCarrierForm, 'Information Carrier')
    if form.validate_on_submit():
        return redirect(save(form))
    return render_template('object/insert.html', form=form)


@app.route('/object/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def object_update(id_: int) -> Union[str, Response]:
    object_ = Entity.get_by_id(id_, nodes=True, view_name='object')
    form = build_form(InformationCarrierForm, object_.system_type.title(), object_, request)
    if form.validate_on_submit():
        if was_modified(form, object_):  # pragma: no cover
            del form.save
            flash(_('error modified'), 'error')
            modifier = link(logger.get_log_for_advanced_view(object_.id)['modifier'])
            return render_template('object/update.html',
                                   form=form,
                                   object_=object_,
                                   modifier=modifier)
        save(form, object_)
        return redirect(url_for('entity_view', id_=id_))
    return render_template('object/update.html', form=form, object_=object_)


def object_view(object_: Entity) -> str:
    tabs = {name: Tab(name, origin=object_) for name in ['info', 'source', 'event']}
    for link_ in object_.get_links('P128'):
        data = get_base_table_data(link_.range)
        if is_authorized('contributor'):
            data.append(remove_link(link_.range.name, link_, object_, link_.range.table_name))
        tabs['source'].table.rows.append(data)
    for link_ in object_.get_links('P25', inverse=True):
        data = get_base_table_data(link_.domain)
        if is_authorized('contributor'):
            data.append(remove_link(link_.range.name, link_, object_, link_.range.table_name))
        tabs['event'].table.rows.append(data)
    object_.note = User.get_note(object_)
    return render_template('object/view.html',
                           object_=object_,
                           tabs=tabs,
                           info=get_entity_data(object_))


def save(form: Any, object_: Optional[Entity] = None) -> str:
    g.cursor.execute('BEGIN')
    log_action = 'update'
    try:
        if not object_:
            log_action = 'insert'
            object_ = Entity.insert('E84', form.name.data, 'information carrier')
        object_.update(form)
        url = url_for('entity_view', id_=object_.id)
        url = url_for('object_insert') if form.continue_.data == 'yes' else url
        g.cursor.execute('COMMIT')
        logger.log_user(object_.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
        url = url_for('object_index')
    return url
