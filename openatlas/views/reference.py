# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template
from openatlas import app


@app.route('/reference')
def reference_index():
    return render_template('reference/index.html')
