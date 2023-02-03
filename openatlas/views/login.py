import datetime
from typing import Optional, Union

import bcrypt
from bcrypt import hashpw
from flask import abort, flash, g, render_template, request, session, url_for
from flask_babel import lazy_gettext as _
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user)
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import Email, InputRequired

from openatlas import app
from openatlas.display.util import display_form, send_mail, uc_first
from openatlas.forms.field import SubmitField
from openatlas.models.user import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id: int) -> Optional[User]:
    return User.get_by_id(user_id, True)


class LoginForm(FlaskForm):
    username = StringField(
        _('username'),
        [InputRequired()],
        render_kw={'autofocus': True})
    password = PasswordField(_('password'), [InputRequired()])
    show_passwords = BooleanField(_('show password'))
    save = SubmitField(_('login'))


class PasswordResetForm(FlaskForm):
    email = StringField(_('email'), [InputRequired(), Email()])
    save = SubmitField(_('submit'))


@app.route('/login', methods=["GET", "POST"])
def login() -> Union[str, Response]:
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(request.form['username'])
        if user and user.username:
            if user.login_attempts_exceeded():
                g.logger.log(
                    'notice',
                    'auth',
                    f'Login attempts exceeded: {user.username}')
                flash(_('error login attempts exceeded'), 'error')
                return render_template('login.html', form=form)
            hash_ = hashpw(
                request.form['password'].encode('utf-8'),
                user.password.encode('utf-8'))
            if hash_ == user.password.encode('utf-8'):
                if user.active:
                    login_user(user)
                    session['login_previous_success'] = user.login_last_success
                    session['login_previous_failures'] = \
                        user.login_failed_count
                    if user.settings['language']:
                        session['language'] = user.settings['language']
                    user.login_last_success = datetime.datetime.now()
                    user.login_failed_count = 0
                    user.update()
                    g.logger.log('info', 'auth', f'Login of {user.username}')
                    return redirect(
                        request.args.get('next') or url_for('overview'))
                g.logger.log(
                    'notice',
                    'auth',
                    f'Inactive login try {user.username}')
                flash(_('error inactive'), 'error')
            else:
                g.logger.log(
                    'notice',
                    'auth',
                    f'Wrong password: {user.username}')
                user.login_failed_count += 1
                user.login_last_failure = datetime.datetime.now()
                user.update()
                flash(_('error wrong password'), 'error')
        else:
            g.logger.log(
                'notice',
                'auth',
                f"Wrong username: {request.form['username']}")
            flash(_('error username'), 'error')
    return render_template(
        'login.html',
        title=_('login'),
        form=form,
        crumbs=[_('login')])


@app.route('/password_reset', methods=["GET", "POST"])
def reset_password() -> Union[str, Response]:
    if current_user.is_authenticated:  # Prevent password reset if logged in
        return redirect(url_for('overview'))
    form = PasswordResetForm()
    if form.validate_on_submit() and g.settings['mail']:
        if user := User.get_by_email(form.email.data):
            code = User.generate_password()
            user.password_reset_code = code
            user.password_reset_date = datetime.datetime.now()
            user.update()
            url = url_for('reset_confirm', code=code)
            link = f"{request.scheme}://{request.headers['Host']}{url}"
            subject = _(
                'Password reset request for %(site_name)s',
                site_name=g.settings['site_name'])
            body = _(
                'We received a password reset request for %(username)s',
                username=user.username)
            body += \
                f" {_('at')} {request.headers['Host']}\n\n" \
                f"{_('reset password link')}:\n\n" \
                f"{link}\n\n" \
                f"{_('The link is valid for')} " \
                f"{g.settings['reset_confirm_hours']} {_('hours')}."
            email = form.email.data
            if send_mail(subject, body, form.email.data):
                flash(
                    _('A password reset confirmation mail was send '
                      'to %(email)s.', email=email),
                    'info')
            else:  # pragma: no cover
                flash(
                    _('Failed to send password reset confirmation mail '
                      'to %(email)s.', email=email),
                    'error')
            return redirect(url_for('login'))
        g.logger.log(
            'info',
            'password',
            f'Password reset for non existing {form.email.data}')
        flash(_('error non existing email'), 'error')
    return render_template(
        'content.html',
        content=f"<p>{_('info password reset')}</p>{display_form(form)}",
        crumbs=[[_('login'), url_for('login')], _('Forgot your password?')])


@app.route('/reset_confirm/<code>')
def reset_confirm(code: str) -> Response:
    user = User.get_by_reset_code(code)
    if not user or not user.username or not user.email:
        g.logger.log('info', 'auth', 'unknown reset code')
        flash(_('invalid password reset confirmation code'), 'error')
        abort(404)
    hours = g.settings['reset_confirm_hours']
    if datetime.datetime.now() > \
            user.password_reset_date + datetime.timedelta(hours=hours):
        g.logger.log('info', 'auth', 'reset code expired')
        flash(_('This reset confirmation code has expired.'), 'error')
        abort(404)
    password = User.generate_password()
    user.password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()).decode('utf-8')
    user.password_reset_code = None
    user.password_reset_date = None
    user.login_failed_count = 0
    user.update()
    subject = \
        _('New password for %(sitename)s', sitename=g.settings['site_name'])
    body = _('New password for %(username)s', username=user.username) + ' '
    body += f"{_('at')} {request.scheme}://{request.headers['Host']}:\n\n"
    body += f"{uc_first(_('username'))}: {user.username}\n"
    body += f"{uc_first(_('password'))}: {password}\n"
    if send_mail(subject, body, user.email, False):
        flash(
            _('A new password was sent to %(email)s.', email=user.email),
            'info')
    else:  # pragma: no cover
        flash(
            _('Failed to send password mail to %(email)s.', email=user.email),
            'error')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('login'))
