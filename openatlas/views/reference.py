from typing import Union

from flask import render_template, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.forms.form import build_add_reference_form
from openatlas.models.entity import Entity
from openatlas.util.util import required_group, uc_first


@app.route('/reference/add/<int:id_>/<view>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_add(id_: int, view: str) -> Union[str, Response]:
    reference = Entity.get_by_id(id_)
    form = build_add_reference_form(view)
    if form.validate_on_submit():
        entity = Entity.get_by_id(getattr(form, view).data)
        reference.link('P67', entity, form.page.data)
        return redirect(f"{url_for('view', id_=reference.id)}#tab-{view}")
    if reference.class_.name == 'external_reference':
        form.page.label.text = uc_first(_('link text'))
    return render_template(
        'display_form.html',
        form=form,
        title=_('reference'),
        crumbs=[
            [_('reference'), url_for('index', view='reference')],
            reference,
            _('link')])
