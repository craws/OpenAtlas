# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Union

import bcrypt
from flask import flash, g, render_template, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import BooleanField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import Email, InputRequired

from openatlas import app, logger
from openatlas.util.util import uc_first


class PasswordForm(FlaskForm):
    password_old = PasswordField(_('old password'), [InputRequired()])
    password = PasswordField(_('password'), [InputRequired()])
    password2 = PasswordField(_('repeat password'), [InputRequired()])
    show_passwords = BooleanField(_('show passwords'))
    save = SubmitField(_('save'))

    def validate(self) -> bool:
        valid = FlaskForm.validate(self)
        hash_ = bcrypt.hashpw(self.password_old.data.encode('utf-8'),
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


class ProfileForm(FlaskForm):
    name = StringField(description=_('tooltip full name'))
    email = StringField([InputRequired(), Email()], description=_('tooltip email'))
    show_email = BooleanField(description=_('tooltip show email'))
    newsletter = BooleanField(description=_('tooltip newsletter'))
    language = SelectField(choices=list(app.config['LANGUAGES'].items()))
    table_rows = SelectField(description=_('tooltip table rows'),
                             choices=list(app.config['DEFAULT_TABLE_ROWS'].items()),
                             coerce=int)
    table_show_aliases = SelectField(choices=[('off', _('off')), ('on', _('on'))])
    layout_choices = [('default', _('default')), ('advanced', _('advanced'))]
    layout = SelectField(_('layout'), description=_('tooltip layout'), choices=layout_choices)
    max_zoom = IntegerField(description=_('tooltip max zoom'))
    module_geonames = BooleanField(description=_('tooltip geonames'))
    module_map_overlay = BooleanField(description=_('tooltip map overlay'))
    module_notes = BooleanField(description=_('tooltip notes'))
    save = SubmitField(_('save'))


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile_index() -> str:
    user = current_user
    data = {'info': [(_('username'), user.username),
                     (_('full name'), user.real_name),
                     (_('email'), user.email),
                     (_('show email'),
                      uc_first(_('on')) if user.settings['show_email'] else uc_first(_('off'))),
                     (_('newsletter'),
                      uc_first(_('on')) if user.settings['newsletter'] else uc_first(_('off')))],
            'display': [(_('language'), user.settings['language']),
                        (_('table rows'), user.settings['table_rows']),
                        (_('show aliases in tables'), user.settings['table_show_aliases']),
                        (_('layout'), user.settings['layout']),
                        (_('max map zoom'), user.settings['max_zoom'])],
            'modules': [(_('GeoNames'), user.settings['module_geonames']),
                        (_('map overlay'), user.settings['module_map_overlay']),
                        (_('notes'), user.settings['module_notes'])]}
    return render_template('profile/index.html', data=data)


@app.route('/profile/update', methods=['POST', 'GET'])
@login_required
def profile_update() -> Union[str, Response]:
    form = ProfileForm()
    user = current_user
    if form.validate_on_submit():
        user.real_name = form.name.data
        user.email = form.email.data
        user.settings['show_email'] = form.show_email.data
        user.settings['newsletter'] = form.newsletter.data
        user.settings['language'] = form.language.data
        user.settings['table_rows'] = form.table_rows.data
        user.settings['module_geonames'] = form.module_geonames.data
        user.settings['module_map_overlay'] = form.module_map_overlay.data
        user.settings['module_notes'] = form.module_notes.data
        user.settings['max_zoom'] = form.max_zoom.data
        user.settings[
            'table_show_aliases'] = 'True' if form.table_show_aliases.data == 'on' else 'False'
        user.settings['layout'] = form.layout.data
        g.cursor.execute('BEGIN')
        try:
            user.update()
            user.update_settings()
            g.cursor.execute('COMMIT')
            session['language'] = form.language.data
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('profile_index'))
    form.name.data = current_user.real_name
    form.name.label.text = uc_first(_('full name'))
    form.email.data = current_user.email
    form.email.label.text = uc_first(_('email'))
    form.show_email.data = current_user.settings['show_email']
    form.show_email.label.text = uc_first(_('show email'))
    form.newsletter.data = current_user.settings['newsletter']
    form.newsletter.label.text = uc_first(_('newsletter'))
    language = user.settings['language'] if user.settings['language'] else session['language']
    form.language.data = language
    form.language.label.text = uc_first(_('language'))
    form.table_rows.data = user.settings['table_rows']
    form.table_rows.label.text = uc_first(_('table rows'))
    form.table_show_aliases.data = 'on' if user.settings['table_show_aliases'] else 'off'
    form.table_show_aliases.label.text = uc_first(_('show aliases in tables'))
    form.layout.data = user.settings['layout']
    form.layout.label.text = uc_first(_('layout'))
    form.max_zoom.data = user.settings['max_zoom']
    form.max_zoom.label.text = uc_first(_('max map zoom'))
    form.module_geonames.data = user.settings['module_geonames']
    form.module_geonames.label.text = 'GeoNames'
    form.module_map_overlay.data = user.settings['module_map_overlay']
    form.module_map_overlay.label.text = uc_first(_('map overlay'))
    form.module_notes.data = user.settings['module_notes']
    form.module_notes.label.text = uc_first(_('notes'))
    form.save.label.text = uc_first(_('save'))
    return render_template('profile/update.html', form=form)


@app.route('/profile/password', methods=['POST', 'GET'])
@login_required
def profile_password() -> Union[str, Response]:
    form = PasswordForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.hashpw(form.password.data.encode('utf-8'),
                                              bcrypt.gensalt()).decode('utf-8')
        current_user.update()
        flash(_('info password updated'), 'info')
        return redirect(url_for('profile_index'))
    return render_template('profile/password.html', form=form)
