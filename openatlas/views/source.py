from typing import Union

from flask import render_template, request, url_for
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.forms.form import build_table_form
from openatlas.models.entity import Entity
from openatlas.util.util import required_group


@app.route('/source/add/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('contributor')
def source_add(id_: int, class_name: str) -> Union[str, Response]:
    source = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            source.link_string('P67', request.form['checkbox_values'])
        return redirect(url_for('entity_view', id_=source.id) + '#tab-' + class_name)
    form = build_table_form(class_name, source.get_linked_entities('P67'))
    return render_template('source/add.html', source=source, class_name=class_name, form=form)
