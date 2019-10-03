# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os
from os.path import basename

from datetime import datetime, timedelta
from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.util.util import (format_date,
                                 required_group)


@app.route('/sql')
@required_group('admin')
def sql_index() -> str:
    return render_template('sql/index.html')


class SqlForm(Form):
    statement = TextAreaField(_('statement'), [InputRequired()])
    save = SubmitField(_('execute'))


@app.route('/sql/execute', methods=['POST', 'GET'])
@required_group('admin')
def sql_execute() -> str:
    path = app.config['EXPORT_FOLDER_PATH'] + '/sql'
    latest_file_date = None
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        name = basename(file)
        if name == '.gitignore':
            continue
        file_date = datetime.utcfromtimestamp(os.path.getmtime(path + '/' + file))
        if not latest_file_date or file_date > latest_file_date:
            latest_file_date = file_date
    yesterday = datetime.today() - timedelta(days=1)
    if yesterday > latest_file_date:
        print('Too old!')
    # formatted_file_date = format_date(latest_file_date)
    # print(formatted_file_date)
    # url = url_for('download_sql', filename=name)
    # data = [name, convert_size(os.path.getsize(path + '/' + name)),
    #        '<a href="' + url + '">' + uc_first(_('download')) + '</a>']
    response = ''
    form = SqlForm()
    if form.validate_on_submit():
        g.execute('BEGIN')
        try:
            g.execute(form.statement.data)
            response = '<p>Rows affected: {count}</p>'.format(count=g.cursor.rowcount)
            try:
                response += '<p>{rows}</p>'.format(rows=g.cursor.fetchall())
            except:  # pragma: no cover
                pass  # Assuming it was no SELECT statement so returning just the rowcount
            g.execute('COMMIT')
            flash(_('SQL executed'), 'info')
        except Exception as e:
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            response = e
            flash(_('error transaction'), 'error')
    return render_template('sql/execute.html', form=form, response=response)
