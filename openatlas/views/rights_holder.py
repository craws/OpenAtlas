from __future__ import annotations

from typing import Any

from flask import flash, g, redirect, render_template, request, url_for, abort
from flask_babel import gettext as _
from flask_wtf import FlaskForm
from werkzeug.wrappers import Response
from wtforms import HiddenField, SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.util import (
    required_group)
from openatlas.display.util2 import sanitize, uc_first
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField
from openatlas.models.rights_holder import RightsHolder


# todo: Select fields need to get openatlas class name from config model
class RightsHolderForm(FlaskForm):
    name: Any = StringField(
        _('name'),
        [InputRequired()],
        render_kw={'autofocus': True})
    role: Any = SelectField(
        _('role'),
        choices=[('person', _('person')), ('group', _('group'))])
    description = TextAreaField(_('info'))
    confirm_duplicate = HiddenField(default='false')
    save = SubmitField(_('save'))


@app.route('/rights_holder_insert', methods=['GET', 'POST'])
@required_group('manager')
def rights_holder_insert() -> str | Response:  # Todo: move to other file
    form: Any = RightsHolderForm()

    if form.validate_on_submit():
        rights_holder_name = sanitize(form.name.data)
        rights_holder_role = sanitize(form.role.data)

        already_confirmed = form.confirm_duplicate.data == 'true'
        duplicate = any(
            rh.name == rights_holder_name
            and rh.class_.name == rights_holder_role
            for rh in g.rights_holder)

        if duplicate and not already_confirmed:
            form.name.errors.append(
                _('This Name-Role combination already exists. '
                  'If this is a different person, click "Save" to confirm.'))
            form.confirm_duplicate.data = 'true'
        else:
            RightsHolder.insert_rights_holder({
                'name': rights_holder_name,
                'role': rights_holder_role,
                'description': sanitize(form.description.data)})
            flash(_('entity created'))
            return redirect(f'{url_for("admin_index")}#tab-rights-holder')

    return render_template(
        'tabs.html',
        tabs={
            'rights_holder': Tab(
                'rights_holder',
                content=display_form(
                    form,
                    'rights-holder-form',
                    manual_page='admin/rights_holder'))},
        title=_('rights holder'),
        crumbs=[
            [_('admin'), f'{url_for("admin_index")}#tab-rights-holder'],
            f'+ {uc_first(_("rights holder"))}'])


@app.route('/rights_holder_update/<int:id_>', methods=['GET', 'POST'])
@required_group('manager')
def rights_holder_update(
        id_: int) -> str | Response:  # Todo: move to other file
    rights_holder = RightsHolder.get_rights_holder_by_id(id_)
    if not rights_holder:
        abort(404)

    form: Any = RightsHolderForm(obj=rights_holder)
    if request.method == 'GET':
        form.role.data = rights_holder.class_.name

    if form.validate_on_submit():
        RightsHolder.update_rights_holder(id_, {
            'name': sanitize(form.name.data),
            'role': sanitize(form.role.data),
            'description': sanitize(form.description.data)})
        flash(_('updated'))
        return redirect(f'{url_for("admin_index")}#tab-rights-holder')

    return render_template(
        'tabs.html',
        tabs={
            'rights_holder': Tab(
                'rights_holder',
                content=display_form(
                    form,
                    'rights-holder-form',
                    manual_page='admin/rights_holder'))},
        title=_('rights holder'),
        crumbs=[
            [_('admin'), f'{url_for("admin_index")}#tab-rights-holder'],
            f'{uc_first(_("rights holder"))}: {rights_holder.name}'])


@app.route('/rights_holder_delete/<int:id_>', methods=['GET', 'POST'])
@required_group('manager')
def rights_holder_delete(id_: int) -> str | Response:
    RightsHolder.rights_holder_delete(id_)
    flash(_('entity deleted'))
    return redirect(f'{url_for("admin_index")}#tab-rights-holder')
