# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import (SubmitField, TextAreaField)
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.user import UserMapper
from openatlas.util.util import (required_group)


class NoteForm(FlaskForm):
    description = TextAreaField(_('note'), [InputRequired()])
    save = SubmitField(_('insert'))


@app.route('/note/insert/<int:entity_id>', methods=['POST', 'GET'])
@required_group('contributor')
def note_insert(entity_id: int) -> Union[str, Response]:
    entity = EntityMapper.get_by_id(entity_id)
    form = build_form(NoteForm, 'note-form')
    if form.validate_on_submit():
        save(form, entity=entity)
        return redirect(url_for(entity.view_name + '_view', id_=entity.id))
    return render_template('note/insert.html', form=form, entity=entity)


@app.route('/note/update/<int:entity_id>', methods=['POST', 'GET'])
@required_group('contributor')
def note_update(entity_id: int) -> Union[str, Response]:
    entity = EntityMapper.get_by_id(entity_id)
    form = build_form(NoteForm, 'note-form')
    if form.validate_on_submit():
        save(form, entity=entity, insert=False)
        return redirect(url_for(entity.view_name + '_view', id_=entity.id))
    form.description.data = UserMapper.get_note(entity)
    return render_template('note/update.html', form=form, entity=entity)


def save(form, entity, insert: bool = True) -> None:
    g.cursor.execute('BEGIN')
    try:
        if insert:
            UserMapper.insert_note(entity, form.description.data)
        else:
            UserMapper.update_note(entity, form.description.data)
        g.cursor.execute('COMMIT')
        flash(_('note added') if insert else _('note updated'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')


@app.route('/note/delete/<int:entity_id>', methods=['POST', 'GET'])
@required_group('contributor')
def note_delete(entity_id: int) -> Response:
    entity = EntityMapper.get_by_id(entity_id)
    UserMapper.delete_note(entity)
    flash(_('note deleted'), 'info')
    return redirect(url_for(entity.view_name + '_view', id_=entity.id))
