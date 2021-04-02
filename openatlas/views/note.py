from typing import Optional, Union

from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.user import User
from openatlas.util.display import uc_first
from openatlas.util.util import required_group


@app.route('/note/insert/<int:entity_id>', methods=['POST', 'GET'])
@required_group('contributor')
def note_insert(entity_id: int) -> Union[str, Response]:
    entity = Entity.get_by_id(entity_id)
    form = build_form('note')
    if form.validate_on_submit():
        save(form, entity_id=entity.id)
        return redirect(url_for('entity_view', id_=entity.id) + '#tab-note')
    return render_template(
        'display_form.html',
        form=form,
        entity=entity,
        crumbs=[
            [_(entity.class_.view), url_for('index', view=_(entity.class_.view))],
            entity,
            '+ ' + uc_first(_('note'))])


@app.route('/note/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def note_update(id_: int) -> Union[str, Response]:
    note = current_user.get_note_by_id(id_)
    entity = Entity.get_by_id(note['entity_id'])
    form = build_form('note')
    if form.validate_on_submit():
        save(form, note_id=note['id'])
        return redirect(url_for('entity_view', id_=note['entity_id']) + '#tab-note')
    form.save.label.text = _('update')
    form.description.data = note['text']
    form.public.data = note['public']
    return render_template(
        'display_form.html',
        form=form,
        entity=entity,
        crumbs=[
            [_(entity.class_.view), url_for('index', view=_(entity.class_.view))],
            entity,
            _('edit note')])


def save(form: FlaskForm, entity_id: Optional[int] = None, note_id: Optional[int] = None) -> None:
    Transaction.begin()
    try:
        if entity_id:
            User.insert_note(entity_id, form.description.data, form.public.data)
        else:
            User.update_note(note_id, form.description.data, form.public.data)
        Transaction.commit()
        flash(_('note added') if entity_id else _('note updated'), 'info')
    except Exception as e:  # pragma: no cover
        Transaction.rollback()
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')


@app.route('/note/delete/<int:entity_id>', methods=['POST', 'GET'])
@required_group('contributor')
def note_delete(entity_id: int) -> Response:
    User.delete_note(entity_id)
    flash(_('note deleted'), 'info')
    return redirect(url_for('entity_view', id_=entity_id))
