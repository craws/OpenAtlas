# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.util.util import (required_group)


@app.route('/import/index')
@required_group('manager')
def import_index():
    return render_template('import/index.html')


class ProjectForm(Form):
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))


@app.route('/import/project/insert', methods=['POST', 'GET'])
@required_group('manager')
def import_project_insert():
    form = ProjectForm()
    return render_template('import/project_insert.html', form=form)
