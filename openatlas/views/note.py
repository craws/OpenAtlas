from typing import Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
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
        save(form, entity=entity)
        return redirect(url_for('entity_view', id_=entity.id))
    return render_template(
        'display_form.html',
        form=form,
        entity=entity,
        crumbs=[[_(entity.view_name), url_for('index', view=_(entity.view_name))],
                entity,
                '+ ' + uc_first(_('note'))])


@app.route('/note/update/<int:entity_id>', methods=['POST', 'GET'])
@required_group('contributor')
def note_update(entity_id: int) -> Union[str, Response]:
    entity = Entity.get_by_id(entity_id)
    form = build_form('note')
    if form.validate_on_submit():
        save(form, entity=entity, insert=False)
        return redirect(url_for('entity_view', id_=entity.id))
    form.save.label.text = _('update')
    form.description.data = User.get_note(entity)
    return render_template(
        'display_form.html',
        form=form,
        entity=entity,
        crumbs=[[_(entity.view_name), url_for('index', view=_(entity.view_name))],
                entity,
                _('edit note')])


def save(form: FlaskForm, entity: Entity, insert: bool = True) -> None:
    g.cursor.execute('BEGIN')
    try:
        if insert:
            User.insert_note(entity, form.description.data)
        else:
            User.update_note(entity, form.description.data)
        g.cursor.execute('COMMIT')
        flash(_('note added') if insert else _('note updated'), 'info')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')


@app.route('/note/delete/<int:entity_id>', methods=['POST', 'GET'])
@required_group('contributor')
def note_delete(entity_id: int) -> Response:
    User.delete_note(entity_id)
    flash(_('note deleted'), 'info')
    return redirect(url_for('entity_view', id_=entity_id))
