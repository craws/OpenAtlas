# -*- coding: utf-8 -*-
import openatlas

from flask import render_template
from openatlas import app


@app.route('/')
def index():
    return render_template('overview/index.html')

