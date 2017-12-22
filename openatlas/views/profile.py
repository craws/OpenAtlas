# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import bcrypt
from flask import flash, render_template, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user, login_required
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import BooleanField, PasswordField, SelectField, SubmitField, StringField
from wtforms.validators import Email, InputRequired, Length

import openatlas
from openatlas import app
from openatlas.util.util import uc_first


class DisplayForm(Form):
    language = SelectField(uc_first(_('language')), choices=[])
    table_rows = SelectField(
        uc_first(_('table rows')), description='tip table rows', choices=[], coerce=int)
    layout = SelectField(
        uc_first(_('layout')),
        description='tip layout',
        choices=[('default', uc_first(_('default'))), ('advanced', uc_first(_('advanced')))])


class PasswordForm(Form):
    password_old = PasswordField(_('old password'), validators=[InputRequired()])
    password = PasswordField(_('password'), validators=[InputRequired()])
    password2 = PasswordField(_('repeat password'), validators=[InputRequired()])
    show_passwords = BooleanField(_('show passwords'))
    save = SubmitField(_('save'))

    def validate(self, extra_validators=None):
        valid = Form.validate(self)
        hash_ = bcrypt.hashpw(
            self.password_old.data.encode('utf-8'),
            current_user.password.encode('utf-8'))
        if hash_ != current_user.password.encode('utf-8'):
            self.password_old.errors.append(_('error wrong password'))
            valid = False
        if self.password.data != self.password2.data:
            self.password.errors.append(_('error passwords must match'))
            self.password2.errors.append(_('error passwords must match'))
            valid = False
        return valid


class ProfileForm(Form):
    name = StringField(_('name'))
    email = StringField(_('email'), validators=[InputRequired(), Email()])
    show_email = BooleanField(_('show email'))
    newsletter = BooleanField(_('newsletter'))
    save = SubmitField(_('save'))


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile_index():
    data = {'info': [
        (_('username'), current_user.username),
        (_('name'), current_user.real_name),
        (_('email'), current_user.email),
        (_('show email'),
            uc_first(_('on')) if current_user.settings['show_email'] else uc_first(_('off'))),
        (_('newsletter'),
            uc_first(_('on')) if current_user.settings['newsletter'] else uc_first(_('off')))]}
    form = DisplayForm()
    getattr(form, 'language').choices = app.config['LANGUAGES'].items()
    getattr(form, 'table_rows').choices = app.config['DEFAULT_TABLE_ROWS'].items()
    if form.validate_on_submit():
        current_user.settings['language'] = form.language.data
        current_user.settings['table_rows'] = form.table_rows.data
        current_user.settings['layout'] = form.layout.data
        openatlas.get_cursor().execute('BEGIN')
        current_user.update_settings()
        openatlas.get_cursor().execute('COMMIT')
        session['language'] = form.language.data
        flash(_('info update'), 'info')
        return redirect(url_for('profile_index'))

    form.language.data = current_user.settings['language']
    form.table_rows.data = current_user.settings['table_rows']
    form.layout.data = current_user.settings['layout']
    data['display'] = [
        (form.language.label, form.language),
        (str(form.table_rows.label) +
            ' <span class="tooltip" title="' + form.table_rows.description + '">i</span>',
            form.table_rows),
        (str(form.layout.label) +
            ' <span class="tooltip" title="' + form.layout.description + '">i</span>', form.layout)]
    return render_template('profile/index.html', data=data, form=form)


@app.route('/profile/update', methods=['POST', 'GET'])
@login_required
def profile_update():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.real_name = form.name.data
        current_user.email = form.email.data
        current_user.settings['show_email'] = form.show_email.data
        current_user.settings['newsletter'] = form.newsletter.data
        openatlas.get_cursor().execute('BEGIN')
        current_user.update()
        current_user.update_settings()
        openatlas.get_cursor().execute('COMMIT')
        flash(_('info update'), 'info')
        return redirect(url_for('profile_index'))
    form.name.data = current_user.real_name
    form.email.data = current_user.email
    form.show_email.data = current_user.settings['show_email']
    form.newsletter.data = current_user.settings['newsletter']
    return render_template('profile/update.html', form=form)


@app.route('/profile/password', methods=['POST', 'GET'])
@login_required
def profile_password():
    form = PasswordForm()
    form.password.validators.append(Length(min=session['settings']['minimum_password_length']))
    form.password2.validators.append(Length(min=session['settings']['minimum_password_length']))
    if form.validate_on_submit():
        current_user.password = bcrypt.hashpw(
            form.password.data.encode('utf-8'),
            bcrypt.gensalt()).decode('utf-8')
        current_user.update()
        flash(_('info password updated'), 'info')
        return redirect(url_for('profile_index'))
    return render_template('profile/password.html', form=form)
