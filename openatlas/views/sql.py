# Created by Alexander Watzinger and others. Please see README.md for licensing information

from flask import render_template

from openatlas import app
from openatlas.util.util import (required_group)


@app.route('/sql')
@required_group('admin')
def sql_index() -> str:
    return render_template('sql/index.html')


@app.route('/sql/execute')
@required_group('admin')
def sql_execute() -> str:
    return render_template('sql/execute.html')
