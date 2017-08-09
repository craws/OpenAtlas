# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_login import login_required, current_user
from openatlas import app
from openatlas.util.util import uc_first


@app.route('/profile')
@login_required
def profile_index():
    tables = {}
    tables['info'] = [
        {uc_first(_('username')): current_user.username},
        {uc_first(_('name')): current_user.real_name},
        {uc_first(_('email')): current_user.email},
        {uc_first(_('show email')): current_user.get_setting('show_email', 'display')},
        {uc_first(_('newsletter')): current_user.get_setting('newsletter', 'display')}
    ]
    return render_template('profile/index.html', tables=tables)


@app.route('/profile/update')
@login_required
def profile_update():
    return render_template('profile/update.html')


@app.route('/profile/password')
@login_required
def profile_password():
    return render_template('profile/password.html')
