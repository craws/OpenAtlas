# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas import app
from flask import render_template, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user
from openatlas.models.user import UserMapper
from werkzeug.utils import redirect
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired
import bcrypt
from flask_babel import lazy_gettext as _

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
            password_hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), user.password.encode('utf-8'))
            if password_hashed == user.password.encode('utf-8'):
                if user.active:
                    login_user(user)
                    if request.args.get("next"):
                        return redirect(request.args.get('next'))
                    return redirect('/')
                else:
                    flash(_("error inactive"), 'error')
            else:
                flash(_("error wrong password"), 'error')
        else:
            flash(_("error username"), 'error')
        return render_template('login/index.html', form=form)
    return render_template('login/index.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')
