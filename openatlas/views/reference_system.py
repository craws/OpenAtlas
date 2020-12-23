from typing import Dict, List, Union

from flask import flash, g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from psycopg2 import IntegrityError
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.forms.form import build_form
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.display import external_url, link
from openatlas.util.tab import Tab
from openatlas.util.table import Table
from openatlas.util.util import is_authorized, required_group


@app.route('/reference_system/insert', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_insert() -> Union[str, Response]:
    form = build_form('reference_system')
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            entity = ReferenceSystem.insert(form)
            ReferenceSystem.add_forms(entity, form)
            flash(_('entity created'), 'info')
            g.cursor.execute('COMMIT')
            return redirect(url_for('entity_view', id_=entity.id))
        except IntegrityError as e:
            g.cursor.execute('ROLLBACK')
            flash(_('error name exists'), 'error')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
    return render_template('reference_system/insert.html', form=form)


@app.route('/reference_system/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_update(id_: int) -> Union[str, Response]:
    entity = ReferenceSystem.get_by_id(id_)
    form = build_form('reference_system', entity)
    if form.validate_on_submit():
        entity.name = form.name.data
        entity.description = form.description.data
        entity.website_url = form.website_url.data
        entity.resolver_url = form.resolver_url.data
        try:
            ReferenceSystem.update(entity, form)
            ReferenceSystem.add_forms(entity, form)
            flash(_('info update'), 'info')
            g.cursor.execute('COMMIT')
            return redirect(url_for('entity_view', id_=id_))
        except IntegrityError as e:
            g.cursor.execute('ROLLBACK')
            flash(_('error name exists'), 'error')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
    return render_template('reference_system/update.html', form=form, entity=entity)


@app.route('/reference_system/remove_form/<int:entity_id>/<int:form_id>', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_remove_form(entity_id: int, form_id: int):
    forms = ReferenceSystem.get_forms(entity_id)
    if forms[form_id]['count']:
        abort(403)  # pragma: no cover
    try:
        ReferenceSystem.remove_form(entity_id, form_id)
        flash(_('info update'), 'info')
    except Exception as e:  # pragma: no cover
        logger.log('error', 'database', 'remove form failed', e)
        flash(_('error database'), 'error')
    return redirect(url_for('entity_view', id_=entity_id))


def reference_system_view(entity: Entity) -> Union[str, Response]:
    tabs = {name: Tab(name, origin=entity) for name in ['info']}
    info: Dict[str, Union[str, List[str]]] = {
        _('website URL'): external_url(entity.website_url),
        _('resolver URL'): external_url(entity.resolver_url)}
    table = Table(paging=False)
    for form_id, form_ in ReferenceSystem.get_forms(entity.id).items():
        if not form_['count'] and is_authorized('manager'):
            html = link(_('remove'), url_for('reference_system_remove_form',
                                             entity_id=entity.id,
                                             form_id=form_id))
        else:
            html = format_number(form_['count'])
        table.rows.append([form_['name'], html])
    return render_template('reference_system/view.html',
                           entity=entity,
                           tabs=tabs,
                           info=info,
                           table=table)
