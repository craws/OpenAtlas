# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template
from flask_login import login_required
from openatlas import app


@app.route('/profile')
@login_required
def profile_index():
    return render_template('profile/index.html')
