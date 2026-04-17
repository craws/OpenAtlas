from __future__ import annotations

from typing import Any

from flask import abort, flash, g, redirect, render_template, request, url_for
from flask_babel import gettext as _
from flask_wtf import FlaskForm
from werkzeug.wrappers import Response
from wtforms import HiddenField, SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import entity_table
from openatlas.display.util import button, link, required_group
from openatlas.display.util2 import is_authorized, manual, sanitize, uc_first
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField
from openatlas.models.entity import Entity
from openatlas.models.rights_holder import RightsHolder


class RightsHolderForm(FlaskForm):
    name: Any = StringField(
        _('name'),
        [InputRequired()],
        render_kw={'autofocus': True})
    class_: Any = SelectField(
        _('class'),
        validators=[InputRequired()],
        choices=[
            ('', ''),
            ('person', uc_first(_('person'))),
            ('group', uc_first(_('group')))])
    description = TextAreaField(_('description'))
    confirm_duplicate = HiddenField(default='false')
    save = SubmitField(_('save'))


@app.route('/rights_holder/<int:id_>')
@required_group('readonly')
def rights_holder_view(id_: int) -> str | Response:
    rights_holder = RightsHolder.get_rights_holder_by_id(id_)
    if not rights_holder:
        abort(418)

    buttons = [manual('admin/rights_holder')]
    if is_authorized('contributor'):
        buttons.append(
            button(_('edit'), url_for('rights_holder_update', id_=id_)))
    if is_authorized('editor'):
        buttons.append(
            button(
                _('delete'),
                url_for('rights_holder_delete', id_=id_),
                onclick=f"return confirm('{
                    uc_first(_(
                        'delete %(name)s?',
                        name=rights_holder.name.replace("'", "")))}?')"))

    linked_files = Entity.get_files_by_rights_holder_id(id_)
    columns = [
        'created', 'icon', 'name', 'license', 'public', 'creator',
        'license_holder', 'size', 'extension', 'description']
    files_table = entity_table(linked_files, columns=columns)
    return render_template(
        'rights_holder.html',
        rights_holder=rights_holder,
        files_table=files_table,
        buttons=buttons,
        crumbs=[
            [_('rights holder'),
             f'{url_for("admin_index")}#tab-rights-holder'],
            rights_holder.name])


@app.route('/rights_holder_insert', methods=['GET', 'POST'])
@app.route(
    '/rights_holder_insert/<int:origin_id>/<relation>',
    methods=['GET', 'POST'])
@required_group('contributor')
def rights_holder_insert(
        origin_id: int = 0,
        relation: str | None = None) -> str | Response:
    form: Any = RightsHolderForm()
    origin = Entity.get_by_id(origin_id) if origin_id else None
    if form.validate_on_submit():
        rights_holder_name = sanitize(form.name.data.strip())
        rights_holder_role = sanitize(form.class_.data)
        duplicate = any(
            rh.name == rights_holder_name
            and rh.class_ == rights_holder_role
            for rh in g.rights_holder)
        url = f'{url_for("admin_index")}#tab-rights-holder'
        if duplicate and not form.confirm_duplicate.data == 'true':
            form.name.errors.append(
                _('Duplicate found. Click "Save" to confirm anyway.'))
            form.confirm_duplicate.data = 'true'
        else:
            try:
                rights_holder = RightsHolder.insert_rights_holder({
                    'name': rights_holder_name,
                    'role': rights_holder_role,
                    'description': sanitize(form.description.data.strip())})
                if origin and relation in {'creator', 'license_holder'}:
                    RightsHolder.insert_rights_holder_link(
                        origin_id,
                        rights_holder,
                        relation)
                    url = url_for('view', id_=origin_id)
                flash(_('entity created'))
            except Exception:  # pragma: no cover
                flash(_('error transaction'), 'error')
                return redirect(url)
            return redirect(url)
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
            [_('rights holder'),
             f'{url_for("admin_index")}#tab-rights-holder'],
            link(origin) if origin else None,
            f'+ {uc_first(_("rights holder"))}'])


@app.route('/rights_holder_update/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def rights_holder_update(
        id_: int) -> str | Response:
    rights_holder = RightsHolder.get_rights_holder_by_id(id_)
    if not rights_holder:
        abort(404)

    form: Any = RightsHolderForm(obj=rights_holder)
    if request.method == 'GET':
        form.class_.data = rights_holder.class_

    if form.validate_on_submit():
        RightsHolder.update_rights_holder(id_, {
            'name': sanitize(form.name.data.strip()),
            'role': sanitize(form.class_.data),
            'description': sanitize(form.description.data.strip())})
        flash(_('info update'))
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
            [_('rights holder'),
             f'{url_for("admin_index")}#tab-rights-holder'],
            link(
                rights_holder,
                url_for('rights_holder_view', id_=rights_holder.id)),
            f'{uc_first(_('edit'))}'])


@app.route('/rights_holder_delete/<int:id_>', methods=['GET', 'POST'])
@required_group('editor')
def rights_holder_delete(id_: int) -> str | Response:
    RightsHolder.rights_holder_delete(id_)
    flash(_('entity deleted'))
    return redirect(f'{url_for("admin_index")}#tab-rights-holder')
