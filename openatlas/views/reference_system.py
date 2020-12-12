from typing import Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from psycopg2._psycopg import IntegrityError
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Optional, URL

from openatlas import app, logger
from openatlas.models.reference_system import ReferenceSystem
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
