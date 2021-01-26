from typing import Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from psycopg2 import IntegrityError
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.util import required_group


@app.route('/reference_system/insert', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_insert() -> Union[str, Response]:
    form = build_form('reference_system')
    if form.validate_on_submit():
        url = save(form)
        if url:
            return redirect(url)
    return render_template('reference_system/insert.html', form=form)


@app.route('/reference_system/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_update(id_: int) -> Union[str, Response]:
    entity = g.reference_systems[id_]
    form = build_form('reference_system', entity)
    if entity.system:
        form.name.render_kw['readonly'] = 'readonly'
    if form.validate_on_submit():
        url = save(form, entity)
        if url:
            return redirect(url)
    return render_template('reference_system/update.html', form=form, entity=entity)


@app.route('/reference_system/remove_form/<int:system_id>/<int:form_id>', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_remove_form(system_id: int, form_id: int) -> Response:
    # Todo: check if there are no form connections anymore
    try:
        g.reference_systems[system_id].remove_form(form_id)
        flash(_('info update'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'database', 'remove form failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('entity_view', id_=system_id))


def save(form: FlaskForm, entity: ReferenceSystem = None) -> str:
    g.cursor.execute('BEGIN')
    try:
        if not entity:
            log_action = 'insert'
            entity = ReferenceSystem.insert_system(form)
        else:
            log_action = 'update'
            entity.name = entity.name if entity.system else form.name.data
            entity.description = form.description.data
        entity.website_url = form.website_url.data if form.website_url.data else None
        entity.resolver_url = form.resolver_url.data if form.resolver_url.data else None
        entity.placeholder = form.placeholder.data if form.placeholder.data else None
        entity.resolver_url = form.resolver_url.data if form.resolver_url.data else None
        entity.update_system(form)
        if hasattr(form, 'forms'):
            entity.add_forms(form)
        g.cursor.execute('COMMIT')
        logger.log_user(entity.id, log_action)
        flash(_('entity created') if log_action == 'insert' else _('info update'), 'info')
        return url_for('entity_view', id_=entity.id)
    except IntegrityError:
        g.cursor.execute('ROLLBACK')
        flash(_('error name exists'), 'error')
    except Exception as e:  # pragma: no cover
        g.cursor.execute('ROLLBACK')
        logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    return ''
