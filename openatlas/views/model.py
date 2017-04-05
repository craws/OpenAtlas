# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import openatlas
from flask import render_template
from openatlas import app


@app.route('/model')
def model_index():
    return render_template('model/index.html')


@app.route('/model/class')
def model_class():
    return render_template('model/class.html')


@app.route('/model/property')
def model_property():
    return render_template('model/property.html')
