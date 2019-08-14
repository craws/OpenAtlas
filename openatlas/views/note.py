# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import (SubmitField, TextAreaField)
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import build_form
from openatlas.models.entity import EntityMapper
from openatlas.models.user import UserMapper
from openatlas.util.util import (required_group)


class NoteForm(Form):
    description = TextAreaField(_('note'), [InputRequired()])
    save = SubmitField(_('insert'))


@app.route('/note/insert/<int:entity_id>', methods=['POST', 'GET'])
@required_group('contributor')
def note_insert(entity_id=None):
    entity = EntityMapper.get_by_id(entity_id) if entity_id else None
    form = build_form(NoteForm, 'note-form')
    if form.validate_on_submit():
        save(form, entity=entity)
        return redirect(url_for(entity.view_name + '_view', id_=entity.id))
    return render_template('note/insert.html', form=form, entity=entity)


def save(form, entity, note=None):
    g.cursor.execute('BEGIN')
    log_action = 'update'
    try:
        if not note:
            UserMapper.insert_note(entity, form.description.data)
            log_action = 'insert'
        else:
            UserMapper.update_note(entity, form.description.data)
        g.cursor.execute('COMMIT')
        flash(_('note added') if log_action == 'insert' else _('note update'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
