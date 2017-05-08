# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template
from openatlas import app


@app.route('/actor')
def actor_index():
    return render_template('actor/index.html')
