# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os
from datetime import datetime, timedelta
from os.path import basename
from typing import Dict

from flask import flash, g, render_template
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.util.util import convert_size, format_date, required_group


@app.route('/sql')
@required_group('admin')
def sql_index() -> str:
    return render_template('sql/index.html')


class SqlForm(FlaskForm):
    statement = TextAreaField(_('statement'), [InputRequired()])
    save = SubmitField(_('execute'))


@app.route('/sql/execute', methods=['POST', 'GET'])
@required_group('admin')
def sql_execute() -> str:
    path = app.config['EXPORT_FOLDER_PATH'] + '/sql'
    latest_file = None
    latest_file_date = None
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        name = basename(file)
        if name == '.gitignore':
            continue
        file_date = datetime.utcfromtimestamp(os.path.getmtime(path + '/' + file))
        if not latest_file_date or file_date > latest_file_date:
            latest_file = file
            latest_file_date = file_date
    file_data: Dict = {'backup_to_old': True}
    if latest_file and latest_file_date:
        yesterday = datetime.today() - timedelta(days=1)
        file_data['file'] = latest_file
        file_data['backup_to_old'] = True if yesterday > latest_file_date else False
        file_data['size'] = convert_size(os.path.getsize(path + '/' + latest_file))
        file_data['date'] = format_date(latest_file_date)
    response = ''
    form = SqlForm()
    if form.validate_on_submit() and not file_data['backup_to_old']:
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
            response = str(e)
            flash(_('error transaction'), 'error')
    return render_template('sql/execute.html', form=form, response=response, file_data=file_data)
