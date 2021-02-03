from typing import Union

from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.forms.field import TableField
from openatlas.forms.form import build_add_reference_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.display import link, uc_first
from openatlas.util.util import required_group


class AddReferenceForm(FlaskForm):  # type: ignore
    reference = TableField(_('reference'), [InputRequired()])
    page = StringField(_('page'))
    save = SubmitField(_('insert'))


@app.route('/reference/add/<int:id_>/<class_name>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_add(id_: int, class_name: str) -> Union[str, Response]:
    reference = Entity.get_by_id(id_)
    form = build_add_reference_form(class_name)
    if form.validate_on_submit():
        property_code = 'P128' if reference.class_.code == 'E84' else 'P67'
        entity = Entity.get_by_id(getattr(form, class_name).data)
        reference.link(property_code, entity, form.page.data)
        return redirect(url_for('entity_view', id_=reference.id) + '#tab-' + class_name)
    if reference.system_type == 'external reference':
        form.page.label.text = uc_first(_('link text'))
    return render_template('display_form.html',
                           reference=reference,
                           form=form,
                           class_name=class_name,
                           title=_('reference'),
                           crumbs=[[_('reference'), url_for('index', class_='reference')],
                                   reference,
                                   _('link')])


@app.route('/reference/link-update/<int:link_id>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def reference_link_update(link_id: int, origin_id: int) -> Union[str, Response]:
    link_ = Link.get_by_id(link_id)
    origin = Entity.get_by_id(origin_id)
    form = AddReferenceForm()
    del form.reference
    if form.validate_on_submit():
        link_.description = form.page.data
        link_.update()
        flash(_('info update'), 'info')
        tab = '#tab-' + (link_.range.view_name if origin.view_name == 'reference' else 'reference')
        return redirect(url_for('entity_view', id_=origin.id) + tab)
    form.save.label.text = _('save')
    form.page.data = link_.description
    if link_.domain.system_type == 'external reference':
        form.page.label.text = uc_first(_('link text'))
    linked_object = link_.domain if link_.domain.id != origin.id else link_.range
    return render_template('display_form.html',
                           origin=origin,
                           form=form,
                           linked_object=linked_object,
                           crumbs=[[_(origin.view_name), url_for('index', class_=origin.view_name)],
                                   origin,
                                   linked_object,
                                   _('edit')])
