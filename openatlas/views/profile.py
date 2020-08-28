import importlib
from typing import Union

import bcrypt
from flask import flash, g, render_template, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.admin_forms import DisplayForm, ModulesForm, ProfileForm
from openatlas.forms.forms import get_form_settings, get_profile_form_settings
from openatlas.util.util import required_group, uc_first


class PasswordForm(FlaskForm):  # type: ignore
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


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile_index() -> str:
    return render_template('profile/index.html',
                           info={'profile': get_profile_form_settings(ProfileForm()),
                                 'modules': get_profile_form_settings(ModulesForm()),
                                 'display': get_profile_form_settings(DisplayForm())})


@app.route('/profile/settings/<category>', methods=['POST', 'GET'])
@required_group('contributor')
def profile_settings(category: str) -> Union[str, Response]:
    #if category in ['general', 'mail'] and not is_authorized('admin'):
    #    abort(403)  # pragma: no cover
    form = getattr(importlib.import_module('openatlas.forms.admin_forms'),
                   uc_first(category) + 'Form')()  # Get forms dynamically
    #if form.validate_on_submit():
    #    g.cursor.execute('BEGIN')
    #    try:
    #        Settings.update(form)
    #        logger.log('info', 'settings', 'Settings updated')
    #        g.cursor.execute('COMMIT')
    #        flash(_('info update'), 'info')
    #    except Exception as e:  # pragma: no cover
    #        g.cursor.execute('ROLLBACK')
    #        logger.log('error', 'database', 'transaction failed', e)
    #        flash(_('error transaction'), 'error')
    #    tab = 'data' if category == 'api' else category
    #    return redirect(url_for('admin_index') + '#tab-' + tab)
    #set_form_settings(form)
    return render_template('admin/settings.html', form=form, category=category)


@app.route('/profile/update', methods=['POST', 'GET'])
@login_required
def profile_update() -> Union[str, Response]:
    form = ProfileForm()
    user = current_user
    if form.validate_on_submit():
        for field in form:
            if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
                continue
            if field.name == 'name':
                user.real_name = field.data
            elif field.name == 'email':
                user.email = field.data
            else:
                user.settings[field.name] = field.data
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
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        field.label.text = uc_first(field.label.text)
        if field.name == 'name':
            field.data = current_user.real_name
        elif field.name == 'email':
            field.data = current_user.email
        else:
            field.data = current_user.settings[field.name]
    form.save.label.text = uc_first(_('save'))
    return render_template('profile/update.html',
                           form=form,
                           form_fields={_('general'): [form.name,
                                                       form.email,
                                                       form.show_email,
                                                       form.newsletter],
                                        _('display'): [form.language,
                                                       form.table_rows,
                                                       form.table_show_aliases,
                                                       form.layout,
                                                       form.map_zoom_default,
                                                       form.map_zoom_max],
                                        _('modules'): [form.module_geonames,
                                                       form.module_map_overlay,
                                                       form.module_notes]})


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
