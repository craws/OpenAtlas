# Created 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import bcrypt
from flask import flash, g, render_template, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user, login_required
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import Email, InputRequired

from openatlas import app, logger
from openatlas.util.util import uc_first


class DisplayForm(Form):
    language = SelectField(_('language'), choices=app.config['LANGUAGES'].items())
    theme_choices = [
        ('default', _('default')),
        ('darkside', 'Darkside'),
        ('omg_ponies', 'OMG Ponies!')]
    theme = SelectField(_('color theme'), choices=theme_choices)
    table_rows = SelectField(
        _('table rows'),
        description=_('tooltip table rows'),
        choices=app.config['DEFAULT_TABLE_ROWS'].items(),
        coerce=int)
    layout_choices = [('default', _('default')), ('advanced', _('advanced'))]
    layout = SelectField(_('layout'), description=_('tooltip layout'), choices=layout_choices)


class PasswordForm(Form):
    password_old = PasswordField(_('old password'), [InputRequired()])
    password = PasswordField(_('password'), [InputRequired()])
    password2 = PasswordField(_('repeat password'), [InputRequired()])
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
        if self.password_old.data == self.password.data:
            self.password.errors.append(_('error new password like old password'))
            valid = False
        if len(self.password.data) < session['settings']['minimum_password_length']:
            self.password.errors.append(_('error password too short'))
            valid = False
        return valid


class ProfileForm(Form):
    name = StringField(_('full name'), description=_('tooltip full name'))
    email = StringField(_('email'), [InputRequired(), Email()], description=_('tooltip email'))
    show_email = BooleanField(_('show email'), description=_('tooltip show email'))
    newsletter = BooleanField(_('newsletter'), description=_('tooltip newsletter'))
    save = SubmitField(_('save'))


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile_index():
    user = current_user
    data = {'info': [
        (_('username'), user.username),
        (_('full name'), user.real_name),
        (_('email'), user.email),
        (_('show email'), uc_first(_('on')) if user.settings['show_email'] else uc_first(_('off'))),
        (_('newsletter'), uc_first(_('on')) if user.settings['newsletter'] else uc_first(_('off')))
    ]}
    form = DisplayForm()
    if form.validate_on_submit():
        user.settings['language'] = form.language.data
        user.settings['theme'] = form.theme.data
        user.settings['table_rows'] = form.table_rows.data
        user.settings['layout'] = form.layout.data
        g.cursor.execute('BEGIN')
        try:
            user.update_settings()
            g.cursor.execute('COMMIT')
            session['language'] = form.language.data
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('profile_index'))

    form.language.data = user.settings['language']
    form.theme.data = user.settings['theme']
    form.table_rows.data = user.settings['table_rows']
    form.layout.data = user.settings['layout']
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
        g.cursor.execute('BEGIN')
        try:
            current_user.update()
            current_user.update_settings()
            g.cursor.execute('COMMIT')
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
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
    if form.validate_on_submit():
        current_user.password = bcrypt.hashpw(
            form.password.data.encode('utf-8'),
            bcrypt.gensalt()).decode('utf-8')
        current_user.update()
        flash(_('info password updated'), 'info')
        return redirect(url_for('profile_index'))
    return render_template('profile/password.html', form=form)
