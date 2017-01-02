# -*- coding: utf-8 -*-
from flask import request, session
from werkzeug.utils import redirect

from flask import render_template
from openatlas import app


@app.route('/')
def index():
    return render_template('overview/index.html')


@app.route('/index/setlocale/<language>')
def new_locale(language):
    session['language'] = language
    return redirect(request.referrer)

