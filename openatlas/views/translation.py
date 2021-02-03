from typing import Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.util.display import uc_first
from openatlas.util.util import required_group


@app.route('/source/translation/insert/<int:source_id>', methods=['POST', 'GET'])
@required_group('contributor')
def translation_insert(source_id: int) -> Union[str, Response]:
    source = Entity.get_by_id(source_id)
    form = build_form('source_translation')
    if form.validate_on_submit():
        translation = save(form, source=source)
        flash(_('entity created'), 'info')
        if hasattr(form, 'continue_') and form.continue_.data == 'yes':
            return redirect(url_for('translation_insert', source_id=source.id))
        return redirect(url_for('entity_view', id_=translation.id))
    return render_template('display_form.html',
                           form=form,
                           crumbs=[[_('source'), url_for('index', class_='source')],
                                   source,
                                   '+ ' + uc_first(_('text'))])


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
    form = build_form('source_translation', translation)
    if form.validate_on_submit():
        save(form, translation)
        flash(_('info update'), 'info')
        return redirect(url_for('entity_view', id_=translation.id))
    return render_template('display_form.html',
                           form=form,
                           title=translation.name,
                           crumbs=[[_('source'), url_for('index', class_='source')],
                                   source,
                                   translation,
                                   _('edit')])


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
