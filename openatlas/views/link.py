from typing import Union

from flask import flash, render_template, url_for, request
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.forms.form import build_table_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.util import required_group


@app.route('/link/delete/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def link_delete(id_: int, origin_id: int) -> Response:
    Link.delete_(id_)
    flash(_('link removed'), 'info')
    return redirect(url_for('entity_view', id_=origin_id))


@app.route('/link/insert/<int:id_>/<view>', methods=['POST', 'GET'])
@required_group('contributor')
def link_insert(id_: int, view: str) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    property_code = 'P67'  # Set defaults (for source)
    inverse = False
    if entity.class_.view == 'actor' and view == 'artifact':
        property_code = 'P52'
        inverse = True
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                property_code,
                request.form['checkbox_values'],
                inverse=inverse)
        return redirect(f"{url_for('entity_view', id_=entity.id)}#tab-{view}")
    if entity.class_.view == 'actor' and view == 'artifact':
        excluded = Entity.get_by_link_property(property_code, 'artifact')
    else:
        excluded = entity.get_linked_entities(property_code, inverse=inverse)
    return render_template(
        'form.html',
        form=build_table_form(view, excluded),
        title=_(entity.class_.view),
        crumbs=[
            [_(entity.class_.view), url_for('index', view=entity.class_.view)],
            entity,
            _('link')])
