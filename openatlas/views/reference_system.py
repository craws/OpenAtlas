from typing import Dict, List, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from psycopg2._psycopg import IntegrityError
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Optional, URL

from openatlas import app, logger
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem
from openatlas.util.display import external_url
from openatlas.util.tab import Tab
from openatlas.util.util import required_group


class ReferenceSystemForm(FlaskForm):  # type: ignore
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    website_url = StringField(_('website URL'), validators=[Optional(), URL()])
    resolver_url = StringField(_('resolver URL'), validators=[Optional(), URL()])
    description = TextAreaField(_('description'))
    save = SubmitField(_('save'))


@app.route('/reference_system/insert', methods=['POST', 'GET'])
@required_group('manager')
def reference_system_insert() -> Union[str, Response]:
    form = ReferenceSystemForm()
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            ReferenceSystem.insert(form)
            flash(_('entity created'), 'info')
            g.cursor.execute('COMMIT')
            return redirect(url_for('admin_index') + '#tab-reference-system')
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
    form = ReferenceSystemForm(entity)
    if form.validate_on_submit():
        pass
    return render_template('reference_system/update.html', form=form, entity=entity)


@app.route('/reference_system/view', methods=['POST', 'GET'])
def reference_system_view(entity: Entity) -> Union[str, Response]:
    tabs = {name: Tab(name, origin=entity) for name in ['info']}
    info: Dict[str, Union[str, List[str]]] = {
        _('website URL'): external_url(entity.website_url),
        _('resolver URL'): external_url(entity.resolver_url)}
    return render_template('reference_system/view.html', entity=entity, tabs=tabs, info=info)
