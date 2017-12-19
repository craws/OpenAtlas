# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from bcrypt import hashpw
import datetime

import openatlas
from openatlas import app
from flask import render_template, request, flash, url_for, session
from flask_babel import lazy_gettext as _
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired
from openatlas.models.user import UserMapper

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return UserMapper.get_by_id(user_id)


class LoginForm(Form):
    username = StringField(_('username'), validators=[InputRequired()])
    password = PasswordField(_('password'), validators=[InputRequired()])
    show_passwords = BooleanField(_('show password'))
    save = SubmitField(_('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = UserMapper.get_by_username(request.form['username'])
        if user:
            if user.login_attempts_exceeded():
                flash(_('error login attempts exceeded'), 'error')
                return render_template('login/index.html', form=form)
            hash_ = hashpw(request.form['password'].encode('utf-8'), user.password.encode('utf-8'))
            if hash_ == user.password.encode('utf-8'):
                if user.active:
                    login_user(user)
                    session['login_previous_success'] = user.login_last_success
                    session['login_previous_failures'] = user.login_failed_count
                    user.login_last_success = datetime.datetime.now()
                    user.login_failed_count = 0
                    user.update()
                    return redirect(request.args.get('next') or url_for('index'))
                else:
                    flash(_('error inactive'), 'error')
            else:
                user.login_failed_count += 1
                user.login_last_failure = datetime.datetime.now()
                user.update()
                flash(_('error wrong password'), 'error')
        else:
            flash(_('error username'), 'error')
        return render_template('login/index.html', form=form)
    return render_template('login/index.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')
