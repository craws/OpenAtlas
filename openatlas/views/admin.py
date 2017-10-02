# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template

from openatlas import app
from openatlas.util.util import required_group


@app.route('/admin')
@required_group('manager')
def admin_index():
    return render_template('admin/index.html')
