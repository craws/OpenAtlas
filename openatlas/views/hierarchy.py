# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template
from openatlas import app
from openatlas.util.util import required_group


@app.route('/hierarchy')
@required_group('readonly')
def hierarchy_index():
    return render_template('hierarchy/index.html')
