from typing import Any

from flask import flash, g, redirect, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from markupsafe import Markup
from werkzeug.wrappers import Response
from wtforms import IntegerField, SelectField

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.tab import Tab
from openatlas.display.util import required_group
from openatlas.display.util2 import is_authorized, manual
from openatlas.forms.field import SubmitField
from openatlas.models.bones import bone_inventory, create_bones
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.views.tools import tools_start_crumbs


@app.route('/tools/bones/<int:id_>')
@required_group('readonly')
def bones(id_: int) -> str:
    entity = Entity.get_by_id(id_, types=True)
    buttons = [manual('tools/anthropological_analyses')]
    if is_authorized('contributor'):
        pass
    return render_template(
        'tabs.html',
        entity=entity,
        tabs={
            'info': Tab(
                'bones',
                render_template(
                    'tools/bones.html',
                    entity=entity,
                    data=bone_inventory),
                buttons=buttons)},
        crumbs=tools_start_crumbs(entity) + [
            [_('tools'), url_for('tools_index', id_=entity.id)],
            _('bone inventory')])


@app.route('/tools/bones_update/<int:id_>/<category>', methods=['GET', 'POST'])
@required_group('contributor')
def bones_update(id_: int, category: str) -> str | Response:
    entity = Entity.get_by_id(id_, types=True)
    form = bones_form(entity, category)
    structure = bone_inventory[category.replace('_', ' ')]
    if form.validate_on_submit():
        if structure['preservation']:
            structure['data'] = getattr(form, category).data
        add_form_data_to_structure(form, structure)
        try:
            Transaction.begin()
            create_bones(entity, category.replace('_', ' '), structure)
            Transaction.commit()
            flash(_('info update'), 'info')
            return redirect(url_for('bones', id_=entity.id))
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
    else:
        add_data_to_structure(entity, structure)
    return render_template(
        'tabs.html',
        entity=entity,
        tabs={
            'info': Tab(
                'bones',
                content=
                Markup(f'<form method="post">{form.csrf_token}') +
                bone_rows(form, category, structure) + form.save +
                Markup('</form>'),
                buttons=[manual('tools/anthropological_analyses')])},
        crumbs=tools_start_crumbs(entity) + [
            [_('tools'), url_for('tools_index', id_=entity.id)],
            [_('bone inventory'), url_for('bones', id_=entity.id)],
            _('edit')])


def add_data_to_structure(entity: Entity, structure_: dict[str, Any]) -> None:
    pass


def add_form_data_to_structure(
        form: FlaskForm,
        structure_: dict[str, Any]) -> None:
    if 'subs' in structure_:
        for label, value in structure_['subs'].items():
            if value['preservation']:
                value['data'] = getattr(form, label.replace(' ', '-')).data
            if 'subs' in value:
                for item in value['subs'].values():
                    add_form_data_to_structure(form, item)


def bones_form(entity: Entity, category: str) -> Any:
    class Form(FlaskForm):
        pass

    inventory = bone_inventory[category.replace('_', ' ')]
    options = {
        g.types[id_].name: id_ for id_
        in Type.get_hierarchy('Bone preservation').subs}
    choices = [
        ('', _('undefined')),
        (options['0%'], '0%'),
        (options['1-24%'], '1-24%'),
        (options['25-74%'], '25-74%'),
        (options['75-99%'], '75-99%'),
        (options['100%'], '100%')]
    if inventory['preservation'] == 'percent':
        setattr(
            Form,
            category.replace(' ', '-'),
            SelectField(category, choices=choices))
    for label, sub in inventory['subs'].items():
        bone_fields_recursive(Form, label, sub, choices)
    setattr(Form, 'save', SubmitField(_('save')))
    return Form()


def bone_fields_recursive(form, label, item, choices):
    if item['preservation'] == 'percent':
        setattr(
            form,
            label.replace(' ', '-'),
            SelectField(label, choices=choices))
    elif item['preservation'] == 'number':
        setattr(form, label.replace(' ', '-'), IntegerField())
    if 'subs' in item:
        for label, sub in item['subs'].items():
            bone_fields_recursive(form, label, sub, choices)


def bone_rows(
        form: Any,
        label: str,
        item: dict[str, Any],
        offset: float = 0):
    html = Markup(
        f'<div style="margin:0.5em;margin-left:{0.5 + offset * 2}em">'
        f'<span style="margin-right:2em;">{label.replace("_", " ")}</span>')
    if item['preservation']:
        html += str(getattr(form, label.replace(' ', '-')))
    html += Markup('</div>')
    if 'subs' in item:
        for label, sub in item['subs'].items():
            html += bone_rows(form, label, sub, offset + 0.5)
    return html
