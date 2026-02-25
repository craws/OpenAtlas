from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for, abort
from flask_babel import gettext as _
from flask_wtf import FlaskForm
from werkzeug.wrappers import Response
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.util import (
    required_group)
from openatlas.display.util2 import sanitize, uc_first
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField
from openatlas.models.rights_holder import RightsHolder


class RightsHolderForm(FlaskForm):
    name: Any = StringField(
        _('name'),
        [InputRequired()],
        render_kw={'autofocus': True})
    role: Any = SelectField(_('role'), choices=('person', 'group'))
    description = TextAreaField(_('info'))
    save = SubmitField(_('save'))


@app.route('/rights_holder_insert', methods=['GET', 'POST'])
@required_group('manager')
def rights_holder_insert() -> str | Response:  # Todo: move to other file
    # Todo: move to other file
    form: Any = RightsHolderForm()

    if form.validate_on_submit():
        rights_holder = RightsHolder.insert({
            'name': sanitize(form.name.data),
            'role': sanitize(form.role.data),
            'description': sanitize(form.description.data)})
        flash(_('created'))  # todo: change name
        print(rights_holder)
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
    rights_holder = RightsHolder.get(id_)
    if not rights_holder:
        abort(404)

    form: Any = RightsHolderForm(obj=rights_holder)
    if request.method == 'GET':
        form.role.data = rights_holder.class_

    if form.validate_on_submit():
        RightsHolder.update(id_, {
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
