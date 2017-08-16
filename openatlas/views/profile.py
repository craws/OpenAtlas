# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_login import login_required, current_user
from openatlas import app


@app.route('/profile')
@login_required
def profile_index():
    tables = {'info': [
        (_('username'), current_user.username),
        (_('name'), current_user.real_name),
        (_('email'), current_user.email),
        (_('show email'), current_user.get_setting('show_email')),
        (_('newsletter'), current_user.get_setting('newsletter')),
    ]}
    return render_template('profile/index.html', tables=tables)


@app.route('/profile/update')
@login_required
def profile_update():
    return render_template('profile/update.html')


@app.route('/profile/password')
@login_required
def profile_password():
    return render_template('profile/password.html')
