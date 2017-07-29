# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import bcrypt
import datetime
from openatlas import app
from flask import render_template, request, flash
from flask_babel import lazy_gettext as _
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired
from openatlas.models.user import UserMapper

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return UserMapper.get_by_id(user_id)


class LoginForm(Form):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserMapper.get_by_username(request.form['username'])
        if user:
            if user.login_attempts_exceeded():
                flash(_('error login attempts exceeded'), 'error')
                return render_template('login/index.html', form=form)
            password_hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), user.password.encode('utf-8'))
            if password_hashed == user.password.encode('utf-8'):
                if user.active:
                    login_user(user)
                    user.login_last_success = datetime.datetime.now()
                    user.login_failed_count = 0
                    user.update()
                    if request.args.get('next'):
                        return redirect(request.args.get('next'))
                    return redirect('/')
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
