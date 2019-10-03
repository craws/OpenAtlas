# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, g, render_template
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import (SubmitField, TextAreaField)
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.util.util import (required_group)


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
