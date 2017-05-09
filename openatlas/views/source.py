# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.util.util import uc_first


class SourceForm(Form):
    name = StringField(uc_first(_('name')), validators=[InputRequired()])
    description = StringField(uc_first(_('content')))


@app.route('/source')
def source_index():
    return render_template('source/index.html')


@app.route('/source/insert/<code>', methods=['POST', 'GET'])
def source_insert(code):
    form = SourceForm()
    if form.validate_on_submit():
        pass
    return render_template('source/insert.html', form=form)
