from typing import Optional, Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.util import build_form2
from openatlas.models.entity import Entity
from openatlas.util.display import get_entity_data
from openatlas.util.util import required_group


class TranslationForm(FlaskForm):  # type: ignore
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    description = TextAreaField(_('content'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()


@app.route('/source/translation/insert/<int:source_id>', methods=['POST', 'GET'])
@required_group('contributor')
def translation_insert(source_id: int) -> Union[str, Response]:
    source = Entity.get_by_id(source_id, view_name='source')
    form = build_form2(TranslationForm, 'Source translation')
    if form.validate_on_submit():
        translation = save(form, source=source)
        flash(_('entity created'), 'info')
        if hasattr(form, 'continue_') and form.continue_.data == 'yes':
            return redirect(url_for('translation_insert', source_id=source.id))
        return redirect(url_for('entity_view', id_=translation.id))
    return render_template('translation/insert.html', source=source, form=form)


@app.route('/source/translation/delete/<int:id_>/<int:source_id>')
@required_group('contributor')
def translation_delete(id_: int, source_id: int) -> Response:
    Entity.delete_(id_)
    flash(_('entity deleted'), 'info')
    return redirect(url_for('entity_view', id_=source_id))


@app.route('/source/translation/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def translation_update(id_: int) -> Union[str, Response]:
    translation = Entity.get_by_id(id_, nodes=True)
    source = translation.get_linked_entity('P73', True)
    form = build_form2(TranslationForm, 'Source translation', translation, request)
    if form.validate_on_submit():
        save(form, translation)
        flash(_('info update'), 'info')
        return redirect(url_for('entity_view', id_=translation.id))
    return render_template('translation/update.html',
                           translation=translation,
                           source=source,
                           form=form)


def translation_view(translation: Entity) -> str:
    return render_template('translation/view.html',
                           info=get_entity_data(translation),
                           source=translation.get_linked_entity('P73', True),
                           translation=translation)


def save(form: FlaskForm,
         entity: Optional[Entity] = None,
         source: Optional[Entity] = None) -> Entity:
    g.cursor.execute('BEGIN')
    try:
        if entity:
            logger.log_user(entity.id, 'update')
        elif source:
            entity = Entity.insert('E33', form.name.data, 'source translation')
            source.link('P73', entity)
            logger.log_user(entity.id, 'insert')
        else:
            abort(400)  # pragma: no cover, either entity or source has to be provided
        entity.update(form)
        g.cursor.execute('COMMIT')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    return entity  # type: ignore
