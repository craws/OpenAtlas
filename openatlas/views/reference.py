import ast
from typing import Union

from flask import render_template, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.util import display_form, required_group, uc_first
from openatlas.forms.form import get_add_reference_form
from openatlas.models.entity import Entity


@app.route('/reference/add/<int:id_>/<view>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_add(id_: int, view: str) -> Union[str, Response]:
    reference = Entity.get_by_id(id_)
    form = get_add_reference_form(view)
    if form.validate_on_submit():
        ids = ast.literal_eval(getattr(form, view).data)
        ids = ids if isinstance(ids, list) else [int(ids)]
        reference.link('P67', Entity.get_by_ids(ids), form.page.data)
        return redirect(f"{url_for('view', id_=reference.id)}#tab-{view}")
    if reference.class_.name == 'external_reference':
        form.page.label.text = uc_first(_('link text'))
    return render_template(
        'content.html',
        content=display_form(form),
        title=_('reference'),
        crumbs=[
            [_('reference'), url_for('index', view='reference')],
            reference,
            _('link')])
